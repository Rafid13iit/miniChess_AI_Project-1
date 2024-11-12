import os
import tkinter as tk
from PIL import Image, ImageTk
from typing import Optional, Dict, Tuple

class PieceView:
    """
    Enhanced chess piece view handler with dynamic sizing and improved visual features
    """
    PIECE_SCALE = 0.85  # Pieces take up 85% of cell size for better aesthetics
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.piece_images: Dict[str, ImageTk.PhotoImage] = {}
        self.highlighted_squares: set = set()
        self.selected_piece_id: Optional[int] = None
        self.hover_piece_id: Optional[int] = None
        
        # Get cell size from canvas (set by BoardView)
        self.cell_size = int(canvas.winfo_reqwidth() / 7)  # Divide total width by 7 (5 cells + 2 borders)
        self.piece_size = int(self.cell_size * self.PIECE_SCALE)
        
        self.load_piece_images()
        self.setup_visual_effects()
        
    def load_piece_images(self) -> None:
        """Load and prepare piece images with dynamic sizing"""
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        # Calculate piece size based on cell size
        piece_size = self.piece_size
        
        for color in colors:
            for piece in piece_types:
                filename = f"{color}_{piece}.png"
                path = os.path.join(assets_dir, filename)
                
                try:
                    img = Image.open(path)
                    # Use high-quality resizing with antialiasing
                    img = img.resize((piece_size, piece_size), Image.Resampling.LANCZOS)
                    
                    # Create normal version
                    self.piece_images[f"{color}_{piece}"] = ImageTk.PhotoImage(img)
                    
                    # Create hover effect version (slightly brighter)
                    hover_img = img.copy()
                    hover_img = hover_img.point(lambda p: min(int(p * 1.2), 255))  # Increase brightness with limit
                    self.piece_images[f"{color}_{piece}_hover"] = ImageTk.PhotoImage(hover_img)
                    
                    # Create selected version (even brighter)
                    selected_img = img.copy()
                    selected_img = selected_img.point(lambda p: min(int(p * 1.4), 255))
                    self.piece_images[f"{color}_{piece}_selected"] = ImageTk.PhotoImage(selected_img)
                    
                except Exception as e:
                    print(f"Could not load image {filename}: {e}")
    
    def setup_visual_effects(self) -> None:
        """Configure canvas bindings for visual effects"""
        self.canvas.tag_bind("piece", "<Enter>", self.on_piece_hover_enter)
        self.canvas.tag_bind("piece", "<Leave>", self.on_piece_hover_leave)
    
    def create_piece(self, piece, x: float, y: float) -> Optional[int]:
        """Create a piece with exact positioning"""
        if piece is None:
            return None
            
        color = piece.color
        piece_type = piece.__class__.__name__.lower()
        image_key = f"{color}_{piece_type}"
        
        if image_key in self.piece_images:
            piece_id = self.canvas.create_image(
                x, y,  # Use exact coordinates provided by BoardView
                image=self.piece_images[image_key],
                tags=("piece", color, piece_type),
                anchor="center"
            )
            
            # Store piece information for effects
            self.canvas.piece_info = {
                "color": color,
                "type": piece_type,
                "original_pos": (x, y)
            }
            
            return piece_id
        return None
    
    def highlight_square(self, x: float, y: float, color: str = "#ffd700") -> int:
        """Create a semi-transparent highlight effect for squares"""
        highlight_id = self.canvas.create_rectangle(
            x - self.cell_size/2,
            y - self.cell_size/2,
            x + self.cell_size/2,
            y + self.cell_size/2,
            fill=color,
            stipple="gray50",
            tags="highlight"
        )
        self.highlighted_squares.add(highlight_id)
        return highlight_id
    
    def clear_highlights(self) -> None:
        """Remove all square highlights"""
        for highlight_id in self.highlighted_squares:
            self.canvas.delete(highlight_id)
        self.highlighted_squares.clear()
    
    def on_piece_hover_enter(self, event) -> None:
        """Handle mouse hover enter event on pieces"""
        piece_id = self.canvas.find_closest(event.x, event.y)[0]
        if piece_id != self.selected_piece_id:
            self.hover_piece_id = piece_id
            self._apply_hover_effect(piece_id)
    
    def on_piece_hover_leave(self, event) -> None:
        """Handle mouse hover leave event on pieces"""
        if self.hover_piece_id:
            self._remove_hover_effect(self.hover_piece_id)
            self.hover_piece_id = None
    
    def _apply_hover_effect(self, piece_id: int) -> None:
        """Apply hover visual effect to a piece"""
        tags = self.canvas.gettags(piece_id)
        color = next((tag for tag in tags if tag in ['white', 'black']), None)
        piece_type = next((tag for tag in tags if tag not in ['piece', 'white', 'black']), None)
        
        if color and piece_type:
            hover_key = f"{color}_{piece_type}_hover"
            if hover_key in self.piece_images:
                self.canvas.itemconfig(piece_id, image=self.piece_images[hover_key])
    
    def _remove_hover_effect(self, piece_id: int) -> None:
        """Remove hover visual effect from a piece"""
        if not self.selected_piece_id or piece_id != self.selected_piece_id:
            tags = self.canvas.gettags(piece_id)
            color = next((tag for tag in tags if tag in ['white', 'black']), None)
            piece_type = next((tag for tag in tags if tag not in ['piece', 'white', 'black']), None)
            
            if color and piece_type:
                normal_key = f"{color}_{piece_type}"
                if normal_key in self.piece_images:
                    self.canvas.itemconfig(piece_id, image=self.piece_images[normal_key])

    def animate_piece_movement(self, piece_id: int, target_x: float, target_y: float, 
                             duration_ms: int = 200) -> None:
        """Smoothly animate piece movement with exact positioning"""
        start_x, start_y = self.canvas.coords(piece_id)
        dx = target_x - start_x
        dy = target_y - start_y
        steps = 20
        step_x = dx / steps
        step_y = dy / steps
        delay = duration_ms / steps
        
        def animate_step(step: int) -> None:
            if step < steps:
                self.canvas.move(piece_id, step_x, step_y)
                self.canvas.after(int(delay), lambda: animate_step(step + 1))
            else:
                # Ensure final position is exact
                final_pos = (target_x, target_y)
                self.canvas.coords(piece_id, *final_pos)
        
        animate_step(0)

    def select_piece(self, piece_id: int) -> None:
        """Apply selected visual effect to a piece"""
        self.selected_piece_id = piece_id
        tags = self.canvas.gettags(piece_id)
        color = next((tag for tag in tags if tag in ['white', 'black']), None)
        piece_type = next((tag for tag in tags if tag not in ['piece', 'white', 'black']), None)
        
        if color and piece_type:
            selected_key = f"{color}_{piece_type}_selected"
            if selected_key in self.piece_images:
                self.canvas.itemconfig(piece_id, image=self.piece_images[selected_key])

    def deselect_piece(self, piece_id: int) -> None:
        """Remove selected visual effect from a piece"""
        if self.selected_piece_id == piece_id:
            self.selected_piece_id = None
            self._remove_hover_effect(piece_id)