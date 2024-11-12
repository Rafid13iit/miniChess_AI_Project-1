# board_themes.py

class ChessBoardThemes:
    def __init__(self):
        self.color_themes = {
            # Original Themes
            'classic': {
                'light_square': '#F0D0A0',    # Classic light wood
                'dark_square': '#AE7249',     # Classic dark wood
                'highlight_selected': '#F7EC75',
                'highlight_moves': '#AAD04B',
                'coordinate_text': '#4A4A4A',
                'border': '#8B4513'
            },
            'modern': {
                'light_square': '#E5E4C5',    # Cool light blue
                'dark_square': '#30608B',     # Cool dark blue
                'highlight_selected': '#F7EC75',
                'highlight_moves': '#AAD04B',
                'coordinate_text': '#2C3E50',
                'border': '#8B4513'
            },
            'tournament': {
                'light_square': '#EAEBC4',    # Light olive
                'dark_square': '#6D9B4F',     # Forest green
                'highlight_selected': '#F7EC75',
                'highlight_moves': '#AAD04B',
                'coordinate_text': '#2C3E50',
                'border': '#234231'
            },
            'classic_mahogany': {
                'light_square': '#F5E6D3',    # Warm cream
                'dark_square': '#8B4513',     # Rich mahogany
                'highlight_selected': '#FFD700',  # Golden yellow
                'highlight_moves': '#90EE90',     # Light green
                'coordinate_text': '#2C1810',     # Dark brown
                'border': '#5C2E1A'              # Deep mahogany
            },
            'royal_azure': {
                'light_square': '#E8EEF4',    # Pearl white
                'dark_square': '#1E4D8C',     # Royal blue
                'highlight_selected': '#FFE066',  # Soft gold
                'highlight_moves': '#7FCDBB',     # Seafoam green
                'coordinate_text': '#162C4E',     # Navy blue
                'border': '#0A2642'              # Deep navy
            },
            'emerald_elite': {
                'light_square': '#F0F7EA',    # Ivory white
                'dark_square': '#2E5C3E',     # Forest emerald
                'highlight_selected': '#F0E68C',  # Khaki
                'highlight_moves': '#98FB98',     # Pale green
                'coordinate_text': '#1C3829',     # Dark green
                'border': '#234231'              # Deep emerald
            },
            'vintage_walnut': {
                'light_square': '#E8DCC4',    # Antique white
                'dark_square': '#6F4E37',     # Walnut brown
                'highlight_selected': '#DEB887',  # Burlywood
                'highlight_moves': '#B8C9A6',     # Sage green
                'coordinate_text': '#3E2723',     # Dark coffee
                'border': '#4A3728'              # Deep walnut
            },
            
            # New Premium Themes
            'marble_luxury': {
                'light_square': '#F5F5F5',    # White marble
                'dark_square': '#2F4F4F',     # Dark slate
                'highlight_selected': '#FFD700',  # Gold
                'highlight_moves': '#98FB98',     # Pale green
                'coordinate_text': '#1C1C1C',     # Almost black
                'border': '#1A1A1A'              # Pure dark
            },
            'rosewood_premium': {
                'light_square': '#FFF0E6',    # Cream white
                'dark_square': '#832A2A',     # Deep rosewood
                'highlight_selected': '#FFB347',  # Pastel orange
                'highlight_moves': '#98FB98',     # Pale green
                'coordinate_text': '#4A0404',     # Dark red
                'border': '#5C1010'              # Darker rosewood
            },
            'carbon_fiber': {
                'light_square': '#E0E0E0',    # Light gray
                'dark_square': '#1C1C1C',     # Carbon black
                'highlight_selected': '#4CA9FF',  # Electric blue
                'highlight_moves': '#00FF95',     # Neon green
                'coordinate_text': '#FFFFFF',     # White
                'border': '#000000'              # Pure black
            },
            'arctic_aurora': {
                'light_square': '#E6EEF5',    # Ice white
                'dark_square': '#264D73',     # Arctic blue
                'highlight_selected': '#7BE0AD',  # Aurora green
                'highlight_moves': '#B4A0E5',     # Northern lights purple
                'coordinate_text': '#1A3C59',     # Deep arctic
                'border': '#0D1F2D'              # Polar night
            },
            'desert_dunes': {
                'light_square': '#F5E6CC',    # Sand light
                'dark_square': '#B87B4B',     # Dune brown
                'highlight_selected': '#FFB347',  # Desert sun
                'highlight_moves': '#98FB98',     # Oasis green
                'coordinate_text': '#6B4423',     # Dark sand
                'border': '#8B4513'              # Rich sand
            },
            'cherry_blossom': {
                'light_square': '#FFE8F0',    # Sakura white
                'dark_square': '#DE6B85',     # Blossom pink
                'highlight_selected': '#FF9EAA',  # Light pink
                'highlight_moves': '#B2F0D1',     # Spring green
                'coordinate_text': '#943D4F',     # Deep pink
                'border': '#4A1F28'              # Dark cherry
            },
            'oceanic_depth': {
                'light_square': '#E0F0F5',    # Sea foam
                'dark_square': '#1F4E5F',     # Deep ocean
                'highlight_selected': '#64B5F6',  # Wave blue
                'highlight_moves': '#80DEEA',     # Shallow water
                'coordinate_text': '#0D2B33',     # Abyss
                'border': '#071B21'              # Ocean floor
            },
            'volcanic_obsidian': {
                'light_square': '#D4C4BC',    # Volcanic ash
                'dark_square': '#1A0F0F',     # Obsidian
                'highlight_selected': '#FF5722',  # Lava
                'highlight_moves': '#FFAB91',     # Cooling magma
                'coordinate_text': '#000000',     # Pure black
                'border': '#0D0707'              # Deep volcanic
            },
            'zen_garden': {
                'light_square': '#F0EDE5',    # Sand white
                'dark_square': '#7D8471',     # Stone gray
                'highlight_selected': '#B8C4B8',  # Moss
                'highlight_moves': '#D1E2C7',     # Bamboo
                'coordinate_text': '#3A3E37',     # Dark stone
                'border': '#2D2F2C'              # Temple stone
            },
            'nordic_frost': {
                'light_square': '#E8EEF1',    # Frost white
                'dark_square': '#435B66',     # Nordic blue
                'highlight_selected': '#A5CAD2',  # Ice blue
                'highlight_moves': '#B8D8BE',     # Winter sage
                'coordinate_text': '#2C3B42',     # Deep frost
                'border': '#1F292E'              # Nordic night
            }
        }
        
        self.theme_descriptions = {
            # Original themes
            'classic': 'Classic Wood',
            'modern': 'Modern Blue',
            'tournament': 'Tournament Green',
            'classic_mahogany': 'Classic Mahogany',
            'royal_azure': 'Royal Azure',
            'emerald_elite': 'Emerald Elite',
            'vintage_walnut': 'Vintage Walnut',
            
            # New premium themes
            'marble_luxury': 'Marble Luxury',
            'rosewood_premium': 'Premium Rosewood',
            'carbon_fiber': 'Carbon Fiber',
            'arctic_aurora': 'Arctic Aurora',
            'desert_dunes': 'Desert Dunes',
            'cherry_blossom': 'Cherry Blossom',
            'oceanic_depth': 'Oceanic Depth',
            'volcanic_obsidian': 'Volcanic Obsidian',
            'zen_garden': 'Zen Garden',
            'nordic_frost': 'Nordic Frost'
        }
    
    def get_theme(self, theme_id):
        """Get color scheme for a specific theme."""
        return self.color_themes.get(theme_id)
    
    def get_theme_description(self, theme_id):
        """Get the display name for a theme."""
        return self.theme_descriptions.get(theme_id)
    
    def get_all_themes(self):
        """Get all available themes and their descriptions."""
        return self.theme_descriptions.items()

    def get_theme_categories(self):
        """Get themes organized by category."""
        categories = {
            'Classic': ['classic', 'classic_mahogany', 'vintage_walnut'],
            'Modern': ['modern', 'carbon_fiber', 'royal_azure'],
            'Nature': ['emerald_elite', 'desert_dunes', 'oceanic_depth'],
            'Cultural': ['zen_garden', 'cherry_blossom', 'nordic_frost'],
            'Premium': ['marble_luxury', 'rosewood_premium', 'arctic_aurora'],
            'Special': ['tournament', 'volcanic_obsidian']
        }
        return categories