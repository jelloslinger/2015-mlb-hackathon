# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.types import *

from datapro import IdMixin, Model


class Game(Model, IdMixin):
    __schema__ = 'common'
    __source__ = 'Mlb'
    __table_type__ = 'DIM'

    gameIdentifier = Column(VARCHAR(64), nullable=False, unique=True)
    gameDatetime = Column(DATETIME, nullable=False)
    gameType = Column(CHAR(4), nullable=False)
    visitor = Column(CHAR(4), nullable=False)
    visitorLong = Column(VARCHAR(64), nullable=False)
    home = Column(CHAR(4), nullable=False)
    homeLong = Column(VARCHAR(64), nullable=False)


class Outcome(Model, IdMixin):
    __schema__ = 'common'
    __source__ = 'Mlb'
    __table_type__ = 'DIM'

    paResult = Column(CHAR(8), nullable=False)
    paResultDescription = Column(VARCHAR(32), nullable=False)
    battedBallType = Column(CHAR(8), nullable=False)
    battedBallTypeDescription = Column(VARCHAR(32), nullable=False)
    battedBallAngleDescription = Column(VARCHAR(16), nullable=False)
    battedBallDistanceDescription = Column(VARCHAR(16), nullable=False)


class Player(Model, IdMixin):
    __schema__ = 'common'
    __source__ = 'Mlb'
    __table_type__ = 'DIM'

    playerIdentifier = Column(INT, nullable=False)
    playerName = Column(VARCHAR(64), nullable=False)
    teamAbbreviation = Column(CHAR(4), nullable=False)
    teamFullName = Column(VARCHAR(32), nullable=False)


class Situation(Model, IdMixin):
    __schema__ = 'common'
    __source__ = 'Mlb'
    __table_type__ = 'DIM'

    numberBalls = Column(SMALLINT, nullable=False)
    numberStrikes = Column(SMALLINT, nullable=False)
    numberOuts = Column(SMALLINT, nullable=False)
    pitchType = Column(CHAR(2), nullable=False)
    pitchTypeDescription = Column(VARCHAR(32), nullable=False)
    pitchResult = Column(CHAR(4), nullable=False)
    pitchResultDescription = Column(VARCHAR(32), nullable=False)

    # TODO - Don't need these yet.  Perhaps covert boolean values to single text field.
    # manOnFirst = Column(BOOLEAN, nullable=False)
    # manOnSecond = Column(BOOLEAN, nullable=False)
    # manOnThird = Column(BOOLEAN, nullable=False)
    # endManOnFirst = Column(BOOLEAN, nullable=False)
    # endManOnSecond = Column(BOOLEAN, nullable=False)
    # endManOnThird = Column(BOOLEAN, nullable=False)

# Going to push this dimension to the player
# class Team(Model, IdMixin):
#     __schema__ = 'common'
#     __source__ = 'Mlb'
#     __table_type__ = 'DIM'
#
#     teamAbbreviation = Column(CHAR(4), nullable=False)
#     teamCity = Column(VARCHAR(16))
#     teamFullName = Column(VARCHAR(32), nullable=False)
#     teamName = Column(CHAR(16))


class PitchByPitch(Model):
    __schema__ = 'common'
    __source__ = 'Mlb'
    __table_type__ = 'FACT'

    dateId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbGameId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbPlayerBatterId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbPlayerPitcherId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbPlayerCatcherId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbSituationId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbOutcomeId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbEventDim = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbSampleDim = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbBaselineSampleDim = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    releaseVelocity = Column(DECIMAL(8, 4))
    spinRate = Column(DECIMAL(8, 4))
    spinDirection = Column(DECIMAL(8, 4))
    px = Column(DECIMAL(8, 4))
    pz = Column(DECIMAL(8, 4))
    szt = Column(DECIMAL(8, 4))
    szb = Column(DECIMAL(8, 4))
    x0 = Column(DECIMAL(8, 4))
    y0 = Column(DECIMAL(8, 4))
    z0 = Column(DECIMAL(8, 4))
    vx0 = Column(DECIMAL(8, 4))
    vy0 = Column(DECIMAL(8, 4))
    vz0 = Column(DECIMAL(8, 4))
    ax = Column(DECIMAL(8, 4))
    ay = Column(DECIMAL(8, 4))
    az = Column(DECIMAL(8, 4))
    battedBallAngle = Column(DECIMAL(8, 4))
    battedBallDistance = Column(DECIMAL(8, 4))
    atBat = Column(SMALLINT, nullable=False)
    plateAppearance = Column(SMALLINT, nullable=False)
    swing = Column(SMALLINT, nullable=False)
    ballInPlay = Column(SMALLINT, nullable=False)
    lineDrive = Column(SMALLINT, nullable=False)
    hit = Column(SMALLINT, nullable=False)
    single = Column(SMALLINT, nullable=False)
    double = Column(SMALLINT, nullable=False)
    triple = Column(SMALLINT, nullable=False)
    homeRun = Column(SMALLINT, nullable=False)
    baseOnBalls = Column(SMALLINT, nullable=False)
    intentionalBaseOnBalls = Column(SMALLINT, nullable=False)
    strikeOut = Column(SMALLINT, nullable=False)


class AtBat(Model):
    __schema__ = 'common'
    __source__ = 'Mlb'
    __table_type__ = 'FACT'

    dateId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbPlayerBatterId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbPlayerPitcherId = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbSampleDim = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    mlbBaselineSampleDim = Column(INTEGER, autoincrement=False, nullable=False, primary_key=True)
    swingsToBallInPlay = Column(INTEGER, nullable=False)
    swingsToLineDrive = Column(INTEGER, nullable=False)
    sampleSwingsToBallInPlay = Column(INTEGER, nullable=False)
    sampleSwingsToLineDrive = Column(INTEGER, nullable=False)
    deltaSwingsToBallInPlay = Column(INTEGER, nullable=False)
    deltaSwingsToLineDrive = Column(INTEGER, nullable=False)
