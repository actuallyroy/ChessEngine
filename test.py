from chessBoard import ChessBoard

board = ChessBoard('rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w - - 0 1')
print(board.getPiece("h8").file)