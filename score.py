class Score:

    def __init__(self):
        self.high = 0
        self.score = 0

    def get_score(self):
        return self.score

    def set_score(self, my_score):
        self.score = my_score
        if self.score > self.high:
            self.high = self.score

    def get_high(self):
        return self.high

    def print_scores(self):
        print(f'Scores [High:{self.high}] -- [Score:{self.score}]')
