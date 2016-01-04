# -*- coding: utf-8 -*-

BATTED_BALL_ANGLES = [
    '',
    'Foul Left',
    'Left',
    'Center',
    'Right',
    'Foul Right',
]

BATTED_BALL_DISTANCES = [
    '',
    'Infield',
    'Outfield',
    'Deep Outfield'
]

BATTED_BALL_TYPE = {
    '': '',
    'PU': 'Pop Up',
    'FB': 'Fly Ball',
    'GB': 'Ground Ball',
    'LD': 'Line Drive',
    'BPU': 'Bunt Pop Up',
    'BGB': 'Bunt Ground Ball',
    'UK': 'Unknown'
}

# Reference: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Baseball/Team_abbreviations
MLB_TEAMS = {
    'ANA': 'Anaheim Angels',
    'ARI': 'Arizona Diamondbacks',
    'ATL': 'Atlanta Braves',
    'BAL': 'Baltimore Orioles',
    'BOS': 'Boston Red Sox',
    'BOA': 'Boston Americans',
    'BOB': 'Boston Braves',
    'BOD': 'Boston Doves',
    'BOR': 'Boston Red Sox',
    'BOU': 'Boston Rustlers',
    'BKN': 'Brooklyn Dodgers',
    'CAL': 'California Angels',
    'CHC': 'Chicago Cubs',
    'CHO': 'Chicago Orphans',
    'CHI': 'Chicago Orphans/Colts/White Stockings',
    'CHW': 'Chicago White Sox',
    'CIN': 'Cincinnati Reds',
    'CLE': 'Cleveland Indians',
    'COL': 'Colorado Rockies',
    'CWS': 'Chicago White Sox',
    'DET': 'Detroit Tigers',
    'FLA': 'Florida Marlins',
    'HOU': 'Houston Astros',
    'KC': 'Kansas City Royals',
    'LAA': 'Los Angeles Angels',
    'LAD': 'Los Angeles Dodgers',
    'LA': ' Los Angeles Dodgers',
    'MIA': 'Miami Marlins',
    'MIL': 'Milwaukee Brewers',
    'MIN': 'Minnesota Twins',
    'MTL': 'Montreal Expos',
    'NY': 'New York Yankees',
    'NYG': 'New York Giants/Gothams',
    'NYM': 'New York Mets',
    'NYY': 'New York Yankees',
    'NYH': ' New York Highlanders',
    'OAK': 'Oakland Athletics',
    'PHA': 'Philadelphia Athletics',
    'PHI': 'Philadelphia Phillies',
    'PHP': 'Philadelphia Phillies',
    'PHB': 'Philadelphia Blue Jays',
    'PIT': 'Pittsburgh Pirates',
    'SD': 'San Diego Padres',
    'SEA': 'Seattle Mariners',
    'SF': 'San Francisco Giants',
    'STB': 'St. Louis Browns (AL)',
    'STL': 'St. Louis Cardinals',
    'STC': 'St. Louis Cardinals',
    'TB': 'Tampa Bay Rays',
    'TEX': 'Texas Rangers',
    'TOR': 'Toronto Blue Jays',
    'WSH': 'Washington Nationals',
    'UN': 'Unknown'
}

# Reference: HackathonProjects.pdf
PA_RESULT = {
    '': '',
    'S': 'Single',
    'D': 'Double',
    'T': 'Triple',
    'HR': 'Homerun',
    'BB': 'Walk',
    'IBB': 'Intentional Walk',
    'HBP': 'Hit by Pitch',
    'IP_OUT': 'In Play Out',
    'K': 'Strikeout',
    'FC': 'Fielder\'s Choice',
    'DP': 'Double Play',
    'TP': 'Triple Play',
    'SH': 'Sacrifice Bunt',
    'SF': 'Sacrifice Fly',
    'ROE': 'Reached on Error',
    'SH_ROE': 'Sacrifice Bunt ROE',
    'SF_ROE': 'Sacrifice Fly ROE',
    'BI': 'Batter Interference',
    'CI': 'Catcher Interference',
    'FI': 'Fielder Interference',
    'NO_PLAY': 'No Play',
}

# Reference: HackathonProjects.pdf
PITCH_RESULT = {
    'SS': 'Swinging Strike',
    'SL': 'Strike Looking',
    'F': 'Foul',
    'FT': 'Foul Tip',
    'FB': 'Foul Bunt',
    'MB': 'Missed Bunt',
    'B': 'Ball',
    'BID': 'Ball in Dirt',
    'HBP': 'Hit By Pitch',
    'IB': 'Intentional Ball',
    'PO': 'Pitch Out',
    'IP': 'Ball in Play',
    'AS': 'Automatic Strike',
    'AB': 'Automatic Ball',
    'CI': 'Catcher Interference',
    'UK': 'Unknown'
}

# Reference: HackathonProjects.pdf
PITCH_TYPE = {
    'CH': 'Changeup',
    'CU': 'Curveball',
    'FA': 'Fastball',
    'FT': 'Two Seamer',
    'FF': 'Four Seamer',
    'FC': 'Cutter',
    'SL': 'Slider',
    'FS': 'Splitter',
    'SI': 'Sinker',
    'FO': 'Forkball',
    'KN': 'Knuckleball',
    'KC': 'Knuckle Curve',
    'SC': 'Screwball',
    'GY': 'Gyroball',
    'EP': 'Eephus',
    'PO': 'Pitchout',
    'IN': 'Intentional Ball',
    'AB': 'Automatic Ball',
    'AS': 'Automatic Strike',
    'UN': 'Unknown'
}
