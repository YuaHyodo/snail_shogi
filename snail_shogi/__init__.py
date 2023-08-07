
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

from .Pieces import*    
from .Piece_base import*

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
        self.piece_name_to_class = {'pawn': Pawn, 'lance': Lance, 'knight': Knight, 'silver': Silver, 'gold': Gold,
                                        'bishop': Bishop, 'rook': Rook, 'king': King,
                                        'pawn+': Promotion_Pawn, 'lance+': Promotion_Lance,
                                        'knight+': Promotion_Knight, 'silver+': Promotion_Silver,
                                        'bishop+': Promotion_Bishop, 'rook+': Promotion_Rook}
        self.piece_black_to_white = {'P': 'p', 'L': 'l', 'N': 'n', 'S': 's', 'G': 'g', 'B': 'b', 'R': 'r', 'K': 'k',
                                                   '+P': '+p', '+L': '+l', '+N': '+n', '+S': '+s', '+B': '+b', '+R': '+r'}
        self.piece_white_to_black = {v: k for k, v in self.piece_black_to_white.items()}
        self.color_change_dict = {BLACK: WHITE, WHITE: BLACK}

        self.king_d = {(i // 9, i % 9): self.return_d((i // 9, i % 9)) for i in range(81)}#マスの座標から同じダイアゴナルにあるマスのlistを取得できる

        self.is_check_memo = {}
        self.generated_legal_moves = {}
        if sfen == None:
            self.set_startpos()
        else:
            self.set_sfen(sfen)
        #self.board_history = [self.return_sfen()]
        self.moves_history = {'startpos': self.return_sfen(), 'moves': []}

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

    def return_d(self, sq):
        """入力されたマスと同じダイアゴナルにあるマスを返す"""
        output = []
        for i in range(1, 9):
            output.append((sq[0] + i, sq[1] + i))
            output.append((sq[0] + i, sq[1] - i))
            output.append((sq[0] - i, sq[1] + i))
            output.append((sq[0] - i, sq[1] - i))
        output = [i for i in output if (min(i) >= 0 and max(i) <= 8)]
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
        self.is_check_memo.clear()
        self.generated_legal_moves.clear()
        return

    def set_startpos(self):
        self.init_board()
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
        self.init_board()
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
                    if sfen[2][i - 1] == '0':
                        piece_num = int(sfen[2][i - 2] + sfen[2][i - 1])
                    else:
                        piece_num = int(sfen[2][i - 1])
                self.pieces_in_hand[0][self.hand_piece_index_dict[sfen[2][i]]] = piece_num
            elif self.piece_white_to_black[sfen[2][i]] in self.hand_piece_index_dict.keys():
                piece_num = 1
                if i > 0 and sfen[2][i - 1] in numbers:
                    if sfen[2][i - 1] == '0':
                        piece_num = int(sfen[2][i - 2] + sfen[2][i - 1])
                    else:
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

    def csamove_to_usi(self, csamove):
        """
        csamoveはCSA形式の指し手。str型
        これはCSA形式の指し手をUSI形式のものに変換するコード
        """
        csa_promoted = ['TO', 'NY', 'NK', 'NG', 'UM', 'RY']
        promote_move = False
        for i in csa_promoted:
            if i in csamove:
                promote_move = True
                break
        usimove = ''
        d = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i'}
        d2 = {'FU': 'P', 'KY': 'L', 'KE': 'N', 'GI': 'S', 'KI': 'G', 'KA': 'B', 'HI': 'R'}
        if csamove[0] == '0':
            usimove += (d2[csamove[-2] + csamove[-1]] + '*')
        else:
            usimove = csamove[0] + d[csamove[1]]
        usimove += (csamove[2] + d[csamove[3]])
        if promote_move:
            #成り駒が移動した際のチェック
            #移動元の駒が成り駒だったらそのまま、そうでなかったら成りを意味する+を末尾につける
            index = self.usi_to_index(usimove[0:2])
            p = self.pieces[index[0]][index[1]]
            if p != None and p.is_promotion == False:
                usimove = usimove + '+'
        return usimove

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
        #もしくは、駒が成る手なのに移動元・移動先の両方とも成れない場所の場合、
        #または、成れない駒が成ろうとした場合は
        #illegalを返す
        index = move['to']
        if min(index) < 0 or max(index) > 8:
            return False
        if move.get('+'):
            if not move_piece.is_promotable:
                return False
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
            for i in range(move_piece.len_attack_squares + 1):
                if i == move_piece.len_attack_squares:
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

    def is_attackable(self, move):
        from_sq = move['from']
        to_sq = move['to']
        if self.pieces[from_sq[0]][from_sq[1]].name == 'knight':
            return True
        else:
            route_squares = self.return_route(move)
            for sq in route_squares:
                if self.pieces[sq[0]][sq[1]] is not None:#障害物あり
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
        if self.is_check():
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
                if piece is None or piece.color != self.turn:
                    continue
                for i in range(piece.len_attack_squares):
                    index =  (y + piece.attack_squares[i][0], x + piece.attack_squares[i][1])
                    moves.append({'from': (y, x), 'to': index, '+': False})
                    moves.append({'from': (y, x), 'to': index, '+': True})
        piece_list = self.hand_piece_index_dict.keys()
        for p in range(len(piece_list)):
            if self.pieces_in_hand[{BLACK: 0, WHITE: 1}[self.turn]][p] > 0:
                for j in range(9):
                    for k in range(9):
                        moves.append({'from': 'hand', 'to': (j, k), 'hand_piece_index': p})
        return moves

    def gen_legal_moves(self):
        sfen = self.return_sfen()
        if sfen in self.generated_legal_moves.keys():
            return self.generated_legal_moves[sfen] 
        candidate_moves = self.gen_candidate_moves()
        legal_moves = []
        for i in range(len(candidate_moves)):
            if self.is_legal(candidate_moves[i]):
                legal_moves.append(self.move_to_usi(candidate_moves[i]))
        legal_moves = list(set(legal_moves))
        self.generated_legal_moves[sfen] = legal_moves
        return legal_moves

    def gen_legal_index_moves(self, gameover_check=False):
        candidate_moves = self.gen_candidate_moves()
        legal_moves = []
        for i in range(len(candidate_moves)):
            if self.is_legal(candidate_moves[i]):
                legal_moves.append(candidate_moves[i])
                if gameover_check:
                    return legal_moves
        return legal_moves

    def gen_legal_index_moves2(self):
        candidate_moves = self.gen_candidate_moves()
        for i in range(len(candidate_moves)):
            if self.is_legal(candidate_moves[i]):
                yield candidate_moves[i]
        return

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
        check = self.is_check()
        if move['from'] == 'hand':
            #持ち駒を打つ手で自殺手になるのは王手回避をしなかった場合のみ
            if not check:
                return False
        else:#持ち駒を打つ手以外
            if self.turn == BLACK:
                king = self.king_square['black']
            else:
                king = self.king_square['white']
            if (not check) and (move['from'][0] != king[0] or move['from'][1] != king[1]):
                #王手されていない場合の玉と同じランク/ファイル/ダイアゴナルに居ない駒が移動する手は自殺手にならない 
                d = self.king_d[(king[0], king[1])]
                if move['from'] not in d:
                    if move['from'][0] != king[0] and move['from'][1] != king[1]:
                        return False
                #自玉と同じダイアゴナルに相手の角行/竜馬が、
                #自玉と同じランクに飛車/竜王が、
                #自玉と同じファイルに香車/飛車/竜王が
                #いない場合は自殺手にならない
                s = True
                if move['from'] in d:
                    #動かす駒が玉と同じダイアゴナルにある場合
                    for i in range(len(d)):
                        p = self.pieces[d[i][0]][d[i][1]]
                        if p is None or p.color == self.turn:
                            continue
                        if p.name in ('bishop', 'bishop+'):
                            #自玉と同じダイアゴナルに角行/竜馬がある
                            s = False
                            break
                elif move['from'][0] == king[0]:
                    #動かす駒が玉と同じランクにある場合  
                    for i in range(9):
                        p = self.pieces[king[0]][i]
                        if p is None or p.color == self.turn:
                            continue
                        if p.name in ('rook', 'rook+'):
                            s = False
                            break
                elif move['from'][1] == king[1]:
                    #動かす駒が玉と同じファイルにある場合
                    for i in range(9):
                        p = self.pieces[i][king[1]]
                        if p is None or p.color == self.turn:
                            continue
                        if p.name in ('lance', 'rook', 'rook+'):
                            s = False
                            break
                if s:
                    return False
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
        #盤を戻す時に使う情報
        #index_move: move
        #to_hand_piece: 取られた駒
        history_move = {'move': move, 'to_hand_piece': None}
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
                #移動先に駒がある
                history_move['to_hand_piece'] = {'name': to_sq.name, 'color': to_sq.color}
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
        #self.board_history.append(self.return_sfen())
        self.moves_history['moves'].append(history_move)
        return

    def push_usi(self, move):
        move = self.move_from_usi(move)
        self.push(move)
        return

    def pop(self):
        self.change_turn()#手番を反転して戻す
        lastmove = self.moves_history['moves'].pop(-1)
        if lastmove['move']['from'] == 'hand':
            #持ち駒を打つ手だった場合
            sq = self.pieces[lastmove['move']['to'][0]][lastmove['move']['to'][1]]
            index = self.hand_piece_index_dict[sq.in_hand]
            if self.turn == BLACK:
                self.pieces_in_hand[0][index] += 1#駒台に戻す
            else:
                self.pieces_in_hand[1][index] += 1
            self.pieces[lastmove['move']['to'][0]][lastmove['move']['to'][1]] = None#盤上から消す
            self.update_pawn_file()
            return
        #それ以外
        piece = self.pieces[lastmove['move']['to'][0]][lastmove['move']['to'][1]]#移動を行った駒
        if lastmove['move'].get('+'):
            #成る前の状態に戻す
            self.pieces[lastmove['move']['from'][0]][lastmove['move']['from'][1]] = self.piece_to_class[piece.in_hand](self.turn)
        else:
            self.pieces[lastmove['move']['from'][0]][lastmove['move']['from'][1]] = piece
            if piece.name == 'king':
                if self.turn == BLACK:
                    self.king_square['black'] = lastmove['move']['from']
                else:
                    self.king_square['white'] = lastmove['move']['from']
        if lastmove['to_hand_piece'] is None:
            self.pieces[lastmove['move']['to'][0]][lastmove['move']['to'][1]] = None
        else:
            #取られた駒を盤に戻す
            piece = self.piece_name_to_class[lastmove['to_hand_piece']['name']](lastmove['to_hand_piece']['color'])
            self.pieces[lastmove['move']['to'][0]][lastmove['move']['to'][1]] = piece
            index = self.hand_piece_index_dict[piece.in_hand]
            if self.turn == BLACK:
                self.pieces_in_hand[0][index] -= 1
            else:
                self.pieces_in_hand[1][index] -= 1
        self.update_pawn_file()
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
                if piece is None or piece.color != color:
                    continue
                for sq in piece.attack_squares:
                    index =  (y + sq[0], x + sq[1])
                    if min(index) < 0 or max(index) > 8:
                        continue
                    move = {'from': (y, x), 'to': index, '+': False}
                    if (index not in attack_square) and self.is_attackable(move):
                        attack_square.append(index)
        self.turn = color_backup
        return attack_square

    def is_check(self):
        key = self.return_sfen()
        if key in self.is_check_memo:
            return self.is_check_memo[key]
        color = {BLACK: 'black', WHITE: 'white'}[self.turn]
        king_sq = self.king_square[color]
        check = False
        attack_square = self.return_attack_square(self.color_change_dict[self.turn])
        for sq in attack_square:
            if sq[0] == king_sq[0] and sq[1] == king_sq[1]:
                check = True
                break
        self.is_check_memo[key] = check
        return check

    def is_gameover(self):
        return len(self.gen_legal_index_moves(gameover_check=True)) == 0

    def is_nyugyoku(self):
        if self.is_check():
            return False
        color = {BLACK: 'black', WHITE: 'white'}[self.turn]
        king_sq = self.king_square[color]
        sq2 = self.squares[king_sq[0]][king_sq[1]]
        if self.turn == BLACK:
            if not sq2.is_black_promotable_square:
                return False
        else:
            if not sq2.is_white_promotable_square:
                return False
        nyugyoku_point = 0
        tekizin_piece_num = 0
        for y in range(9):
            for x in range(9):
                piece = self.pieces[y][x]
                sq = self.squares[y][x]
                if piece != None:
                    if self.turn == BLACK:
                        if sq.is_black_promotable_square:
                            tekizin_piece_num += 1
                            if piece.in_hand in ['B', 'R']:
                                nyugyoku_point += 5
                            else:
                                nyugyoku_point += 1
                    else:
                        if sq.is_white_promotable_square:
                            tekizin_piece_num += 1
                            if piece.in_hand in ['B', 'R']:
                                nyugyoku_point += 5
                            else:
                                nyugyoku_point += 1
        if self.turn == BLACK:
            hand_pieces = self.pieces_in_hand[0]
        else:
            hand_pieces = self.pieces_in_hand[1]
        for i in range(len(hand_pieces)):
            point = 1
            if i in [5, 6]:
                point = 5
            nyugyoku_point += (hand_pieces[i] * point)
        if self.turn == BLACK and nyugyoku_point >= 28 and tekizin_piece_num >= 10:
            return True
        if self.turn == WHITE and nyugyoku_point >= 27 and tekizin_piece_num >= 10:
            return True
        return False
