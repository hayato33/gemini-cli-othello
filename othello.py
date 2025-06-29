
import sys

class Othello:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'  # B: Black, W: White

    def print_board(self):
        print("  a b c d e f g h")
        print(" +-+-+-+-+-+-+-+-+")
        for i, row in enumerate(self.board):
            print(f"{i+1}|{'|'.join(row)}|{i+1}")
            print(" +-+-+-+-+-+-+-+-+")
        print("  a b c d e f g h")

    def is_valid_move(self, x, y, player):
        if not (0 <= x < 8 and 0 <= y < 8 and self.board[y][x] == ' '):
            return False

        opponent = 'W' if player == 'B' else 'B'
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                if not (0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent):
                    continue
                
                to_flip = []
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if self.board[ny][nx] == ' ':
                        break
                    if self.board[ny][nx] == player:
                        if to_flip:
                            return True
                        break
                    to_flip.append((nx, ny))
                    nx, ny = nx + dx, ny + dy
        return False

    def get_valid_moves(self, player):
        return [(x, y) for y in range(8) for x in range(8) if self.is_valid_move(x, y, player)]

    def make_move(self, x, y, player):
        if not self.is_valid_move(x, y, player):
            return False

        self.board[y][x] = player
        opponent = 'W' if player == 'B' else 'B'

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                to_flip = []
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if self.board[ny][nx] == opponent:
                        to_flip.append((nx, ny))
                    elif self.board[ny][nx] == player:
                        for flip_x, flip_y in to_flip:
                            self.board[flip_y][flip_x] = player
                        break
                    else: # self.board[ny][nx] == ' '
                        break
                    nx, ny = nx + dx, ny + dy
        return True

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'

    def get_score(self):
        black_score = sum(row.count('B') for row in self.board)
        white_score = sum(row.count('W') for row in self.board)
        return black_score, white_score

    def play_game(self):
        while True:
            self.print_board()
            black_score, white_score = self.get_score()
            print(f"スコア: 黒 (B) {black_score} - {white_score} 白 (W)")

            valid_moves = self.get_valid_moves(self.current_player)
            if not valid_moves:
                print(f"プレイヤー {self.current_player} は有効な手がありません。ターンをスキップします。")
                self.switch_player()
                if not self.get_valid_moves(self.current_player):
                    print("どちらのプレイヤーも有効な手がありません。ゲーム終了です。")
                    break
                continue

            player_name = "黒 (B)" if self.current_player == 'B' else "白 (W)"
            print(f"{player_name} の番です。")
            
            temp_board = [row[:] for row in self.board]
            for move_x, move_y in valid_moves:
                temp_board[move_y][move_x] = '*'
            
            print("  a b c d e f g h")
            print(" +-+-+-+-+-+-+-+-+")
            for i, row in enumerate(temp_board):
                print(f"{i+1}|{'|'.join(row)}|{i+1}")
                print(" +-+-+-+-+-+-+-+-+")
            print("  a b c d e f g h")
            print("'*' の位置に石を置くことができます。")


            move = input("手を入力してください (例: 'a5'): ").lower()
            if move == 'quit':
                print("ゲームを終了します。")
                sys.exit()

            if len(move) != 2 or not ('a' <= move[0] <= 'h') or not ('1' <= move[1] <= '8'):
                print("無効な入力です。文字 (a-h) と数字 (1-8) を入力してください。")
                continue

            x = ord(move[0]) - ord('a')
            y = int(move[1]) - 1

            if self.make_move(x, y, self.current_player):
                self.switch_player()
            else:
                print("無効な手です。有効な手を選択してください。")

        self.print_board()
        black_score, white_score = self.get_score()
        print("ゲーム終了！")
        print(f"最終スコア: 黒 (B) {black_score} - {white_score} 白 (W)")
        if black_score > white_score:
            print("黒の勝ちです！")
        elif white_score > black_score:
            print("白の勝ちです！")
        else:
            print("引き分けです！")

if __name__ == "__main__":
    game = Othello()
    game.play_game()
