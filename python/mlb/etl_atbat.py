# -*- coding: utf-8 -*-

from sqlalchemy import func

from datapro.framework.model.common import Date
from datapro.framework.db import OrmConnection
from datapro.framework.job import EtlJob

from mlb.model import AtBat, PitchByPitch


if __name__ == '__main__':

    connection = OrmConnection('common')
    cumulative_stats = dict()

    with EtlJob('mlb') as job:

        at_bat_query = connection.session.query(
            Date.id.label('dateId'),
            PitchByPitch.mlbPlayerBatterId,
            PitchByPitch.mlbPlayerPitcherId,
            PitchByPitch.mlbSampleDim,
            PitchByPitch.mlbBaselineSampleDim,
            func.sum(PitchByPitch.swing).label('swings'),
            func.sum(PitchByPitch.ballInPlay).label('ballInPlay'),
            func.sum(PitchByPitch.lineDrive).label('lineDrive')
        ).join(
            PitchByPitch,
            Date.id == PitchByPitch.dateId
        ).group_by(
            Date.id,
            PitchByPitch.mlbPlayerBatterId,
            PitchByPitch.mlbPlayerPitcherId,
            PitchByPitch.mlbSampleDim,
            PitchByPitch.mlbBaselineSampleDim
        ).order_by(
            Date.id,
            PitchByPitch.mlbSampleDim
        )

        for ab in at_bat_query:

            cumulative_stats.setdefault(ab.mlbPlayerBatterId, {
                # Swings to Ball In Play
                'last_at_bat_ball_in_play': False,
                'last_sample_at_bat_ball_in_play': False,
                'swings_to_ball_in_play': 0,
                'sample_swings_to_ball_in_play': 0,
                'delta_swings_to_ball_in_play': 0,
                # Swings to Line Drive
                'last_at_bat_line_drive': False,
                'last_sample_at_bat_line_drive': False,
                'swings_to_line_drive': 0,
                'sample_swings_to_line_drive': 0,
                'delta_swings_to_line_drive': 0
            })

            # Swings to Ball in Play
            if cumulative_stats[ab.mlbPlayerBatterId]['last_at_bat_ball_in_play']:
                cumulative_stats[ab.mlbPlayerBatterId].update({'swings_to_ball_in_play': 0})
            if ab.mlbBaselineSampleDim > 0 and cumulative_stats[ab.mlbPlayerBatterId]['last_sample_at_bat_ball_in_play']:
                cumulative_stats[ab.mlbPlayerBatterId].update({'sample_swings_to_ball_in_play': 0})

            cumulative_stats[ab.mlbPlayerBatterId]['swings_to_ball_in_play'] += ab.swings
            if ab.mlbBaselineSampleDim > 0:
                cumulative_stats[ab.mlbPlayerBatterId]['sample_swings_to_ball_in_play'] += ab.swings

            if ab.ballInPlay > 0:
                cumulative_stats[ab.mlbPlayerBatterId].update({'last_at_bat_ball_in_play': True})
                if ab.mlbBaselineSampleDim > 0:
                    cumulative_stats[ab.mlbPlayerBatterId].update({'last_sample_at_bat_ball_in_play': True})
            else:
                cumulative_stats[ab.mlbPlayerBatterId].update({'last_at_bat_ball_in_play': False})
                if ab.mlbBaselineSampleDim > 0:
                    cumulative_stats[ab.mlbPlayerBatterId].update({'last_sample_at_bat_ball_in_play': False})

            cumulative_stats[ab.mlbPlayerBatterId]['delta_swings_to_ball_in_play'] = cumulative_stats[ab.mlbPlayerBatterId]['swings_to_ball_in_play'] - cumulative_stats[ab.mlbPlayerBatterId]['sample_swings_to_ball_in_play']

            # Swings to Line Drive
            if cumulative_stats[ab.mlbPlayerBatterId]['last_at_bat_line_drive']:
                cumulative_stats[ab.mlbPlayerBatterId].update({'swings_to_line_drive': 0})
            if ab.mlbBaselineSampleDim > 0 and cumulative_stats[ab.mlbPlayerBatterId]['last_sample_at_bat_line_drive']:
                cumulative_stats[ab.mlbPlayerBatterId].update({'sample_swings_to_line_drive': 0})

            cumulative_stats[ab.mlbPlayerBatterId]['swings_to_line_drive'] += ab.swings
            if ab.mlbBaselineSampleDim > 0:
                cumulative_stats[ab.mlbPlayerBatterId]['sample_swings_to_line_drive'] += ab.swings

            if ab.lineDrive > 0:
                cumulative_stats[ab.mlbPlayerBatterId].update({'last_at_bat_line_drive': True})
                if ab.mlbBaselineSampleDim > 0:
                    cumulative_stats[ab.mlbPlayerBatterId].update({'last_sample_at_bat_line_drive': True})
            else:
                cumulative_stats[ab.mlbPlayerBatterId].update({'last_at_bat_line_drive': False})
                if ab.mlbBaselineSampleDim > 0:
                    cumulative_stats[ab.mlbPlayerBatterId].update({'last_sample_at_bat_line_drive': False})

            cumulative_stats[ab.mlbPlayerBatterId]['delta_swings_to_line_drive'] = cumulative_stats[ab.mlbPlayerBatterId]['swings_to_line_drive'] - cumulative_stats[ab.mlbPlayerBatterId]['sample_swings_to_line_drive']

            f = AtBat(
                dateId=ab.dateId,
                mlbPlayerBatterId=ab.mlbPlayerBatterId,
                mlbPlayerPitcherId=ab.mlbPlayerPitcherId,
                mlbSampleDim=ab.mlbSampleDim,
                mlbBaselineSampleDim=ab.mlbBaselineSampleDim,
                swingsToBallInPlay=cumulative_stats[ab.mlbPlayerBatterId]['swings_to_ball_in_play'],
                swingsToLineDrive=cumulative_stats[ab.mlbPlayerBatterId]['swings_to_line_drive'],
                sampleSwingsToBallInPlay=cumulative_stats[ab.mlbPlayerBatterId]['sample_swings_to_ball_in_play'],
                sampleSwingsToLineDrive=cumulative_stats[ab.mlbPlayerBatterId]['sample_swings_to_line_drive'],
                deltaSwingsToBallInPlay=cumulative_stats[ab.mlbPlayerBatterId]['delta_swings_to_ball_in_play'],
                deltaSwingsToLineDrive=cumulative_stats[ab.mlbPlayerBatterId]['delta_swings_to_line_drive']
            )

            connection.session.add(f)
            connection.block_flush()

    connection.session.commit()