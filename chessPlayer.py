from math import inf
from chessBoard import ChessBoard
class ChessPlayer:
    def __init__(self, color="white", chessBoard=None) -> None:
        if(isinstance(chessBoard, ChessBoard)):
            self.board = chessBoard
        else:
            self.board = ChessBoard()
        self.color = color
        self.squares = [[Square() for __ in range(8)] for _ in range(8)]
    
    def getSquarePoints(self):
        self.calcSquares()
        res = 0
        for i in self.squares:
            for j in i:
                res += j.points
        return res
    
    def calcPossibleMoves(self):
        self.calcSquares()
        moves = []
        for r, row in enumerate(self.squares):
            for c, rowItem in enumerate(row):
                position = chr(c + 97) + str(8 - r)
                piece = self.board.getPiece(position)
                t = []
                if(piece):
                    if((self.color == "white" and piece.piece.isupper()) or (self.color != "white" and piece.piece.islower())):
                        t = piece.possibleSquares()
                        if(piece.piece.upper() == "P"):
                            atkSquares = []
                            if(piece.enPassant):
                                if(piece.file == 'a' or piece.file == 'h'):
                                    atkSquares = t[-3:]
                                    moveSquares = t[:-3]
                                else:
                                    atkSquares = t[-4:]
                                    moveSquares = t[:-4]
                            else:
                                if(piece.file == 'a' or piece.file == 'h'):
                                    atkSquares = t[-1:]
                                    moveSquares = t[:-1]
                                else:
                                    atkSquares = t[-2:]
                                    moveSquares = t[:-2]
                            t = []
                            for i in atkSquares:
                                if(self.board.getPiece(i)):
                                    tPiece = self.board.getPiece(i).piece
                                    if((self.color == "white" and tPiece.islower()) or (self.color != "white" and tPiece.isupper())):
                                        t.append(i)
                            for i in moveSquares:
                                if(not self.board.getPiece(i)):
                                    t.append(i)
                        # print(piece.piece, position, atkSquares, moveSquares, t)
                        for i in t:
                            moves.append(position + i)
        return moves

    def calcAllPossibleAttacks(self):
        t = set()
        for row in self.board.board:
            for col in row:
                if(col):
                    # if((self.color == "white" and col.piece.isupper()) or (self.color != "white" and col.piece.islower())):
                    #     t.add(col.position)
                    for i in col.possibleAttacks():
                        t.add(i)
        return t



    def calcSquares(self):
        points = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 7,
            "K": 8,
        }
        for i in range(8):
            for j in range(8):
                self.squares[i][j].points = 0
        allPossibleAttacks = self.calcAllPossibleAttacks()
        for r, row in enumerate(self.squares):
            for c, rowItem in enumerate(row):
                position = chr(c + 97) + str(8 - r)
                piece = self.board.getPiece(position)
                if(piece):
                    # print(piece.piece, position)
                    pieceStr = piece.piece.upper()
                    if((self.color == "white" and piece.piece.isupper()) or (self.color != "white" and piece.piece.islower())):
                        #If pieces are players'
                        if(position in allPossibleAttacks):
                            self.squares[r][c].add(-1 * points[pieceStr])
                        atkSquares = piece.possibleAttacks(True)
                        for i in atkSquares:
                            r1, c1 = self.rowColFrmPos(i)
                            self.squares[r1][c1].add(9 - points[pieceStr])
                    else:
                        if(position in allPossibleAttacks):
                            self.squares[r][c].add(points[pieceStr])
                        atkSquares = piece.possibleAttacks(True)
                        for i in atkSquares:
                            r1, c1 = self.rowColFrmPos(i)
                            tP = self.board.getPiece(i)
                            if(tP and ((self.color == "white" and tP.piece.isupper()) or (self.color != "white" and tP.piece.islower()))):
                                self.squares[r1][c1].add(-10 * (9 - points[pieceStr]))
                            else:
                                self.squares[r1][c1].add(-1 * (9 - points[pieceStr]))
                # else:
                #     print(None, position)
                self.squares[r][c].position = position
                self.squares[r][c].piece = piece
                # for i in self.squares:
                #     for j in i:
                #         print(str(j.points) + "\t", end="")
                #     print()
        return self.squares
    
    def rowColFrmPos(self, position):
        return 8 - int(position[1]), ord(position[0]) - 97
    
    def calcBestMove(self):
        moves = self.calcPossibleMoves()
        res = {}
        for move in moves:
            tBoard = ChessBoard(self.board.toFEN())
            self.board.fMove(move)
            res[move] = self.getSquarePoints()
            self.board = tBoard
        return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))



            
class Square:
    def __init__(self, position = None, piece = None) -> None:
        self.position = position
        self.piece = piece
        self.points = 0
    
    def add(self, points):
        self.points += points


player = ChessPlayer()

print(player.calcAllPossibleAttacks())