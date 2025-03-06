"""
Team Module
Handles team logic and rendering.
"""
import pygame

class Team:
    def __init__(self, name, logo_path, position, velocity, color, size=30):
        self.name = name
        self.pos = position.copy() if isinstance(position, list) else list(position)
        self.vel = velocity.copy() if isinstance(velocity, list) else list(velocity)
        self.score = 0
        self.color = color
        self.size = size
        
        # Load team logo
        self.logo = self.load_team_logo(logo_path, size)
        
    def load_team_logo(self, filename, size):
        """Load team logo or create a fallback surface if file doesn't exist"""
        try:
            logo = pygame.image.load(filename)
            return pygame.transform.scale(logo, (size, size))
        except pygame.error:
            # Create a fallback circular surface with text
            fallback = pygame.Surface((size, size), pygame.SRCALPHA)
            if "team1" in filename:
                pygame.draw.circle(fallback, (255, 0, 0), (size//2, size//2), size//2)
                text_color = (255, 255, 255)
                letter = "A"
            else:
                pygame.draw.circle(fallback, (0, 0, 255), (size//2, size//2), size//2)
                text_color = (255, 255, 255)
                letter = "B"
            
            # Add text to the circle
            font = pygame.font.Font(None, 24)
            text = font.render(letter, True, text_color)
            text_rect = text.get_rect(center=(size//2, size//2))
            fallback.blit(text, text_rect)
            
            return fallback
            
    def draw(self, screen):
        """Draw the team logo at its current position"""
        logo_rect = self.logo.get_rect(center=self.pos)
        screen.blit(self.logo, logo_rect)
        
    def update_name(self, new_name):
        """Update the team's name"""
        self.name = new_name
        print(f"Updated team name to: {new_name}")