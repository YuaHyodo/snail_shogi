
"""
This file is part of snail_shogi

Copyright (c) 2022 YuaHyodo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from Piece_base import Piece_base as base

BLACK = True
WHITE = False

#よく使う効き
Gold_attack_squares_black = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0))
Gold_attack_squares_white = ((1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, 0))

class Square:
    def __init__(self):
        self.symbol = {'simple': '[ ]', 'normal': '[  ]'}
        self.is_black_promotable_square = False
        self.is_white_promotable_square = False

class Pawn(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'pawn'
        if color == BLACK:
            self.attack_squares = ((-1, 0),)
            self.symbol['simple'] = '[P]'
            self.symbol['normal'] = '[A歩]'
        else:
            self.attack_squares = ((1, 0),)
            self.symbol['simple'] = '[p]'
            self.symbol['normal'] = '[V歩]'
        self.color = color
        self.is_promotion = False
        self.is_promotable = True
        self.in_hand = 'P'

class Lance(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'lance'
        if color == BLACK:
            self.attack_squares = ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0), (-9, 0))
            self.symbol['simple'] = '[L]'
            self.symbol['normal'] = '[A香]'
        else:
            self.attack_squares = ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0))
            self.symbol['simple'] = '[ l ]'
            self.symbol['normal'] = '[V香]'
        self.color = color
        self.is_promotion = False
        self.is_promotable = True
        self.in_hand = 'L'

class Knight(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'knight'
        if color == BLACK:
            self.attack_squares = ((-2, -1), (-2, 1))
            self.symbol['simple'] = '[N]'
            self.symbol['normal'] = '[A桂]'
        else:
            self.attack_squares = ((2, -1), (2, 1))
            self.symbol['simple'] = '[n]'
            self.symbol['normal'] = '[V桂]'
        self.color = color
        self.is_promotion = False
        self.is_promotable = True
        self.in_hand = 'N'

class Silver(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'silver'
        if color == BLACK:
            self.attack_squares = ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 1))
            self.symbol['simple'] = '[S]'
            self.symbol['normal'] = '[A銀]'
        else:
            self.attack_squares = ((1, -1), (1, 0), (1, 1), (-1, -1), (-1, 1))
            self.symbol['simple'] = '[s]'
            self.symbol['normal'] = '[V銀]'
        self.color = color
        self.is_promotion = False
        self.is_promotable = True
        self.in_hand = 'S'

class Gold(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'gold'
        if color == BLACK:
            self.attack_squares = Gold_attack_squares_black
            self.symbol['simple'] = '[G]'
            self.symbol['normal'] = '[A金]'
        else:
            self.attack_squares = Gold_attack_squares_white
            self.symbol['simple'] = '[ g ]'
            self.symbol['normal'] = '[V金]'
        self.color = color
        self.is_promotion = False
        self.is_promotable = False
        self.in_hand = 'G'

class Bishop(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'bishop'
        self.attack_squares = ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), (-8, -8),
                                        (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (-8, 8),
                                        (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (8, -8),
                                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8))
        self.color = color
        if color == BLACK:
            self.symbol['simple'] = '[B]'
            self.symbol['normal'] = '[A角]'
        else:
            self.symbol['simple'] = '[ b ]'
            self.symbol['normal'] = '[V角]'
        self.is_promotion = False
        self.is_promotable = True
        self.in_hand = 'B'

class Rook(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'rook'
        self.attack_squares = ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0),
                                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                                          (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (0, -8),
                                          (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8))
        self.color = color
        if color == BLACK:
            self.symbol['simple'] = '[R]'
            self.symbol['normal'] = '[A飛]'
        else:
            self.symbol['simple'] = '[ r ]'
            self.symbol['normal'] = '[V飛]'
        self.is_promotion = False
        self.is_promotable = True
        self.in_hand = 'R'

class King(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'king'
        self.attack_squares = ((-1, -1), (-1, 0), (-1, 1), (-1, 0), (1, 0), (1, -1), (1, 0), (1, 1))
        self.color = color
        if color == BLACK:
            self.symbol['simple'] = '[K]'
            self.symbol['normal'] = '[A玉]'
        else:
            self.symbol['simple'] = '[ k ]'
            self.symbol['normal'] = '[V玉]'
        self.is_promotion = False
        self.is_promotable = False
        self.in_hand = 'K'

class Promotion_Pawn(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'pawn+'
        if color == BLACK:
            self.attack_squares = Gold_attack_squares_black
            self.symbol['simple'] = '[+P]'
            self.symbol['normal'] = '[A+歩]'
        else:
            self.attack_squares = Gold_attack_squares_white
            self.symbol['simple'] = '[+p ]'
            self.symbol['normal'] = '[V+歩]'
        self.color = color
        self.is_promotion = True
        self.is_promotable = False
        self.in_hand = 'P'

class Promotion_Lance(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'lance+'
        if color == BLACK:
            self.attack_squares = Gold_attack_squares_black
            self.symbol['simple'] = '[+L]'
            self.symbol['normal'] = '[A+香]'
        else:
            self.attack_squares = Gold_attack_squares_white
            self.symbol['simple'] = '[+ l ]'
            self.symbol['normal'] = '[V+香]'
        self.color = color
        self.is_promotion = True
        self.is_promotable = False
        self.in_hand = 'L'

class Promotion_Knight(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'knight+'
        if color == BLACK:
            self.attack_squares = Gold_attack_squares_black
            self.symbol['simple'] = '[+N]'
            self.symbol['normal'] = '[A+桂]'
        else:
            self.attack_squares = Gold_attack_squares_white
            self.symbol['simple'] = '[+n ]'
            self.symbol['normal'] = '[V+桂]'
        self.color = color
        self.is_promotion = True
        self.is_promotable = False
        self.in_hand = 'N'

class Promotion_Silver(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'silver+'
        if color == BLACK:
            self.attack_squares = Gold_attack_squares_black
            self.symbol['simple'] = '[+S]'
            self.symbol['normal'] = '[A+銀]'
        else:
            self.attack_squares = Gold_attack_squares_white
            self.symbol['simple'] = '[+s ]'
            self.symbol['normal'] = '[V+銀]'
        self.color = color
        self.is_promotion = True
        self.is_promotable = False
        self.in_hand = 'S'

class Promotion_Bishop(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'bishop+'
        self.attack_squares = ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), (-8, -8),
                                        (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7), (-8, 8),
                                        (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (8, -8),
                                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
                                        (-1, 0), (-1, 0), (1, 0), (1, 0))
        self.color = color
        if color == BLACK:
            self.symbol['simple'] = '[+B]'
            self.symbol['normal'] = '[A+角]'
        else:
            self.symbol['simple'] = '[+b ]'
            self.symbol['normal'] = '[V+角]'
        self.is_promotion = True
        self.is_promotable = False
        self.in_hand = 'B'

class Promotion_Rook(base):
    def __init__(self, color):
        super().__init__()
        self.name = 'rook+'
        self.attack_squares = ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0),
                                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                                          (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7), (0, -8),
                                          (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                                          (-1, -1), (-1, 1), (1, -1), (1, 1))
        self.color = color
        if color == BLACK:
            self.symbol['simple'] = '[+R]'
            self.symbol['normal'] = '[A+飛]'
        else:
            self.symbol['simple'] = '[+r ]'
            self.symbol['normal'] = '[V+飛]'
        self.is_promotion = True
        self.is_promotable = False
        self.in_hand = 'R'

promotion_dict = {'pawn': Promotion_Pawn, 'lance': Promotion_Lance, 'knight': Promotion_Knight,
                             'silver': Promotion_Silver, 'bishop': Promotion_Bishop, 'rook': Promotion_Rook}
