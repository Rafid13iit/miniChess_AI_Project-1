import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.GUI.main_window import MainWindow
import tkinter as tk

def main():
    """
    The main function of the script. This function is called when the script
    is run directly (i.e. not imported as a module in another script).

    This function sets up the main window of the application and starts the
    application's main event loop.
    """
    # Create the main window
    root = tk.Tk()
    # Set the title of the window
    root.title("MiniChess_AI_Project-01")
    # Create an instance of the MainWindow class and pass the root window as
    # an argument. This creates the actual window and all its widgets.
    MainWindow(root)
    # Start the main event loop of the application. This is an infinite loop
    # that waits for events (such as button clicks, key presses, etc.) and
    # reacts to them by calling the appropriate functions.
    root.mainloop()

if __name__ == "__main__":
    main()