import os
import tkinter as tk
from PIL import Image, ImageTk

class PieceView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.piece_images = self.load_piece_images()

    def load_piece_images(self):
        assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        images = {}
        for color in colors:
            for piece in piece_types:
                filename = f"{color}_{piece}.png"
                path = os.path.join(assets_dir, filename)
                
                try:
                    img = Image.open(path)
                    img = img.resize((60, 60), Image.LANCZOS)
                    images[f"{color}_{piece}"] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Could not load image {filename}: {e}")
        
        return images

    def create_piece(self, piece, x, y):
        if piece is None:
            return None

        color = piece.color
        piece_type = piece.__class__.__name__.lower()
        image_key = f"{color}_{piece_type}"

        if image_key in self.piece_images:
            return self.canvas.create_image(x, y, image=self.piece_images[image_key], tags="piece")
        return None