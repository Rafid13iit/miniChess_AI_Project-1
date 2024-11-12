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
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("MiniChess - Game Setup")
        self.game = None
        
        # Configure window
        window_width = 440
        window_height = 580
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Window properties
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        self.window.configure(bg=self.COLORS['background'])
        
        # Variables
        self.player1_type = tk.StringVar(value='human')
        self.player2_type = tk.StringVar(value='ai')
        
        # Setup
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        
        # Configure main frame style
        style.configure('Main.TFrame',
                       background=self.COLORS['background'])
        
        # Configure label frame style
        style.configure('Player.TLabelframe',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])
        style.configure('Player.TLabelframe.Label',
                       font=('Helvetica', 12, 'bold'),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])
        
        # Configure radiobutton style
        style.configure('Player.TRadiobutton',
                       font=('Helvetica', 11),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])
        
        # Configure button style
        style.configure('Start.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=15,
                       background=self.COLORS['accent'])
        
        # Configure separator style
        style.configure('TSeparator',
                       background=self.COLORS['border'])

    def create_widgets(self):
        # Main container with padding
        self.main_frame = ttk.Frame(self.window, style='Main.TFrame', padding="30 25")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and subtitle
        self.create_header()
        
        # Separator
        ttk.Separator(self.main_frame).pack(fill=tk.X, pady=20)
        
        # Player setup sections
        self.create_player_section("White Player", self.player1_type)
        self.create_player_section("Black Player", self.player2_type)
        
        # Footer section
        self.create_footer()

    def create_header(self):
        # Title
        title_label = ttk.Label(self.main_frame,
                               text="MiniChess Setup",
                               font=('Helvetica', 24, 'bold'),
                               foreground=self.COLORS['primary'],
                               background=self.COLORS['background'])
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(self.main_frame,
                                 text="Configure your game settings",
                                 font=('Helvetica', 12),
                                 foreground=self.COLORS['secondary'],
                                 background=self.COLORS['background'])
        subtitle_label.pack(pady=(0, 10))

    def create_player_section(self, title, variable):
        # Player frame
        frame = ttk.LabelFrame(self.main_frame,
                             text=title,
                             style='Player.TLabelframe',
                             padding="20 15")
        frame.pack(fill=tk.X, pady=10)
        
        # Player type selection
        ttk.Radiobutton(frame,
                       text="Human Player",
                       variable=variable,
                       value='human',
                       style='Player.TRadiobutton').pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(frame,
                       text="AI Player",
                       variable=variable,
                       value='ai',
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
        game = MinichessGame(self.player1_type.get(), self.player2_type.get())
        self.window.destroy()
        return game