import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from ..game import MinichessGame

class GameSetupDialog:
    THEME_COLORS = {
        'bg_dark': '#1a1a1a',
        'bg_light': '#2d2d2d',
        'accent': '#7289da',
        'text_primary': '#ffffff',
        'text_secondary': '#9e9e9e',
        'success': '#43b581'
    }

    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("MiniChess Pro Setup")
        
        # Configure window
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Set dark theme
        self.window.configure(bg=self.THEME_COLORS['bg_dark'])
        
        # Variables
        self.player1_type = tk.StringVar(value='human')
        self.player2_type = tk.StringVar(value='ai')
        self.setup_complete = False
        
        # Create custom fonts
        self.create_fonts()
        
        # Setup styles
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.window, style='Dark.TFrame', padding="30")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.center_window()
        
        # Add hover effects
        self.setup_hover_effects()

    def create_fonts(self):
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight='bold')
        self.header_font = tkfont.Font(family='Helvetica', size=16, weight='bold')
        self.button_font = tkfont.Font(family='Helvetica', size=12, weight='bold')

    def setup_styles(self):
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Dark.TFrame',
                       background=self.THEME_COLORS['bg_dark'])
        
        style.configure('Card.TFrame',
                       background=self.THEME_COLORS['bg_light'],
                       relief='flat')
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.THEME_COLORS['bg_dark'],
                       foreground=self.THEME_COLORS['text_primary'],
                       font=self.title_font)
        
        style.configure('Header.TLabel',
                       background=self.THEME_COLORS['bg_light'],
                       foreground=self.THEME_COLORS['text_primary'],
                       font=self.header_font)
        
        # Configure button styles
        style.configure('Action.TButton',
                       background=self.THEME_COLORS['accent'],
                       foreground=self.THEME_COLORS['text_primary'],
                       font=self.button_font,
                       padding=(30, 15))
        
        # Configure radiobutton styles
        style.configure('Player.TRadiobutton',
                       background=self.THEME_COLORS['bg_light'],
                       foreground=self.THEME_COLORS['text_primary'],
                       font=('Helvetica', 12))

    def create_widgets(self):
        # Title with subtitle
        title_frame = ttk.Frame(self.main_container, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        ttk.Label(title_frame,
                 text="MINICHESS",
                 style='Title.TLabel').pack()
        
        ttk.Label(title_frame,
                 text="Game Setup",
                 foreground=self.THEME_COLORS['text_secondary'],
                 background=self.THEME_COLORS['bg_dark'],
                 font=('Helvetica', 14)).pack()

        # Player selection cards
        self.create_player_card("WHITE PLAYER", self.player1_type, "♔")
        self.create_player_card("BLACK PLAYER", self.player2_type, "♚")

        # Start button with pulsing effect
        self.start_button = tk.Button(self.main_container,
                                    text="START GAME",
                                    font=self.button_font,
                                    fg=self.THEME_COLORS['text_primary'],
                                    bg=self.THEME_COLORS['accent'],
                                    activebackground=self.THEME_COLORS['success'],
                                    activeforeground=self.THEME_COLORS['text_primary'],
                                    relief='flat',
                                    command=self.start_game,
                                    cursor='hand2',
                                    pady=15)
        self.start_button.pack(fill=tk.X, pady=(30, 0))
        
        # Add pulsing animation
        self.pulse_animation()

    def create_player_card(self, title, variable, chess_piece):
        card = ttk.Frame(self.main_container, style='Card.TFrame', padding=20)
        card.pack(fill=tk.X, pady=(0, 20))
        
        # Header with chess piece
        header_frame = ttk.Frame(card, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header_frame,
                 text=chess_piece,
                 font=('Arial', 36),
                 foreground=self.THEME_COLORS['accent'],
                 background=self.THEME_COLORS['bg_light']).pack(side=tk.LEFT)
        
        ttk.Label(header_frame,
                 text=title,
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(15, 0))

        # Options container
        options_frame = ttk.Frame(card, style='Card.TFrame')
        options_frame.pack(fill=tk.X)
        
        # Player type selection with custom radio buttons
        for value, text, icon in [('human', 'Human Player', '👤'), ('ai', 'AI Player', '🤖')]:
            option_frame = ttk.Frame(options_frame, style='Card.TFrame')
            option_frame.pack(fill=tk.X, pady=5)
            
            rb = ttk.Radiobutton(option_frame,
                                text=f"{icon} {text}",
                                variable=variable,
                                value=value,
                                style='Player.TRadiobutton')
            rb.pack(side=tk.LEFT, padx=10)

    def setup_hover_effects(self):
        def on_enter(e):
            e.widget.configure(bg=self.THEME_COLORS['success'])
            
        def on_leave(e):
            e.widget.configure(bg=self.THEME_COLORS['accent'])
            
        self.start_button.bind('<Enter>', on_enter)
        self.start_button.bind('<Leave>', on_leave)

    def pulse_animation(self):
        if not self.setup_complete:
            current_color = self.start_button.cget('background')
            next_color = self.THEME_COLORS['success'] if current_color == self.THEME_COLORS['accent'] else self.THEME_COLORS['accent']
            self.start_button.configure(bg=next_color)
            self.window.after(1500, self.pulse_animation)

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def start_game(self):
        self.setup_complete = True
        game = MinichessGame(self.player1_type.get(), self.player2_type.get())
        self.window.destroy()
        return game

# Helper function to create translucent overlay effect
def create_hover_effect(widget, color):
    overlay = tk.Frame(widget, bg=color)
    
    def on_enter(e):
        overlay.place(relwidth=1, relheight=1)
        
    def on_leave(e):
        overlay.place_forget()
        
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)