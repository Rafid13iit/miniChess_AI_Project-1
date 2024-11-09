import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.GUI.main_window import MainWindow
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("MiniChess_AI_Project-01")
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()