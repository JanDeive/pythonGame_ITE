import tkinter as tk
from tkinter import messagebox
import random

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(9):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        while not is_valid(board, row, col, num) or board[row][col] != 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            num = random.randint(1, 9)
        board[row][col] = num
    solve_sudoku(board)

    # difficulty
    if difficulty == 'easy':
        num_removals = random.randint(30, 35)
    elif difficulty == 'medium':
        num_removals = random.randint(36, 45)
    else:  # hard
        num_removals = random.randint(46, 55)

    for _ in range(num_removals):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        board[row][col] = 0

    return board

def solve_button_action():
    board = [[int(entries[row][col].get() or 0) for col in range(9)] for row in range(9)]
    if solve_sudoku(board):
        for row in range(9):
            for col in range(9):
                entries[row][col].delete(0, tk.END)
                entries[row][col].insert(0, str(board[row][col]))
        messagebox.showinfo("Sudoku Solver", "Sudoku solved successfully!")
    else:
        messagebox.showerror("Sudoku Solver", "No solution exists.")

def check_solution(board):
    for row in range(9):
        if len(set(board[row])) != 9 or 0 in set(board[row]):
            return False

    for col in range(9):
        column = [board[row][col] for row in range(9)]
        if len(set(column)) != 9 or 0 in set(column):
            return False

    for box_row in range(3):
        for box_col in range(3):
            nums = set()
            for i in range(3):
                for j in range(3):
                    num = board[3 * box_row + i][3 * box_col + j]
                    if num in nums or num == 0:
                        return False
                    nums.add(num)

    return True

def setup_sudoku_solver():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Sudoku Solver")
    root.configure(bg="#D2B48C")

    frames = [[tk.Frame(root, highlightbackground="black", highlightthickness=2, bg="#D2B48C") for _ in range(3)] for _ in range(3)]
    global entries
    entries = [[None for _ in range(9)] for _ in range(9)]

    for box_row in range(3):
        for box_col in range(3):
            frames[box_row][box_col].grid(row=box_row, column=box_col, padx=2, pady=2)
            for i in range(3):
                for j in range(3):
                    row, col = 3 * box_row + i, 3 * box_col + j
                    entries[row][col] = tk.Entry(frames[box_row][box_col], width=2, font=('Arial', 18), justify='center')
                    entries[row][col].grid(row=i, column=j, padx=2, pady=2)

    solve_button = tk.Button(root, text="Solve", command=solve_button_action, font=('Arial', 14))
    solve_button.grid(row=3, column=0, columnspan=3, pady=10)

def setup_sudoku_game(difficulty):
    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"Play Sudoku ({difficulty.capitalize()})")
    root.configure(bg="#D2B48C")

    frames = [[tk.Frame(root, highlightbackground="black", highlightthickness=2, bg="#D2B48C") for _ in range(3)] for _ in range(3)]
    global entries
    entries = [[None for _ in range(9)] for _ in range(9)]

    board = generate_sudoku(difficulty)

    for box_row in range(3):
        for box_col in range(3):
            frames[box_row][box_col].grid(row=box_row, column=box_col, padx=2, pady=2)
            for i in range(3):
                for j in range(3):
                    row, col = 3 * box_row + i, 3 * box_col + j
                    entries[row][col] = tk.Entry(frames[box_row][box_col], width=2, font=('Arial', 18), justify='center')
                    entries[row][col].grid(row=i, column=j, padx=2, pady=2)
                    if board[row][col] != 0:
                        entries[row][col].insert(0, str(board[row][col]))
                        entries[row][col].config(state='disabled')

    submit_button = tk.Button(root, text="Submit", font=('Arial', 14), command=lambda: submit_solution(board))
    submit_button.grid(row=3, column=0, columnspan=3, pady=10)

def submit_solution(board):
    user_board = [[int(entries[row][col].get() or 0) for col in range(9)] for row in range(9)]
    if check_solution(user_board):
        show_well_done_page()
    else:
        messagebox.showerror("Sudoku", "Incorrect solution. Please try again.")

def show_well_done_page():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Well Done!")
    root.configure(bg="#D2B48C")

    well_done_label = tk.Label(root, text="Well Done!", font=('Arial', 24), bg="#D2B48C")
    well_done_label.pack(pady=20)

    play_again_button = tk.Button(root, text="Play Again", font=('Arial', 14), command=show_difficulty_selection)
    play_again_button.pack(pady=10)

def show_welcome_page():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Welcome to Sudoku App")
    root.configure(bg="#D2B48C")

    welcome_label = tk.Label(root, text="Welcome to Sudoku App", font=('Arial', 24), bg="#D2B48C")
    welcome_label.pack(pady=20)

    play_sudoku_button = tk.Button(root, text="Play Sudoku", font=('Arial', 14), command=show_difficulty_selection)
    play_sudoku_button.pack(pady=10)

    sudoku_solver_button = tk.Button(root, text="Sudoku Solver", font=('Arial', 14), command=setup_sudoku_solver)
    sudoku_solver_button.pack(pady=10)

def show_difficulty_selection():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Select Difficulty")
    root.configure(bg="#D2B48C")

    difficulty_label = tk.Label(root, text="Choose Difficulty Level", font=('Arial', 24), bg="#D2B48C")
    difficulty_label.pack(pady=20)

    easy_button = tk.Button(root, text="Easy", font=('Arial', 14), command=lambda: setup_sudoku_game("easy"))
    easy_button.pack(pady=10)

    medium_button = tk.Button(root, text="Medium", font=('Arial', 14), command=lambda: setup_sudoku_game("medium"))
    medium_button.pack(pady=10)

    hard_button = tk.Button(root, text="Hard", font=('Arial', 14), command=lambda: setup_sudoku_game("hard"))
    hard_button.pack(pady=10)

# GUI setup
root = tk.Tk()
show_welcome_page()

root.mainloop()

