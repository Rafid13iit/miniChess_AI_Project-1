import tkinter as tk
from tkinter import ttk
import threading
import time

from src.game import MinichessGame

class GameSetupDialog:
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'accent': '#3498db',
        'background': '#ecf0f1',
        'text': '#2c3e50',
        'white': '#ffffff',
        'border': '#bdc3c7'
    }

    def __init__(self, parent):
        # Set the parent window and create a new top-level window
        self.parent = parent
        self.window = tk.Toplevel(parent)
        
        # Set the title of the window
        self.window.title("MiniChess - Game Setup")
        
        # Initialize game attribute to None
        self.game = None
        
        # Define the dimensions of the window
        window_width = 500
        window_height = 600
        
        # Get the width and height of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate the center position of the window on the screen
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        
        # Set the geometry of the window to the specified width, height, and position
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Make the window a transient window (always on top of the parent window)
        self.window.transient(parent)
        
        # Grab all input focus, making this window modal
        self.window.grab_set()
        
        # Make the window non-resizable
        self.window.resizable(False, False)
        
        # Set the background color of the window using predefined colors
        self.window.configure(bg=self.COLORS['background'])
        
        # Initialize player type variables with default values
        self.player1_type = tk.StringVar(value='human')
        self.player2_type = tk.StringVar(value='ai')
        
        # Call a method to set up styles for the window
        self.setup_styles()
        
        # Call a method to create the necessary widgets for the window
        self.create_widgets()

    def setup_styles(self):
        """
        Configure the styles for the widgets in the window.
        
        This method uses the ttk.Style class to configure the styles for the
        widgets in the window.
        """
        style = ttk.Style()

        # Configure the style for the main frame
        style.configure('Main.TFrame',
                       background=self.COLORS['background'])

        # Configure the style for the label frame
        style.configure('Player.TLabelframe',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])
        style.configure('Player.TLabelframe.Label',
                       font=('Helvetica', 12, 'bold'),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])

        # Configure the style for the radiobutton
        style.configure('Player.TRadiobutton',
                       font=('Helvetica', 11),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])

        # Configure the style for the start button
        style.configure('Start.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=15,
                       background=self.COLORS['accent'])

        # Configure the style for the separator
        style.configure('TSeparator',
                       background=self.COLORS['border'])


    def create_widgets(self):
        """
        Create all the widgets in the window.
        
        This method creates all the widgets in the window, including the main
        container, the title and subtitle, the separator, the player setup
        sections, and the footer section.
        """
        # Main container with padding
        self.main_frame = ttk.Frame(self.window, style='Main.TFrame', padding="30 25")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and subtitle
        self.create_header()
        
        # Separator
        ttk.Separator(self.main_frame).pack(fill=tk.X, pady=20)
        
        # Player setup sections
        # Create a section for each player, with a label frame that contains
        # two radiobuttons for selecting the player type.
        self.create_player_section("White Player", self.player1_type)
        self.create_player_section("Black Player", self.player2_type)
        
        # Footer section
        # Create a frame at the bottom of the window that contains the start
        # button and the quit button.
        self.create_footer()

    def create_header(self):
        """
        Create the title and subtitle of the game setup window

        This method creates the title and subtitle of the game setup window.
        The title is a label with a bold font, size 24, and a blue color.
        The subtitle is a label with a normal font, size 12, and a gray color.
        """
        # Title
        # Create a label for the title
        title_label = ttk.Label(self.main_frame,
                               # Set the text of the label
                               text="MiniChess Setup",
                               # Set the font of the label to Helvetica, size 24, bold
                               font=('Helvetica', 24, 'bold'),
                               # Set the foreground color of the label to blue
                               foreground=self.COLORS['primary'],
                               # Set the background color of the label to white
                               background=self.COLORS['background'])
        # Pack the label, adding padding above and below the label
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        # Create a label for the subtitle
        subtitle_label = ttk.Label(self.main_frame,
                                 # Set the text of the label
                                 text="Configure your game settings",
                                 # Set the font of the label to Helvetica, size 12
                                 font=('Helvetica', 12),
                                 # Set the foreground color of the label to gray
                                 foreground=self.COLORS['secondary'],
                                 # Set the background color of the label to white
                                 background=self.COLORS['background'])
        # Pack the label, adding padding above and below the label
        subtitle_label.pack(pady=(0, 10))

    def create_player_section(self, title, variable):
        """
        Create a section for the player configuration

        This method creates a section for the player configuration, which
        includes a label, a frame, and two radio buttons. The label is the
        title of the section and the frame contains the two radio buttons.
        The two radio buttons are used to select the type of player: human
        or AI.

        Parameters
        ----------
        title : str
            The title of the section
        variable : str
            The variable name of the selected player type

        Returns
        -------
        None
        """
        # Player frame
        # Create a frame for the player type selection
        frame = ttk.LabelFrame(self.main_frame,
                             # Set the text of the label to the title
                             text=title,
                             # Set the style of the frame to the predefined style
                             style='Player.TLabelframe',
                             # Set the padding of the frame to 20 pixels on the left and right
                             # and 15 pixels on the top and bottom
                             padding="20 15")
        # Pack the frame, adding padding above and below the frame
        frame.pack(fill=tk.X, pady=10)
        
        # Player type selection
        # Create a radio button for the human player
        ttk.Radiobutton(frame,
                       # Set the text of the button to "Human Player"
                       text="Human Player",
                       # Set the variable of the button to the variable
                       # that stores the selected player type
                       variable=variable,
                       # Set the value of the button to 'human'
                       value='human',
                       # Set the style of the button to the predefined style
                       style='Player.TRadiobutton').pack(anchor=tk.W, pady=5)
        
        # Create a radio button for the AI player
        ttk.Radiobutton(frame,
                       # Set the text of the button to "AI Player"
                       text="AI Player",
                       # Set the variable of the button to the variable
                       # that stores the selected player type
                       variable=variable,
                       # Set the value of the button to 'ai'
                       value='ai',
                       # Set the style of the button to the predefined style
                       style='Player.TRadiobutton').pack(anchor=tk.W, pady=5)

    def create_footer(self):
        # Separator before footer
        ttk.Separator(self.main_frame).pack(fill=tk.X, pady=20)
        
        # Footer frame
        footer_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        footer_frame.pack(fill=tk.X, pady=10)
        
        # Start button with custom style
        self.start_button = ttk.Button(footer_frame,
                                     text="Start Game",
                                     command=self.start_game,
                                     style='Start.TButton')
        self.start_button.pack(pady=10)
        
        # Keyboard shortcut hint
        shortcut_label = ttk.Label(footer_frame,
                                 text="Press Enter to start or Esc to cancel",
                                 font=('Helvetica', 9),
                                 foreground=self.COLORS['secondary'],
                                 background=self.COLORS['background'])
        shortcut_label.pack(pady=(5, 0))
        
        # Bind keyboard shortcuts
        self.window.bind('<Return>', lambda e: self.start_game())
        self.window.bind('<Escape>', lambda e: self.window.destroy())
        
        # Bind hover effects
        self.start_button.bind('<Enter>', self.on_enter)
        self.start_button.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self.start_button.state(['active'])

    def on_leave(self, event):
        self.start_button.state(['!active'])

    def start_game(self):
        # Create a new MinichessGame instance with the selected player types
        # `self.player1_type.get()` retrieves the selected type for player 1 (e.g., 'human' or 'ai')
        # `self.player2_type.get()` retrieves the selected type for player 2
        game = MinichessGame(self.player1_type.get(), self.player2_type.get())
        
        # Close the game setup window
        self.window.destroy()
        
        # Return the newly created game instance
        return game
