import tkinter as tk
from tkinter import messagebox

#old code that didnt change
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

# GUI logic
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

# GUI setup 
root = tk.Tk()
root.title("Sudoku Solver")

frames = [[tk.Frame(root, highlightbackground="black", highlightthickness=2) for _ in range(3)] for _ in range(3)]
entries = [[None for _ in range(9)] for _ in range(9)]

#3x3 bordered frames
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

root.mainloop()
