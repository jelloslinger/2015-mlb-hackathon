# -*- coding: utf-8 -*-

import datetime

from datapro.framework.db import OrmConnection
from mlb import BATTED_BALL_TYPE, BATTED_BALL_ANGLES, BATTED_BALL_DISTANCES, PA_RESULT, PITCH_RESULT, PITCH_TYPE
from mlb.model import *


def init(connection):

    # Dimension Tables
    Game.__table__.create(connection.engine, checkfirst=True)
    Outcome.__table__.create(connection.engine, checkfirst=True)
    Player.__table__.create(connection.engine, checkfirst=True)
    Situation.__table__.create(connection.engine, checkfirst=True)

    # Fact Tables
    PitchByPitch.__table__.create(connection.engine, checkfirst=True)
    AtBat.__table__.create(connection.engine, checkfirst=True)

    if len([row for row in connection.session.query(Game).limit(1)]) == 0:
        connection.session.execute("SET SESSION sql_mode='NO_AUTO_VALUE_ON_ZERO'")
        connection.session.add(
            Game(
                id=0,
                gameIdentifier='None',
                gameDatetime=datetime.datetime(1970, 1, 1),
                gameType='XX',
                visitor='UN',
                visitorLong='Unknown',
                home='UN',
                homeLong='Unknown'
            )
        )

    if len([row for row in connection.session.query(Outcome).limit(1)]) == 0:
        for par_key, par_value in iter(PA_RESULT.items()):
            for bbt_key, bbt_value in iter(BATTED_BALL_TYPE.items()):
                for bba in BATTED_BALL_ANGLES:
                    for bbd in BATTED_BALL_DISTANCES:
                        connection.session.add(
                            Outcome(
                                paResult=par_key,
                                paResultDescription=par_value,
                                battedBallType=bbt_key,
                                battedBallTypeDescription=bbt_value,
                                battedBallAngleDescription=bba,
                                battedBallDistanceDescription=bbd
                            )
                        )

    if len([row for row in connection.session.query(Player).limit(1)]) == 0:
        connection.session.execute("SET SESSION sql_mode='NO_AUTO_VALUE_ON_ZERO'")
        connection.session.add(
            Player(
                id=0,
                playerIdentifier=0,
                playerName='Unknown',
                teamAbbreviation='UN',
                teamFullName='Unknown'
            )
        )

    if len([row for row in connection.session.query(Situation).limit(1)]) == 0:
        connection.session.execute("SET SESSION sql_mode='NO_AUTO_VALUE_ON_ZERO'")
        connection.session.add(
            Situation(
                numberBalls=0,
                numberStrikes=0,
                numberOuts=0,
                pitchType='UN',
                pitchTypeDescription='Unknown',
                pitchResult='UK',
                pitchResultDescription='Unknown'
            )
        )

        for nb in range(0, 4):
            for ns in range(0, 3):
                for no in range(0, 4):
                    for pr_key, pr_value in iter(PITCH_RESULT.items()):
                        for pt_key, pt_value in iter(PITCH_TYPE.items()):
                            connection.session.add(
                                Situation(
                                    numberBalls=nb,
                                    numberStrikes=ns,
                                    numberOuts=no,
                                    pitchType=pt_key,
                                    pitchTypeDescription=pt_value,
                                    pitchResult=pr_key,
                                    pitchResultDescription=pr_value
                                )
                            )

    connection.session.commit()


if __name__ == '__main__':

    init(OrmConnection('common'))
