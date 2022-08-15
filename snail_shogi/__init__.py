
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

from Pieces import*

k = '\n'

class Board:
    def __init__(self, sfen=None):
        self.hand_piece_index_dict = {'P': 0, 'L': 1, 'N': 2, 'S': 3, 'G': 4, 'B': 5, 'R': 6}
        self.hand_piece_index_dict2 = {v: k for k, v in self.hand_piece_index_dict.items()}
        self.piece_to_class = {'P': Pawn, 'L': Lance, 'N': Knight, 'S': Silver, 'G': Gold,
                                        'B': Bishop, 'R': Rook, 'K': King,
                                        '+P': Promotion_Pawn, '+L': Promotion_Lance,
                                        '+N': Promotion_Knight, '+S': Promotion_Silver,
                                        '+B': Promotion_Bishop, '+R': Promotion_Rook}
        self.piece_black_to_white = {'P': 'p', 'L': 'l', 'N': 'n', 'S': 's', 'G': 'g', 'B': 'b', 'R': 'r', 'K': 'k',
                                                   '+P': '+p', '+L': '+l', '+N': '+n', '+S': '+s', '+B': '+b', '+R': '+r'}
        self.piece_white_to_black = {v: k for k, v in self.piece_black_to_white.items()}
        self.color_change_dict = {BLACK: WHITE, WHITE: BLACK}
        
        self.init_board()
        if sfen == None:
            self.set_startpos()
        else:
            self.set_sfen(sfen)
        self.board_history = [self.return_sfen()]

    def __str__(self):
        output = ''
        index = 0
        for y in range(9):
            for x in range(9):
                sq = self.pieces[y][x]
                if sq == None:
                    output += '[     ]'
                else:
                    output += sq.symbol['normal']
                index += 1
            output += k
        output += ('Black:' + str(self.pieces_in_hand[0]) + k)
        output += ('White:' + str(self.pieces_in_hand[1]) + k)
        return output

    def copy(self):
        copy_board = Board(sfen=self.return_sfen())
        return

    def init_board(self):
        self.squares = []
        self.pieces = []
        self.pieces_in_hand = [[0] * 7, [0] * 7]
        self.black_pawn_file = [0] * 9
        self.white_pawn_file = [0] * 9
        self.king_square = {'black': [0, 0], 'white': [0, 0]}
        for y in range(9):
            rank = []
            pieces_rank = []
            for x in range(9):
                rank.append(Square())
                pieces_rank.append(None)
                if y in [6, 7, 8]:
                    rank[x].is_white_promotable_square  = True
                if y in [0, 1, 2]:
                    rank[x].is_black_promotable_square = True
            self.squares.append(rank)
            self.pieces.append(pieces_rank)
        return

    def set_startpos(self):
        b = BLACK
        w = WHITE
        self.pieces = [[Lance(w), Knight(w), Silver(w), Gold(w), King(w), Gold(w), Silver(w), Knight(w), Lance(w)],
                             [None, Rook(w), None, None, None, None, None, Bishop(w), None],
                             [Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w)],
                             [None] * 9,
                             [None] * 9,
                             [None] * 9,
                             [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)],
                             [None, Bishop(b), None, None, None, None, None, Rook(b), None],
                             [Lance(b), Knight(b), Silver(b), Gold(b), King(b), Gold(b), Silver(b), Knight(b), Lance(b)]]
        self.black_pawn_file = [1] * 9
        self.white_pawn_file = [1] * 9
        self.king_square = {'black': [8, 4], 'white': [0, 4]}
        self.turn = BLACK
        self.update_pawn_file()
        return

    def set_sfen(self, sfen):
        sfen = sfen.split(' ')
        ind = 0
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        promoted = False
        for i in range(len(sfen[0])):
            if sfen[0][i] in numbers:
                ind += int(sfen[0][i])
            else:
                if sfen[0][i] != '/':
                    if sfen[0][i] == '+':
                        promoted = True
                    else:
                        if promoted:
                            key = '+' + sfen[0][i]
                            if key in self.piece_to_class.keys():
                                self.pieces[ind // 9][ind % 9] = self.piece_to_class[key](BLACK)
                            else:
                                key = '+' + self.piece_white_to_black[sfen[0][i]]
                                self.pieces[ind // 9][ind % 9] = self.piece_to_class[key](WHITE)
                            promoted = False
                        else:
                            key = sfen[0][i]
                            if key in self.piece_to_class.keys():
                                self.pieces[ind // 9][ind % 9] = self.piece_to_class[key](BLACK)
                                if key == 'K':
                                    self.king_square['black'] = [ind // 9, ind % 9]
                            else:
                                key = self.piece_white_to_black[sfen[0][i]]
                                self.pieces[ind // 9][ind % 9] = self.piece_to_class[key](WHITE)
                                if key == 'K':
                                    self.king_square['white'] = [ind // 9, ind % 9]
                            promoted = False
                        ind += 1
        if sfen[1] == 'b':
            self.turn = BLACK
        else:
            self.turn = WHITE
        for i in range(len(sfen[2])):
            if sfen[2] == '-':
                break
            if sfen[2][i] in numbers:
                continue
            if sfen[2][i] in self.hand_piece_index_dict.keys():
                piece_num = 1
                if i > 0 and sfen[2][i - 1] in numbers:
                    piece_num = int(sfen[2][i - 1])
                self.pieces_in_hand[0][self.hand_piece_index_dict[sfen[2][i]]] = piece_num
            elif self.piece_white_to_black[sfen[2][i]] in self.hand_piece_index_dict.keys():
                piece_num = 1
                if i > 0 and sfen[2][i - 1] in numbers:
                    piece_num = int(sfen[2][i - 1])
                self.pieces_in_hand[1][self.hand_piece_index_dict[self.piece_white_to_black[sfen[2][i]]]] = piece_num
        self.update_pawn_file()
        return

    def return_sfen(self):
        sfen = ''
        for y in range(9):
            c = 0
            for x in range(9):
                piece = self.pieces[y][x]
                if piece != None:
                    if c > 0:
                        sfen += str(c)
                    c = 0
                    if piece.color == BLACK:
                        sfen += {'pawn': 'P', 'lance': 'L', 'knight': 'N', 'silver': 'S', 'gold': 'G',
                                     'bishop': 'B', 'rook': 'R', 'king': 'K',
                                     'pawn+': '+P', 'lance+': '+L', 'knight+': '+N', 'silver+': '+S',
                                     'bishop+': '+B', 'rook+': '+R'}[piece.name]
                    else:
                        sfen += {'pawn': 'p', 'lance': 'l', 'knight': 'n', 'silver': 's', 'gold': 'g',
                                     'bishop': 'b', 'rook': 'r', 'king': 'k',
                                     'pawn+': '+p', 'lance+': '+l', 'knight+': '+n', 'silver+': '+s',
                                     'bishop+': '+b', 'rook+': '+r'}[piece.name]
                else:
                    c += 1
            if c > 0:
                sfen += str(c)
            if y not in [8]:
                sfen += '/'
        sfen += ' ' + {BLACK: 'b', WHITE: 'w'}[self.turn]
        hand = ''
        for i in range(7):
            if self.pieces_in_hand[0][i] > 0:
                hand += (str(self.pieces_in_hand[0][i]) + self.hand_piece_index_dict2[i])
        for i in range(7):
            if self.pieces_in_hand[1][i] > 0:
                hand += (str(self.pieces_in_hand[1][i]) + self.piece_black_to_white[self.hand_piece_index_dict2[i]])
        if len(hand) > 1:
            sfen += (' ' + hand + ' ')
        else:
            sfen += ' - '
        sfen += '1'
        return sfen

    def change_turn(self):
        self.turn = {BLACK: WHITE, WHITE: BLACK}[self.turn]
        return

    def usi_to_index(self, usi):
        d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        return [d[usi[1]], 9 - int(usi[0])]

    def index_to_usi(self, index):
        d = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
        return str(9 - int(index[1])) + d[index[0]]

    def move_to_usi(self, move):
        if move['from'] == 'hand':
            d = {0: 'P', 1: 'L', 2: 'N', 3: 'S', 4: 'G', 5: 'B', 6: 'R'}
            return d[move['hand_piece_index']] + '*' + self.index_to_usi(move['to'])
        usimove = self.index_to_usi(move['from']) + self.index_to_usi(move['to'])
        if move['+']:
            usimove += '+'
        return usimove

    def move_from_usi(self, usimove):
        if '*' in usimove:
            move = {'from': 'hand', 'to': self.usi_to_index(usimove[2:4]),
                         '+': False, 'hand_piece_index': self.hand_piece_index_dict[usimove[0]]}
            return move
        move = {'from': self.usi_to_index(usimove[0:2]),
                     'to': self.usi_to_index(usimove[2:4]),
                     '+': False}
        if '+' in usimove:
            move['+'] = True
        return move

    def return_route(self, move):
        """
        moveを受け取って、移動経路を返す
        """
        from_sq = move['from']
        to_sq = move['to']
        output = []
        if from_sq[0] == to_sq[0]:#横移動
            if from_sq[1] > to_sq[1]:
                for i in range(1, from_sq[1] - to_sq[1]):
                    output.append((to_sq[0], to_sq[1] + i))
            else:
                for i in range(1, to_sq[1] - from_sq[1]):
                    output.append((from_sq[0], from_sq[1] + i))
                    
        elif from_sq[1] == to_sq[1]:#縦移動
            if from_sq[0] > to_sq[0]:
                for i in range(1, from_sq[0] - to_sq[0]):
                    output.append((to_sq[0] + i, to_sq[1]))
            else:
                for i in range(1, to_sq[0] - from_sq[0]):
                    output.append((from_sq[0] + i, from_sq[1]))
        
        else:#斜め移動
            if to_sq[0] > from_sq[0] and to_sq[1] > from_sq[1]:#右斜め下
                for i in range(1, to_sq[0] - from_sq[0]):
                    output.append((from_sq[0] + i, from_sq[1] + i))
                    
            elif to_sq[0] > from_sq[0] and to_sq[1] < from_sq[1]:#左斜め下
                for i in range(1, to_sq[0] - from_sq[0]):
                    output.append((from_sq[0] + i, from_sq[1] - i))
                    
            elif to_sq[0] < from_sq[0] and to_sq[1] > from_sq[1]:#右斜め上
                for i in range(1, from_sq[0] - to_sq[0]):
                    output.append((from_sq[0] - i, from_sq[1] + i))
            else:#左斜め上
                for i in range(1, from_sq[0] - to_sq[0]):
                    output.append((from_sq[0] - i, from_sq[1] - i))
        return output

    def is_legal_pseudo(self, move):
        #第一段階: 移動元が空白または、
        #手番側の駒では無いなら、illegalを返す(ただし、持ち駒を打つ場合は手駒が存在するかの確認のみ行う)
        index = move['from']
        if index == 'hand':
            if self.turn == BLACK:
                num = self.pieces_in_hand[0][move['hand_piece_index']]
            else:
                num = self.pieces_in_hand[1][move['hand_piece_index']]
            if num == 0:
                return False
        else:
            move_piece = self.pieces[index[0]][index[1]]
            if move_piece == None:
                return False
            if move_piece.color != self.turn:
                return False
        #第二段階: 移動先が盤面の外　
        #もしくは、駒が成る手なのに移動元・移動先の両方とも成れない場所の場合は
        #illegalを返す
        index = move['to']
        if min(index) < 0 or max(index) > 8:
            return False
        if move.get('+'):
            sq = self.squares[index[0]][index[1]]
            sq2 = self.squares[move['from'][0]][move['from'][1]]
            if self.turn == BLACK:
                if (not sq.is_black_promotable_square) and (not sq2.is_black_promotable_square):
                    return False
            else:
                if (not sq.is_white_promotable_square) and (not sq2.is_white_promotable_square):
                    return False
        #第三段階: 移動先が味方の駒　もしくは、
        #持ち駒を打つ先に駒があるなら、
        #illegalを返す
        if move['from'] == 'hand':
            piece = self.pieces[index[0]][index[1]]
            if piece != None:
                return False
        else:
            piece = self.pieces[index[0]][index[1]]
            if piece != None and piece.color == move_piece.color:
                return False
        #第四段階: 移動先のマスが、移動するコマの(障害物がない場合の)移動可能範囲とかぶってない場合はillegalを返す
        #(持ち駒を打つ場合はスキップ)
        if move['from'] == 'hand':
            pass
        else:
            for i in range(len(move_piece.attack_squares) + 1):
                if i == len(move_piece.attack_squares):
                    return False
                index = [move['from'][0] + move_piece.attack_squares[i][0],
                             move['from'][1] + move_piece.attack_squares[i][1]]
                if move['to'][0] == index[0] and move['to'][1] == index[1]:
                    break
        #第五段階: 通常moveは間に駒がいるかどうか調べる(ただし、桂馬は例外)
        #持ち駒を打つ手は二歩チェックをする
        if move['from'] != 'hand':
            if move_piece.name == 'knight':
                pass
            else:
                route_squares = self.return_route(move)
                for sq in route_squares:
                    if self.pieces[sq[0]][sq[1]] != None:#障害物あり
                        return False
        elif self.is_double_pawn(move):
            return False
        return True

    def cannot_move_piece(self, move):
        target_piece = ['P', 'L', 'N']
        if move['from'] == 'hand':
            index = move['hand_piece_index']
            piece = self.piece_to_class[self.hand_piece_index_dict2[index]](self.turn)
        else:
            piece = self.pieces[move['from'][0]][move['from'][1]]
        if piece.name not in ['pawn', 'lance', 'knight']:
            return False
        if move.get('+'):
            return False
        
        if move['to'][0] == 0 and self.turn == BLACK:
            return True
        if move['to'][0] <= 1 and self.turn == BLACK and piece.name == 'knight':
            return True
        if move['to'][0] == 8 and self.turn == WHITE:
            return True
        if move['to'][0] >= 7 and self.turn == WHITE and piece.name == 'knight':
            return True
        return False

    def is_drop_pawn_checkmate(self, move):
        if move['from'] != 'hand':
            return False
        index = move['hand_piece_index']
        piece = self.piece_to_class[self.hand_piece_index_dict2[index]](self.turn)
        if piece.name != 'pawn':
            return False
        self.push(move)
        if self.is_gameover():
            self.pop()
            return True
        self.pop()
        return False

    def is_legal(self, move):
        if not self.is_legal_pseudo(move):
            return False
        #is_legal_pseudoの続き
        #第六段階: 行き場のない駒のチェック
        if self.cannot_move_piece(move):
            return False
        #第六段階: 自殺手チェック
        if self.is_suicide_move(move):
            return False
        #第七段階:  打ち歩詰めチェック
        if self.is_drop_pawn_checkmate(move):
            return False
        return True

    def gen_candidate_moves(self):
        moves =[]
        for y in range(9):
            for x in range(9):
                piece = self.pieces[y][x]
                if piece == None or piece.color != self.turn:
                    pass
                else:
                    for i in range(len(piece.attack_squares)):
                        index =  (y + piece.attack_squares[i][0],
                                     x + piece.attack_squares[i][1])
                        moves.append({'from': (y, x), 'to': index, '+': False})
                        moves.append({'from': (y, x), 'to': index, '+': True})
        piece_list = ['P', 'L', 'N', 'S' 'G', 'B', 'R']
        ind = 0
        for p in piece_list:
            if self.pieces_in_hand[{BLACK: 0, WHITE: 1}[self.turn]][ind] > 0:
                for j in range(9):
                    for k in range(9):
                        moves.append({'from': 'hand', 'to': (j, k), 'hand_piece_index': ind})
            ind += 1
        return moves

    def gen_legal_moves(self):
        candidate_moves = self.gen_candidate_moves()
        legal_moves = []
        for i in range(len(candidate_moves)):
            if self.is_legal(candidate_moves[i]):
                legal_moves.append(self.move_to_usi(candidate_moves[i]))
        return list(set(legal_moves))

    def is_double_pawn(self, move):
        if move['from'] != 'hand':
            return False
        if move['hand_piece_index'] != 0:
            return False
        if self.turn == BLACK and self.black_pawn_file[move['to'][1]] == 1:
            return True
        elif self.turn == WHITE and self.white_pawn_file[move['to'][1]] == 1:
            return True
        return False

    def is_suicide_move(self, move):
        self.push(move)
        self.change_turn()
        is_suicide = self.is_check()
        self.change_turn()
        self.pop()
        return is_suicide

    def update_pawn_file(self):
        self.black_pawn_file = [0] * 9
        self.white_pawn_file = [0] * 9
        for y in range(9):
            for x in range(9):
                piece = self.pieces[y][x]
                if piece != None and piece.name == 'pawn':
                    if piece.color == BLACK:
                        self.black_pawn_file[x] = 1
                    else:
                        self.white_pawn_file[x] = 1
        return
                        
    def push(self, move):
        if move['from'] == 'hand':
            index = move['hand_piece_index']
            piece = self.piece_to_class[self.hand_piece_index_dict2[index]]
            self.pieces[move['to'][0]][move['to'][1]] = piece(self.turn)
            if self.turn == BLACK:
                self.pieces_in_hand[0][index] -= 1
            else:
                self.pieces_in_hand[1][index] -= 1
        else:
            piece = self.pieces[move['from'][0]][move['from'][1]]
            to_sq = self.pieces[move['to'][0]][move['to'][1]]
            if to_sq != None:
                index = self.hand_piece_index_dict[to_sq.in_hand]
                if self.turn == BLACK:
                    self.pieces_in_hand[0][index] += 1
                else:
                    self.pieces_in_hand[1][index] += 1
            if move.get('+'):
                self.pieces[move['to'][0]][move['to'][1]] = promotion_dict[piece.name](self.turn)
            else:
                self.pieces[move['to'][0]][move['to'][1]] = piece
            if piece.name == 'king':
                if self.turn == BLACK:
                    self.king_square['black'] = move['to']
                else:
                    self.king_square['white'] = move['to']
            self.pieces[move['from'][0]][move['from'][1]] = None
        self.update_pawn_file()
        self.change_turn()
        self.board_history.append(self.return_sfen())
        return

    def push_usi(self, move):
        move = self.move_from_usi(move)
        self.push(move)
        return

    def pop(self):
        self.board_history.pop(-1)
        self.init_board()
        self.set_sfen(self.board_history[-1])
        return

    def return_attack_square(self, color):
        """
        color側が攻撃しているマスを返す
        """
        attack_square = []
        color_backup = self.turn
        self.turn = color
        for y in range(9):
            for x in range(9):
                piece = self.pieces[y][x]
                if piece == None or piece.color != color:
                    pass
                else:
                    for i in range(len(piece.attack_squares)):
                        index =  (y + piece.attack_squares[i][0],
                                     x + piece.attack_squares[i][1])
                        move = {'from': (y,x), 'to': index, '+': False}
                        if index not in attack_square and self.is_legal_pseudo(move):
                            attack_square.append(index)
        self.turn = color_backup
        return attack_square

    def is_check(self):
        color = {BLACK: 'black', WHITE: 'white'}[self.turn]
        king_sq = self.king_square[color]
        check = False
        attack_square = self.return_attack_square(self.color_change_dict[self.turn])
        for sq in attack_square:
            if sq[0] == king_sq[0] and sq[1] == king_sq[1]:
                check = True
                break
        return check

    def is_gameover(self):
        return len(self.gen_legal_moves()) == 0
