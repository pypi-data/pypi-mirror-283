class Checkers():
    def __init__(self):
        self.chess = {
            'A1': Cell('B'),
            'A2': Cell('X'),
            'A3': Cell('B'),
            'A4': Cell('X'),
            'A5': Cell('X'),
            'A6': Cell('X'),
            'A7': Cell('W'),
            'A8': Cell('X'),

            'B1': Cell('X'),
            'B2': Cell('B'),
            'B3': Cell('X'),
            'B4': Cell('X'),
            'B5': Cell('X'),
            'B6': Cell('W'),
            'B7': Cell('X'),
            'B8': Cell('W'),

            'C1': Cell('B'),
            'C2': Cell('X'),
            'C3': Cell('B'),
            'C4': Cell('X'),
            'C5': Cell('X'),
            'C6': Cell('X'),
            'C7': Cell('W'),
            'C8': Cell('X'),

            'D1': Cell('X'),
            'D2': Cell('B'),
            'D3': Cell('X'),
            'D4': Cell('X'),
            'D5': Cell('X'),
            'D6': Cell('W'),
            'D7': Cell('X'),
            'D8': Cell('W'),

            'E1': Cell('B'),
            'E2': Cell('X'),
            'E3': Cell('B'),
            'E4': Cell('X'),
            'E5': Cell('X'),
            'E6': Cell('X'),
            'E7': Cell('W'),
            'E8': Cell('X'),

            'F1': Cell('X'),
            'F2': Cell('B'),
            'F3': Cell('X'),
            'F4': Cell('X'),
            'F5': Cell('X'),
            'F6': Cell('W'),
            'F7': Cell('X'),
            'F8': Cell('W'),

            'G1': Cell('B'),
            'G2': Cell('X'),
            'G3': Cell('B'),
            'G4': Cell('X'),
            'G5': Cell('X'),
            'G6': Cell('X'),
            'G7': Cell('W'),
            'G8': Cell('X'),

            'H1': Cell('X'),
            'H2': Cell('B'),
            'H3': Cell('X'),
            'H4': Cell('X'),
            'H5': Cell('X'),
            'H6': Cell('W'),
            'H7': Cell('X'),
            'H8': Cell('W'),
        }

    def move(self, f, t):
        self.chess[t] = self.chess[f]
        self.chess[f] = Cell('X')

    def get_cell(self,p):
        return self.chess[p]

#W —белая шашка, B — чёрная шашка, X — пустая клетка

class Cell():
    def __init__(self, condition):
        self.condition = condition

    def status(self):
        return self.condition




# my_chess = Checkers()
#
# my_chess.move("A1", "B2")
#
#
#
# for row in '87654321':
#     for col in 'ABCDEFGH':
#         print(my_chess.get_cell(col + row).status(), end='')
#     print()
