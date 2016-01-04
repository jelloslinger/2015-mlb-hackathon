# -*- coding: utf-8 -*-

from collections import namedtuple
import csv

from datapro.framework.model.common import Date
from datapro.framework.db import OrmConnection
from datapro.framework.job import EtlJob
from datapro.framework.validation import Validator

from mlb import BATTED_BALL_ANGLES, BATTED_BALL_DISTANCES, BATTED_BALL_TYPE, MLB_TEAMS, PA_RESULT, PITCH_RESULT, PITCH_TYPE
from mlb.helper import BaselineSampleManager
from mlb.model import Game, Outcome, Player, Situation, PitchByPitch


if __name__ == '__main__':

    columns = {
        'seasonYear': -1,
        'gameString': -1,
        'gameDate': -1,
        'gameType': -1,
        'visitor': -1,
        'home': -1,
        'visitingTeamFinalRuns': -1,
        'homeTeamFinalRuns': -1,
        'inning': -1,
        'side': -1,
        'batterId': -1,
        'batter': -1,
        'batterHand': -1,
        'pitcherId': -1,
        'pitcher': -1,
        'pitcherHand': -1,
        'catcherId': -1,
        'catcher': -1,
        'timesFaced': -1,
        'batterPosition': -1,
        'balls': -1,
        'strikes': -1,
        'outs': -1,
        'manOnFirst': -1,
        'manOnSecond': -1,
        'manOnThird': -1,
        'endManOnFirst': -1,
        'endManOnSecond': -1,
        'endManOnThird': -1,
        'visitingTeamCurrentRuns': -1,
        'homeTeamCurrentRuns': -1,
        'pitchResult': -1,
        'pitchType': -1,
        'releaseVelocity': -1,
        'spinRate': -1,
        'spinDir': -1,
        'px': -1,
        'pz': -1,
        'szt': -1,
        'szb': -1,
        'x0': -1,
        'y0': -1,
        'z0': -1,
        'vx0': -1,
        'vy0': -1,
        'vz0': -1,
        'ax': -1,
        'ay': -1,
        'az': -1,
        'paResult': -1,
        'runsHome': -1,
        'battedBallType': -1,
        'battedBallAngle': -1,
        'battedBallDistance': -1,
        'atbatDesc': -1
    }

    connection = OrmConnection('common')

    with EtlJob('mlb') as job:

        dims = {
            # Common Dimensions
            Date.__tablename__: {},
            # MLB Dimensions
            Game.__tablename__: {},
            Outcome.__tablename__: {},
            Player.__tablename__: {},
            Situation.__tablename__: {},
        }

        # Common Dimensions
        date = namedtuple('date', ['date'])
        for d in connection.session.query(Date.id, Date.date):
            dims[Date.__tablename__][date(d[1])] = d[0]

        # MLB Dimensions
        game = namedtuple('game', ['identifier'])
        for d in connection.session.query(Game.id, Game.gameIdentifier):
            dims[Game.__tablename__][game(d[1])] = d[0]

        outcome = namedtuple('outcome', ['paResult', 'battedBallType', 'battedBallAngleDescription', 'battedBallDistanceDescription'])
        for d in connection.session.query(
                Outcome.id,
                Outcome.paResult,
                Outcome.battedBallType,
                Outcome.battedBallAngleDescription,
                Outcome.battedBallDistanceDescription
        ):
            dims[Outcome.__tablename__][outcome(d[1], d[2], d[3], d[4])] = d[0]

        player = namedtuple('player', ['playerIdentifier', 'teamAbbreviation'])
        for d in connection.session.query(Player.id, Player.playerIdentifier, Player.teamAbbreviation):
            dims[Player.__tablename__][player(d[1], d[2])] = d[0]

        situation = namedtuple('situation', ['numberBalls', 'numberStrikes', 'numberOuts', 'pitchType', 'pitchResult'])
        for d in connection.session.query(
            Situation.id,
            Situation.numberBalls,
            Situation.numberStrikes,
            Situation.numberOuts,
            Situation.pitchType,
            Situation.pitchResult
        ):
            dims[Situation.__tablename__][situation(d[1], d[2], d[3], d[4], d[5])] = d[0]

        facts = []
        key_game = None
        mlb_event_dim = 0
        sample_manager = BaselineSampleManager()

        with open('./mlb/reference/2015.csv') as f:

            csv_reader = csv.reader(f)
            v = Validator()

            for i, row in enumerate(csv_reader):
                # While on the header row, fill in the column map.
                if i == 0:
                    j = 0
                    for column_name in row:
                        if column_name in columns:
                            columns[column_name] = j
                        else:
                            raise ValueError('Unexpected column: {0}'.format(column_name))

                        j += 1

                    # Check if any expected column have not been mapped
                    for column_name, column_ordinal in iter(columns.items()):
                        if column_ordinal == -1:
                            raise ValueError('Expected column is unmapped: {0}'.format(column_name))

                    continue

                v.reset('[row: {0}, {{key}}] {{message}}'.format(i))

                # Date
                v.date('date', row[columns['gameDate']].split(' ')[0], '%Y-%m-%d')

                # Game
                v.string('gameIdentifier', row[columns['gameString']], max_length=64)
                v.datetime('gameDatetime', row[columns['gameDate']], '%Y-%m-%d %H:%M:00')
                v.string('gameType', row[columns['gameType']], max_length=4)
                v.string('visitor', row[columns['visitor']], max_length=4)
                v.string('visitorLong', MLB_TEAMS[row[columns['visitor']]], max_length=64)
                v.string('home', row[columns['home']], max_length=4)
                v.string('homeLong', MLB_TEAMS[row[columns['home']]], max_length=64)

                # Outcome
                v.string('paResult', row[columns['paResult']], blanks_ok=True, max_length=8)
                v.string('paResultDescription', PA_RESULT[row[columns['paResult']]], blanks_ok=True, max_length=32)
                v.string('battedBallType', row[columns['battedBallType']], blanks_ok=True, max_length=8)
                v.string('battedBallTypeDescription', BATTED_BALL_TYPE[row[columns['battedBallType']]], blanks_ok=True, max_length=32)

                # Outcome Metrics
                batted_ball_angle = row[columns['battedBallAngle']] if len(row[columns['battedBallAngle']]) > 0 else None
                batted_ball_distance = row[columns['battedBallDistance']] if len(row[columns['battedBallDistance']]) > 0 else None

                v.decimal('battedBallAngle', row[columns['battedBallAngle']], 4, nulls_ok=True)
                v.decimal('battedBallDistance', row[columns['battedBallAngle']], 4, nulls_ok=True)

                if v.properties['battedBallAngle'] is None:
                    batted_ball_angle_description = BATTED_BALL_ANGLES[0]
                elif v.properties['battedBallAngle'] < -45:
                    batted_ball_angle_description = BATTED_BALL_ANGLES[1]
                elif v.properties['battedBallAngle'] < -15:
                    batted_ball_angle_description = BATTED_BALL_ANGLES[2]
                elif v.properties['battedBallAngle'] <= 15:
                    batted_ball_angle_description = BATTED_BALL_ANGLES[3]
                elif v.properties['battedBallAngle'] <= 45:
                    batted_ball_angle_description = BATTED_BALL_ANGLES[4]
                else:
                    batted_ball_angle_description = BATTED_BALL_ANGLES[5]

                v.string('battedBallAngleDescription', batted_ball_angle_description, blanks_ok=True, max_length=16)

                if v.properties['battedBallDistance'] is None:
                    batted_ball_distance_description = BATTED_BALL_DISTANCES[0]
                elif v.properties['battedBallDistance'] <= 150:
                    batted_ball_distance_description = BATTED_BALL_DISTANCES[1]
                elif v.properties['battedBallDistance'] <= 300:
                    batted_ball_distance_description = BATTED_BALL_DISTANCES[2]
                else:
                    batted_ball_distance_description = BATTED_BALL_DISTANCES[3]

                v.string('battedBallDistanceDescription', batted_ball_distance_description, blanks_ok=True, max_length=16)

                if row[columns['side']] == 'T':
                    offense_team_abbreviation = row[columns['visitor']]
                    defense_team_abbreviation = row[columns['home']]
                else:
                    offense_team_abbreviation = row[columns['home']]
                    defense_team_abbreviation = row[columns['visitor']]

                # Player (Batter)
                v.int('playerIdentifier_batter', row[columns['batterId']])
                v.string('playerName_batter', row[columns['batter']], max_length=64)
                v.string('teamAbbreviation_batter', offense_team_abbreviation, max_length=4)
                v.string('teamFullName_batter', MLB_TEAMS[offense_team_abbreviation], max_length=32)

                # Player (Pitcher)
                v.int('playerIdentifier_pitcher', row[columns['pitcherId']])
                v.string('playerName_pitcher', row[columns['pitcher']], max_length=64)
                v.string('teamAbbreviation_pitcher', defense_team_abbreviation, max_length=4)
                v.string('teamFullName_pitcher', MLB_TEAMS[defense_team_abbreviation], max_length=32)

                # Player (Catcher)
                v.int('playerIdentifier_catcher', row[columns['catcherId']])
                v.string('playerName_catcher', row[columns['catcher']], max_length=64)
                v.string('teamAbbreviation_catcher', defense_team_abbreviation, max_length=4)
                v.string('teamFullName_catcher', MLB_TEAMS[defense_team_abbreviation], max_length=32)

                # Situation
                v.int('numberBalls', row[columns['balls']])
                v.int('numberStrikes', row[columns['strikes']])
                v.int('numberOuts', row[columns['outs']])
                v.string('pitchResult', row[columns['pitchResult']], max_length=4)
                v.string('pitchResultDescription', PITCH_RESULT[row[columns['pitchResult']]], max_length=32)
                v.string('pitchType', row[columns['pitchType']], max_length=2)
                v.string('pitchResultDescription', PITCH_TYPE[row[columns['pitchType']]], max_length=32)

                # Metrics
                v.decimal('releaseVelocity', row[columns['releaseVelocity']], 4, nulls_ok=True)
                v.decimal('spinRate', row[columns['spinRate']], 4, nulls_ok=True)
                v.decimal('spinDirection', row[columns['spinDir']], 4, nulls_ok=True)
                v.decimal('px', row[columns['px']], 4, nulls_ok=True)
                v.decimal('pz', row[columns['pz']], 4, nulls_ok=True)
                v.decimal('szt', row[columns['szt']], 4, nulls_ok=True)
                v.decimal('szb', row[columns['szb']], 4, nulls_ok=True)
                v.decimal('x0', row[columns['x0']], 4, nulls_ok=True)
                v.decimal('y0', row[columns['y0']], 4, nulls_ok=True)
                v.decimal('z0', row[columns['z0']], 4, nulls_ok=True)
                v.decimal('vx0', row[columns['vx0']], 4, nulls_ok=True)
                v.decimal('vy0', row[columns['vy0']], 4, nulls_ok=True)
                v.decimal('vz0', row[columns['vz0']], 4, nulls_ok=True)
                v.decimal('ax', row[columns['ax']], 4, nulls_ok=True)
                v.decimal('ay', row[columns['ay']], 4, nulls_ok=True)
                v.decimal('az', row[columns['az']], 4, nulls_ok=True)

                if not v.valid:
                    # counts['invalid'] += 1
                    continue
                elif key_game != game(v.properties['gameIdentifier']):
                    mlb_event_dim = 0

                mlb_event_dim += 1

                v.properties.update({
                    'atBat': 0,
                    'plateAppearance': 0,
                    'swing': 0,
                    'ballInPlay': 0,
                    'lineDrive': 0,
                    'hit': 0,
                    'single': 0,
                    'double': 0,
                    'triple': 0,
                    'homeRun': 0,
                    'baseOnBalls': 0,
                    'intentionalBaseOnBalls': 0,
                    'strikeOut': 0
                })

                if len(v.properties['paResult']):
                    v.properties['plateAppearance'] = 1

                if v.properties['paResult'] in ('S', 'D', 'T', 'HR', 'IP_OUT', 'K', 'FC', 'DP', 'TP'):
                    v.properties['atBat'] = 1
                    if v.properties['paResult'] in ('S', 'D', 'T', 'HR'):
                        v.properties['hit'] = 1
                        if v.properties['paResult'] == 'S':
                            v.properties['single'] = 1
                        elif v.properties['paResult'] == 'D':
                            v.properties['double'] = 1
                        elif v.properties['paResult'] == 'T':
                            v.properties['triple'] = 1
                        elif v.properties['paResult'] == 'HR':
                            v.properties['homeRun'] = 1
                    elif v.properties['paResult'] == 'K':
                        v.properties['strikeOut'] = 1
                elif v.properties['paResult'] == 'BB':
                    v.properties['baseOnBalls'] = 1
                elif v.properties['paResult'] == 'IBB':
                    v.properties['intentionalBaseOnBalls'] = 1

                if v.properties['pitchResult'] in ('SS', 'F', 'FT', 'FB', 'MB', 'IP'):
                    v.properties['swing'] = 1
                    if v.properties['pitchResult'] == 'IP':
                        v.properties['ballInPlay'] = 1

                if v.properties['battedBallType'] == 'LD':
                    v.properties['lineDrive'] = 1

                fact = {
                    'dateId': -1,
                    'mlbGameId': -1,
                    'mlbPlayerBatterId': -1,
                    'mlbPlayerPitcherId': -1,
                    'mlbPlayerCatcherId': -1,
                    'mlbSituationId': -1,
                    'mlbOutcomeId': -1,
                    'mlbEventDim': mlb_event_dim,
                    'mlbSampleDim': -1,
                    'mlbBaselineSampleDim': -1,
                    'releaseVelocity': v.properties['releaseVelocity'],
                    'spinRate': v.properties['spinRate'],
                    'spinDirection': v.properties['spinDirection'],
                    'px': v.properties['px'],
                    'pz': v.properties['pz'],
                    'szt': v.properties['szt'],
                    'szb': v.properties['szb'],
                    'x0': v.properties['x0'],
                    'y0': v.properties['y0'],
                    'z0': v.properties['z0'],
                    'vx0': v.properties['vx0'],
                    'vy0': v.properties['vy0'],
                    'vz0': v.properties['vz0'],
                    'ax': v.properties['ax'],
                    'ay': v.properties['ay'],
                    'az': v.properties['az'],
                    'battedBallAngle': v.properties['battedBallAngle'],
                    'battedBallDistance': v.properties['battedBallDistance'],
                    'atBat': v.properties['atBat'],
                    'plateAppearance': v.properties['plateAppearance'],
                    'swing': v.properties['swing'],
                    'ballInPlay': v.properties['ballInPlay'],
                    'lineDrive': v.properties['lineDrive'],
                    'hit': v.properties['hit'],
                    'single': v.properties['single'],
                    'double': v.properties['double'],
                    'triple': v.properties['triple'],
                    'homeRun': v.properties['homeRun'],
                    'baseOnBalls': v.properties['baseOnBalls'],
                    'intentionalBaseOnBalls': v.properties['intentionalBaseOnBalls'],
                    'strikeOut': v.properties['strikeOut']
                }

                # Date
                fact.update({'dateId': dims[Date.__tablename__][date(v.properties['date'])]})

                # Game
                key_game = game(v.properties['gameIdentifier'])
                if key_game not in dims[Game.__tablename__]:
                    d = Game.from_dict(v.properties, subset=[col.name for col in Game.__table__.columns])
                    connection.session.add(d)
                    connection.session.flush()
                    # counts['games'] += 1
                    dims[Game.__tablename__][key_game] = d.id

                fact.update({'mlbGameId': dims[Game.__tablename__][key_game]})

                # Player (Batter)
                v.properties['playerIdentifier'] = v.properties['playerIdentifier_batter']
                v.properties['playerName'] = v.properties['playerName_batter']
                v.properties['teamAbbreviation'] = v.properties['teamAbbreviation_batter']
                v.properties['teamFullName'] = v.properties['teamFullName_batter']

                key_player = player(v.properties['playerIdentifier'], v.properties['teamAbbreviation'])
                if key_player not in dims[Player.__tablename__]:
                    d = Player.from_dict(v.properties, subset=[col.name for col in Player.__table__.columns])
                    connection.session.add(d)
                    connection.session.flush()
                    # counts['players'] += 1
                    dims[Player.__tablename__][key_player] = d.id

                fact.update({'mlbPlayerBatterId': dims[Player.__tablename__][key_player]})

                # Player (Pitcher)
                v.properties['playerIdentifier'] = v.properties['playerIdentifier_pitcher']
                v.properties['playerName'] = v.properties['playerName_pitcher']
                v.properties['teamAbbreviation'] = v.properties['teamAbbreviation_pitcher']
                v.properties['teamFullName'] = v.properties['teamFullName_pitcher']

                key_player = player(v.properties['playerIdentifier'], v.properties['teamAbbreviation'])
                if key_player not in dims[Player.__tablename__]:
                    d = Player.from_dict(v.properties, subset=[col.name for col in Player.__table__.columns])
                    connection.session.add(d)
                    connection.session.flush()
                    # counts['players'] += 1
                    dims[Player.__tablename__][key_player] = d.id

                fact.update({'mlbPlayerPitcherId': dims[Player.__tablename__][key_player]})

                # Player (Catcher)
                v.properties['playerIdentifier'] = v.properties['playerIdentifier_catcher']
                v.properties['playerName'] = v.properties['playerName_catcher']
                v.properties['teamAbbreviation'] = v.properties['teamAbbreviation_catcher']
                v.properties['teamFullName'] = v.properties['teamFullName_catcher']

                key_player = player(v.properties['playerIdentifier'], v.properties['teamAbbreviation'])
                if key_player not in dims[Player.__tablename__]:
                    d = Player.from_dict(v.properties, subset=[col.name for col in Player.__table__.columns])
                    connection.session.add(d)
                    connection.session.flush()
                    # counts['players'] += 1
                    dims[Player.__tablename__][key_player] = d.id

                fact.update({'mlbPlayerCatcherId': dims[Player.__tablename__][key_player]})

                # Situation
                key_situation = situation(
                    v.properties['numberBalls'],
                    v.properties['numberStrikes'],
                    v.properties['numberOuts'],
                    v.properties['pitchType'],
                    v.properties['pitchResult']
                )
                fact.update({'mlbSituationId': dims[Situation.__tablename__][key_situation]})

                # Outcome
                key_outcome = outcome(
                    v.properties['paResult'],
                    v.properties['battedBallType'],
                    v.properties['battedBallAngleDescription'],
                    v.properties['battedBallDistanceDescription']
                )
                fact.update({'mlbOutcomeId': dims[Outcome.__tablename__][key_outcome]})

                sample_manager.side = row[columns['side']]
                sample_manager.fact = fact

                if sample_manager.is_sample_finished():
                    facts.extend(sample_manager.facts)
                    sample_manager.facts = []
                elif sample_manager.is_game_finished():
                    for side in (sample_manager.other_side, sample_manager.side, ):
                        sample_manager.side = side
                        sample_manager.zero_baseline_sample()
                        facts.extend(sample_manager.facts)
                        sample_manager.facts = []
                elif sample_manager.is_pitcher_finished():
                    sample_manager.zero_baseline_sample()
                    facts.extend(sample_manager.facts)
                    sample_manager.facts = []

                sample_manager.reset()
                sample_manager.fact.update({'mlbSampleDim': sample_manager.baseline_sample_number})
                sample_manager.fact.update({'mlbBaselineSampleDim': sample_manager.baseline_sample_number})
                sample_manager.add()

            sample_manager.fact = {
                'mlbGameId': 0,
                'mlbPlayerBatterId': 0,
                'mlbPlayerPitcherId': 0
            }

            if sample_manager.is_sample_finished():
                facts.extend(sample_manager.facts)
                sample_manager.facts = []

            for side in (sample_manager.other_side, sample_manager.side, ):
                sample_manager.side = side
                sample_manager.zero_baseline_sample()
                facts.extend(sample_manager.facts)
                sample_manager.facts = []

            # sample_manager.reset()

        # Free some memory
        del dims

        for f in facts:

            pbp = PitchByPitch(
                dateId=f['dateId'],
                mlbGameId=f['mlbGameId'],
                mlbPlayerBatterId=f['mlbPlayerBatterId'],
                mlbPlayerPitcherId=f['mlbPlayerPitcherId'],
                mlbPlayerCatcherId=f['mlbPlayerCatcherId'],
                mlbSituationId=f['mlbSituationId'],
                mlbOutcomeId=f['mlbOutcomeId'],
                mlbEventDim=f['mlbEventDim'],
                mlbSampleDim=f['mlbSampleDim'],
                mlbBaselineSampleDim=f['mlbBaselineSampleDim'],
                releaseVelocity=f['releaseVelocity'],
                spinRate=f['spinRate'],
                spinDirection=f['spinDirection'],
                px=f['px'],
                pz=f['pz'],
                szt=f['szt'],
                szb=f['szb'],
                x0=f['x0'],
                y0=f['y0'],
                z0=f['z0'],
                vx0=f['vx0'],
                vy0=f['vy0'],
                vz0=f['vz0'],
                ax=f['ax'],
                ay=f['ay'],
                az=f['az'],
                battedBallAngle=f['battedBallAngle'],
                battedBallDistance=f['battedBallDistance'],
                atBat=f['atBat'],
                plateAppearance=f['plateAppearance'],
                swing=f['swing'],
                ballInPlay=f['ballInPlay'],
                lineDrive=f['lineDrive'],
                hit=f['hit'],
                single=f['single'],
                double=f['double'],
                triple=f['triple'],
                homeRun=f['homeRun'],
                baseOnBalls=f['baseOnBalls'],
                intentionalBaseOnBalls=f['intentionalBaseOnBalls'],
                strikeOut=f['strikeOut']
            )

            connection.session.add(pbp)
            connection.block_flush()

    connection.session.commit()
