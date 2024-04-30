class ChessBoard:
    def __init__(self, setup=None):
        if isinstance(setup, str) and '/' in setup:
            self.board = self.fromFEN(setup)
        elif isinstance(setup, list):
            self.board = setup
        else:
            self.board = self.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.calcPaths()
    
    def calcPaths(self):
        for i in self.board:
            for j in i:
                if(j): j.paths = j.getPaths()

    def toFEN(self):
        # Simplified FEN converter
        fen = []
        for row in self.board:
            empty = 0
            fen_row = ''
            for cell in row:
                if cell is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += cell.piece
            if empty > 0:
                fen_row += str(empty)
            fen.append(fen_row)
        return '/'.join(fen) + ' w - - 0 1'

    def fromFEN(self, fen):
        # fen = 'rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w - - 0 1'
        # Convert FEN string to board
        rows = fen.split()[0].split('/')
        new_board = []
        for j, row in enumerate(rows):
            board_row = []
            i1 = 0
            for i, char in enumerate(row):
                if char.isdigit():
                    board_row.extend([None] * int(char))
                    i1 += int(char)
                else:
                    board_row.append(ChessPiece(char, chr(i1 + 97) + str(8 - j), self))
                    i1 += 1
            new_board.append(board_row)
        return new_board

    def getPiece(self, position):
        file, rank = position[0], position[1]
        return self.board[8 - int(rank)][ord(file) - 97]

    def print(self):
        # Print the board in a readable format
        for row in self.board:
            print(' | '.join([' ' if piece is None else piece.piece for piece in row]))
            print('-' * 31)  # Print separator line

    def fMove(self, notation):
        return self.move(notation, True)

    def move(self, notation, ignore = False):
        start, end = notation[:2], notation[2:]
        piece = self.getPiece(start)
        if((piece and end in piece.possibleSquares()) or ignore):
            start_row, start_col = 8 - int(start[1]), ord(start[0]) - ord('a')
            end_row, end_col = 8 - int(end[1]), ord(end[0]) - ord('a')
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = None
            self.getPiece(end).setPosition(end)
            self.calcPaths()
            return "Moved successfully!"
        else:
            return "ERROR: Illegal move!"



class ChessPiece:
    def __init__(self, piece, position, board = None) -> None:
        self.piece = piece
        self.board = board
        self.setPosition(position)
        points = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 7,
            "K": 8,
        }
        self.power = points[self.piece.upper()]
    
    def getPaths(self, attack = False, enPassant = False, includeSelfPiece = False):
        steps = {
            'p': 1,
            'P': 1,
            'R': 8,
            'N': 1,
            'B': 8,
            'Q': 8,
            'K': 1,
        }
        paths = [[] for _ in self.getDirections(1, attack, enPassant)]
        for _ in range(1, steps[self.piece.upper()] + 1):
            pieceDirections = self.getDirections(_, attack, enPassant)
            for i, x in enumerate(pieceDirections):
                if(self.fileInt + x[1] >= 1 and self.fileInt + x[1] <= 8 and self.rank + x[0] >= 1 and self.rank + x[0] <= 8):
                    paths[i].append(
                        chr(self.fileInt + x[1] + 96) +
                        str(self.rank + x[0])
                    )
        try:
            for j, path in enumerate(paths):
                for i, x in enumerate(path):
                    tPiece = self.board.getPiece(x)
                    if(tPiece):
                        if((tPiece.piece.islower() and self.piece.islower()) or (tPiece.piece.isupper() and self.piece.isupper())):
                            if(includeSelfPiece): paths[j] = path[:i + 1]
                            else: paths[j] = path[:i]
                            break
                        if((tPiece.piece.islower() and self.piece.isupper()) or (tPiece.piece.isupper() and self.piece.islower())):
                            try:
                                paths[j] = path[:i+1]
                            except:
                                paths[j] = path[:i]
                            break
        except:
            pass
        self.paths = paths
        return paths
    
    def setPosition(self, position, override=False):
        self.position = position
        self.file = position[0]
        self.rank = int(position[1])
        self.fileInt = ord(self.file) - 96
        if(not self.board or override):
            self.paths = self.getPaths()
        else:
            self.paths = []

    def possibleSquares(self):
        paths = self.getPaths()
        return [j for i in paths for j in i]
    
    def possibleAttacks(self, enPassant = False):
        paths = self.getPaths(True, enPassant)
        return [j for i in paths for j in i]
    
    def possibleDefends(self, enPassant = False):
        paths = self.getPaths(True, enPassant, True)
        return [j for i in paths for j in i]

    def getDirections(self, step = 1, attack = False, enPassant = False):
        # Define movement patterns for each piece

        directions = {
            'R': [[1, 0], [-1, 0], [0, 1], [0, -1]], # Rook movements
            'N': [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]], # Knight movements
            'B': [[1, 1], [1, -1], [-1, 1], [-1, -1]], # Bishop movements
            'Q': [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]], # Queen movements
            'K': [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]  # King movements
        }
        atkDirections = {
            'p': [[-1, -1], [-1, 1]],  # Simplified pawn movements (no en passant)
            'P': [[1, 1], [1, -1]],  # Simplified pawn movements (no en passant)
        }
        moveDirections = {
            'p': [[-1, 0]],
            'P': [[1, 0]]
        }
        piece = self.piece
        if(self.piece != 'P' and self.piece != 'p'):
            piece = self.piece.upper()
        if((piece == 'P' and self.rank == 2) or (piece == "p" and self.rank == 7)):
                moveDirections['p'].append([-2, 0])
                moveDirections['P'].append([2, 0])
        if(enPassant):
            atkDirections['p'].extend([[0, -1], [0, 1]])
            atkDirections['P'].extend([[0, -1], [0, 1]])
        
        if(attack):
            directions.update(atkDirections)
        else:
            directions.update(moveDirections)

        t = directions[piece]
        for i in range(len(t)):
            for j in range(2):
                t[i][j] *= step
        return t
