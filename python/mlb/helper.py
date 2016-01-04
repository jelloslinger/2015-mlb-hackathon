# -*- coding: utf-8 -*-


class BaselineSampleManager(object):

    def __init__(self):
        self._baseline_counter = 0
        self._current_game_id = 0
        self._manager = {
            'B': {
                'baseline_sample_number': 0,
                'batter_ids': [],
                'pitcher_ids': [],
                'facts': []
            },
            'T': {
                'baseline_sample_number': 0,
                'batter_ids': [],
                'pitcher_ids': [],
                'facts': []
            },
        }
        self.side = 'T'
        self.fact = None

    @property
    def baseline_sample_number(self):
        return self._manager[self.side]['baseline_sample_number']

    @property
    def facts(self):
        return self._manager[self.side]['facts']

    @facts.setter
    def facts(self, x):
        self._manager[self.side]['facts'] = x

    @property
    def last_batter_id(self):
        if len(self._manager[self.side]['batter_ids']):
            return self._manager[self.side]['batter_ids'][-1]
        return 0

    @property
    def last_pitcher_id(self):
        if len(self._manager[self.side]['pitcher_ids']):
            return self._manager[self.side]['pitcher_ids'][-1]
        return 0

    @property
    def other_side(self):
        return 'B' if self.side == 'T' else 'T'

    def add(self):

        self._current_game_id = self.fact['mlbGameId']
        if self.fact['mlbPlayerBatterId'] not in self._manager[self.side]['batter_ids']:
            self._manager[self.side]['batter_ids'].append(self.fact['mlbPlayerBatterId'])
        if self.fact['mlbPlayerPitcherId'] not in self._manager[self.side]['pitcher_ids']:
            self._manager[self.side]['pitcher_ids'].append(self.fact['mlbPlayerPitcherId'])

        self.facts.append(self.fact)

    def is_game_finished(self):
        if 'mlbGameId' in self.fact:
            return self._current_game_id != self.fact['mlbGameId']
        return True

    def is_pitcher_finished(self):
        if 'mlbPlayerPitcherId' in self.fact:
            return self.last_pitcher_id != self.fact['mlbPlayerPitcherId']
        return True

    def is_sample_finished(self):
        if len(self._manager[self.side]['batter_ids']) >= 9 and self.last_batter_id != self.fact['mlbPlayerBatterId']:
            return True
        return False

    def reset(self):
        if self.is_sample_finished() or self.is_game_finished() or self.is_pitcher_finished():
            self._baseline_counter += 1
            self._manager[self.side]['baseline_sample_number'] = self._baseline_counter
            self._manager[self.side]['batter_ids'] = []
            if self.is_game_finished():
                self._manager[self.side]['pitcher_ids'] = []
                self._manager[self.other_side]['batter_ids'] = []
                self._manager[self.other_side]['pitcher_ids'] = []

    def zero_baseline_sample(self):
        for x in self._manager[self.side]['facts']:
            x.update({'mlbBaselineSampleDim': 0})