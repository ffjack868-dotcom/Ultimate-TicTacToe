import tkinter as tk
from tkinter import messagebox
import math


class UltraTicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Ultimate Tic-Tac-Toe - AI Project")
        self.window.geometry("520x750")
        self.window.configure(bg="#2C3E50")

        # --- Game Configuration ---
        self.board_size = 3  # Default: 3x3
        self.game_mode = 'PvC'  # 'PvC' (vs AI) or 'PvP' (vs Friend)
        self.user_symbol = 'X'
        self.ai_symbol = 'O'
        self.starter = 'Player'  # Who starts?

        # --- State Variables ---
        self.current_turn = 'X'
        self.board = []
        self.buttons = []
        self.game_over = False

        # --- Theme Colors ---
        self.colors = {
            'bg': "#2C3E50",
            'btn': "#ECF0F1",
            'btn_hover': "#D5D8DC",
            'X': "#E74C3C",
            'O': "#3498DB",
            'win': "#2ECC71",
            'draw': "#F39C12",
            'text': "#2C3E50"
        }

        # --- Build UI ---
        self.create_menu()
        self.setup_ui()
        self.start_new_game()

    def create_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        # Settings Menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="⚙️ Game Settings", menu=settings_menu)

        # Game Mode
        mode_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="👥 Game Mode", menu=mode_menu)
        mode_menu.add_command(label="vs Computer 🤖", command=lambda: self.set_mode('PvC'))
        mode_menu.add_command(label="vs Friend 👤", command=lambda: self.set_mode('PvP'))

        settings_menu.add_separator()

        # Grid Size
        size_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="📏 Grid Size", menu=size_menu)
        size_menu.add_command(label="3x3 (Classic)", command=lambda: self.set_size(3))
        size_menu.add_command(label="4x4 (Advanced)", command=lambda: self.set_size(4))

        settings_menu.add_separator()

        # AI Options
        pvc_opts = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="🎮 AI Options", menu=pvc_opts)
        pvc_opts.add_command(label="Play as X", command=lambda: self.set_symbol('X'))
        pvc_opts.add_command(label="Play as O", command=lambda: self.set_symbol('O'))
        pvc_opts.add_separator()
        pvc_opts.add_command(label="I start first", command=lambda: self.set_starter('Player'))
        pvc_opts.add_command(label="AI starts first", command=lambda: self.set_starter('AI'))

    def setup_ui(self):
        # Info Panel
        self.info_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.info_frame.pack(pady=15)

        self.lbl_mode = tk.Label(self.info_frame, text="", font=('Helvetica', 11), bg=self.colors['bg'], fg="#BDC3C7")
        self.lbl_mode.pack()

        self.lbl_status = tk.Label(self.window, text="", font=('Helvetica', 18, 'bold'),
                                   bg=self.colors['bg'], fg="white")
        self.lbl_status.pack(pady=10)

        # Game Grid Area
        self.grid_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.grid_frame.pack(pady=10)

        # Reset Button
        tk.Button(self.window, text="🔄 New Game", font=('Helvetica', 12, 'bold'),
                  bg="#F1C40F", fg="#2C3E50", activebackground="#F39C12",
                  command=self.start_new_game, width=15).pack(pady=25)

    # --- Settings Handlers ---
    def set_mode(self, mode):
        self.game_mode = mode
        self.start_new_game()

    def set_size(self, size):
        self.board_size = size
        self.start_new_game()

    def set_symbol(self, sym):
        self.user_symbol = sym
        self.ai_symbol = 'O' if sym == 'X' else 'X'
        self.start_new_game()

    def set_starter(self, who):
        self.starter = who
        self.start_new_game()

    # --- Game Logic ---
    def start_new_game(self):
        # Clear previous grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Initialize State
        total_cells = self.board_size ** 2
        self.board = [" " for _ in range(total_cells)]
        self.buttons = []
        self.game_over = False

        # Update Labels
        mode_text = "vs AI" if self.game_mode == 'PvC' else "vs Friend"
        self.lbl_mode.config(text=f"Mode: {mode_text} | Grid: {self.board_size}x{self.board_size}")

        # Set Turn
        if self.game_mode == 'PvC':
            if self.starter == 'Player':
                self.current_turn = self.user_symbol
                self.lbl_status.config(text=f"Your Turn ({self.user_symbol}) 🎮")
            else:
                self.current_turn = self.ai_symbol
                self.lbl_status.config(text="AI is thinking... 🤖")
                self.window.after(600, self.ai_move)
        else:
            self.current_turn = 'X'  # In PvP, X always starts
            self.lbl_status.config(text="Player X Turn")

        # Create Grid Buttons
        for i in range(total_cells):
            btn = tk.Button(self.grid_frame, text=" ", font=('Verdana', 16, 'bold'),
                            width=5 if self.board_size == 3 else 4,
                            height=2, bg=self.colors['btn'],
                            command=lambda idx=i: self.on_click(idx))
            r, c = divmod(i, self.board_size)
            btn.grid(row=r, column=c, padx=3, pady=3)
            self.buttons.append(btn)

    def on_click(self, index):
        if self.board[index] != " " or self.game_over:
            return

        # Handle Move based on mode
        if self.game_mode == 'PvC':
            # Human Move
            if self.current_turn == self.user_symbol:
                self.make_move(index, self.user_symbol)

                if not self.check_end_condition():
                    self.current_turn = self.ai_symbol
                    self.lbl_status.config(text="AI is thinking... 🤖")
                    # Small delay so it feels like thinking
                    self.window.after(100, self.ai_move)

        else:  # PvP Mode
            self.make_move(index, self.current_turn)
            if not self.check_end_condition():
                self.current_turn = 'O' if self.current_turn == 'X' else 'X'
                self.lbl_status.config(text=f"Player {self.current_turn} Turn")

    def make_move(self, index, player):
        self.board[index] = player
        color = self.colors['X'] if player == 'X' else self.colors['O']
        self.buttons[index].config(text=player, fg=color)

    # --- Win Checking ---
    def get_winner(self, board):
        n = self.board_size
        # Rows
        for i in range(0, len(board), n):
            row = board[i:i + n]
            if row.count(row[0]) == n and row[0] != " ": return row[0]
        # Columns
        for i in range(n):
            col = [board[i + j * n] for j in range(n)]
            if col.count(col[0]) == n and col[0] != " ": return col[0]
        # Diagonals
        d1 = [board[i * (n + 1)] for i in range(n)]
        if d1.count(d1[0]) == n and d1[0] != " ": return d1[0]
        d2 = [board[(i + 1) * (n - 1)] for i in range(n)]
        if d2.count(d2[0]) == n and d2[0] != " ": return d2[0]

        return None

    def check_end_condition(self):
        winner = self.get_winner(self.board)
        if winner:
            self.highlight_win(winner)
            if self.game_mode == 'PvC':
                msg = "🎉 You Won!" if winner == self.user_symbol else "🤖 AI Won!"
            else:
                msg = f"🎉 Player {winner} Wins!"

            self.lbl_status.config(text=msg)
            messagebox.showinfo("Game Over", msg)
            self.game_over = True
            return True

        if " " not in self.board:
            self.lbl_status.config(text="🤝 It's a Draw!")
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.game_over = True
            return True

        return False

    def highlight_win(self, winner):
        n = self.board_size
        indices = []
        # Check all lines again to find winning indices
        # Rows
        for i in range(0, len(self.board), n):
            if all(self.board[i + k] == winner for k in range(n)):
                indices.extend([i + k for k in range(n)])
        # Cols
        for i in range(n):
            if all(self.board[i + j * n] == winner for j in range(n)):
                indices.extend([i + j * n for j in range(n)])
        # Diagonals
        if all(self.board[k * (n + 1)] == winner for k in range(n)):
            indices.extend([k * (n + 1) for k in range(n)])
        if all(self.board[(k + 1) * (n - 1)] == winner for k in range(n)):
            indices.extend([(k + 1) * (n - 1) for k in range(n)])

        for idx in set(indices):
            self.buttons[idx].config(bg=self.colors['win'], fg="white")

    # --- AI Algorithm (Minimax with Alpha-Beta) ---
    def ai_move(self):
        if self.game_over: return

        best_score = -math.inf
        best_move = None

        # Depth limit ensures 4x4 doesn't freeze (Complexity management)
        # 3x3 can go deep (9), 4x4 limited to 4
        depth_limit = 6 if self.board_size == 3 else 4

        # Try all empty cells
        for i in range(len(self.board)):
            if self.board[i] == " ":
                self.board[i] = self.ai_symbol
                score = self.minimax(self.board, 0, False, -math.inf, math.inf, depth_limit)
                self.board[i] = " "  # Undo move

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.make_move(best_move, self.ai_symbol)
            if not self.check_end_condition():
                self.current_turn = self.user_symbol
                self.lbl_status.config(text=f"Your Turn ({self.user_symbol}) 🎮")

    def minimax(self, board, depth, is_maximizing, alpha, beta, limit):
        winner = self.get_winner(board)
        if winner == self.ai_symbol: return 100 - depth
        if winner == self.user_symbol: return -100 + depth
        if " " not in board: return 0
        if depth >= limit: return 0  # Heuristic stop for 4x4

        if is_maximizing:
            max_eval = -math.inf
            for i in range(len(board)):
                if board[i] == " ":
                    board[i] = self.ai_symbol
                    eval_score = self.minimax(board, depth + 1, False, alpha, beta, limit)
                    board[i] = " "
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for i in range(len(board)):
                if board[i] == " ":
                    board[i] = self.user_symbol
                    eval_score = self.minimax(board, depth + 1, True, alpha, beta, limit)
                    board[i] = " "
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha: break
            return min_eval

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = UltraTicTacToe()
    game.run()