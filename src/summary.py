from dataclasses import dataclass

@dataclass
class Summary:
    qsos: int = 0
    points: int = 0
    mult1: int = 0
    mult2: int = 0

    def add(self, other):
        self.qsos += other.qsos
        self.points += other.points
        self.mult1 += other.mult1
        self.mult2 += other.mult2

    def add_qso(self, points, mult1, mult2):
        self.qsos += 1
        self.points += points
        self.mult1 += mult1
        self.mult2 += mult2

    def mults(self) -> int:
        return self.mult1 + self.mult2


BANDS = ['160', '80', '40', '20', '15', '10']

MODES = ['CW', 'SSB', 'DIG']
