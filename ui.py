"""
UI Module
Handles all user interface elements.
"""
import pygame
import math
from pygame.locals import *

class UI:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        
        # Colors
        self.PURPLE = (102, 0, 153)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 60)
        
    def draw_scoreboard(self, teams, game_time, settings, score_pulse_timer=0):
        """Draw the scoreboard with team info and score"""
        # Team names and icons
        team1_text = self.font.render(teams[0].name, True, self.WHITE)
        team2_text = self.font.render(teams[1].name, True, self.WHITE)
        
        # Score
        if score_pulse_timer > 0:
            # Larger font for pulsing effect
            pulse_size = int(36 + 10 * math.sin(score_pulse_timer * 20))
            pulse_font = pygame.font.Font(None, pulse_size)
            score_text = pulse_font.render(f"{teams[0].score}:{teams[1].score}", True, self.WHITE)
        else:
            score_text = self.font.render(f"{teams[0].score}:{teams[1].score}", True, self.WHITE)
        
        # Time
        time_text = self.font.render(settings.format_time(game_time), True, self.WHITE)
        
        # Draw team info on top
        self.screen.blit(teams[0].logo, (20, 20))
        self.screen.blit(team1_text, (60, 25))
        self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, 25))
        self.screen.blit(team2_text, (self.WIDTH - 60 - team2_text.get_width(), 25))
        self.screen.blit(teams[1].logo, (self.WIDTH - 50, 20))
        
        # Draw time below score
        self.screen.blit(time_text, (self.WIDTH//2 - time_text.get_width()//2, 70))
    
    def draw_buttons(self, is_playing):
        """Draw play/pause, reset, and settings buttons"""
        button_width = 100
        button_height = 40
        play_button = pygame.Rect(self.WIDTH//2 - button_width - 10, self.HEIGHT - 60, button_width, button_height)
        reset_button = pygame.Rect(self.WIDTH//2 + 10, self.HEIGHT - 60, button_width, button_height)
        settings_button = pygame.Rect(self.WIDTH//2 - button_width//2, self.HEIGHT - 110, button_width, button_height)
        
        pygame.draw.rect(self.screen, self.WHITE, play_button, border_radius=5)
        pygame.draw.rect(self.screen, self.WHITE, reset_button, border_radius=5)
        pygame.draw.rect(self.screen, self.WHITE, settings_button, border_radius=5)
        
        play_text = self.font.render("Pause" if is_playing else "Play", True, self.PURPLE)
        reset_text = self.font.render("Reset", True, self.PURPLE)
        settings_text = self.font.render("Settings", True, self.PURPLE)
        
        self.screen.blit(play_text, (play_button.centerx - play_text.get_width()//2, 
                                    play_button.centery - play_text.get_height()//2))
        self.screen.blit(reset_text, (reset_button.centerx - reset_text.get_width()//2, 
                                     reset_button.centery - reset_text.get_height()//2))
        self.screen.blit(settings_text, (settings_button.centerx - settings_text.get_width()//2, 
                                       settings_button.centery - settings_text.get_height()//2))
        
        return {
            "play": play_button,
            "reset": reset_button,
            "settings": settings_button
        }
    
    def draw_settings_menu(self, settings):
        """Draw settings menu and return clickable areas"""
        # Settings background
        settings_bg = pygame.Rect(self.WIDTH//2 - 150, self.HEIGHT//2 - 150, 300, 300)
        pygame.draw.rect(self.screen, self.WHITE, settings_bg, border_radius=10)
        
        # Settings title
        title_text = self.font.render("Game Settings", True, self.BLACK)
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, settings_bg.top + 20))
        
        # Settings options
        y_pos = settings_bg.top + 70
        spacing = 50
        
        # Team 1 Name
        team1_label = self.small_font.render("Team A Name:", True, self.BLACK)
        self.screen.blit(team1_label, (settings_bg.left + 20, y_pos))
        
        team1_value_bg = pygame.Rect(settings_bg.left + 150, y_pos - 5, 130, 30)
        pygame.draw.rect(self.screen, self.GRAY if settings.active_setting != "team1_name" else (220, 220, 255), team1_value_bg, border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, team1_value_bg, 1, border_radius=5)
        
        team1_value = self.small_font.render(settings.team1_name if settings.active_setting != "team1_name" else settings.text_input, True, self.BLACK)
        self.screen.blit(team1_value, (team1_value_bg.left + 5, team1_value_bg.centery - team1_value.get_height()//2))
        
        # Team 2 Name
        y_pos += spacing
        team2_label = self.small_font.render("Team B Name:", True, self.BLACK)
        self.screen.blit(team2_label, (settings_bg.left + 20, y_pos))
        
        team2_value_bg = pygame.Rect(settings_bg.left + 150, y_pos - 5, 130, 30)
        pygame.draw.rect(self.screen, self.GRAY if settings.active_setting != "team2_name" else (220, 220, 255), team2_value_bg, border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, team2_value_bg, 1, border_radius=5)
        
        team2_value = self.small_font.render(settings.team2_name if settings.active_setting != "team2_name" else settings.text_input, True, self.BLACK)
        self.screen.blit(team2_value, (team2_value_bg.left + 5, team2_value_bg.centery - team2_value.get_height()//2))
        
        # Rotation Speed (with slider)
        y_pos += spacing
        speed_label = self.small_font.render("Rotation Speed:", True, self.BLACK)
        self.screen.blit(speed_label, (settings_bg.left + 20, y_pos))
        
        # Draw slider track
        slider_track = pygame.Rect(settings_bg.left + 150, y_pos + 8, 130, 6)
        pygame.draw.rect(self.screen, self.GRAY, slider_track, border_radius=3)
        
        # Calculate slider handle position (speed range 0.1 to 2.0)
        min_speed = 0.1
        max_speed = 2.0
        slider_range = slider_track.width
        handle_pos = int((settings.rotation_speed - min_speed) / (max_speed - min_speed) * slider_range)
        handle_pos = max(0, min(slider_range, handle_pos))  # Clamp position
        
        # Draw slider handle
        handle_radius = 8
        handle_center = (slider_track.left + handle_pos, slider_track.centery)
        pygame.draw.circle(self.screen, self.PURPLE, handle_center, handle_radius)
        pygame.draw.circle(self.screen, self.WHITE, handle_center, handle_radius - 2)
        
        # Display current speed value
        speed_value_text = self.small_font.render(f"{settings.rotation_speed:.1f}", True, self.BLACK)
        self.screen.blit(speed_value_text, (slider_track.right + 10, slider_track.centery - speed_value_text.get_height()//2))
        
        # Close button
        y_pos += spacing + 20
        close_button = pygame.Rect(self.WIDTH//2 - 50, settings_bg.bottom - 50, 100, 40)
        pygame.draw.rect(self.screen, self.PURPLE, close_button, border_radius=5)
        
        close_text = self.small_font.render("Save", True, self.WHITE)
        self.screen.blit(close_text, (close_button.centerx - close_text.get_width()//2, close_button.centery - close_text.get_height()//2))
        
        return {
            "team1_name": team1_value_bg,
            "team2_name": team2_value_bg,
            "slider_track": slider_track,
            "close": close_button
        }
    
    def draw_match_end_screen(self, teams, game_time, settings):
        """Display end of match screen with results"""
        if game_time >= settings.match_duration:
            # Create semi-transparent overlay
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Dark overlay with transparency
            self.screen.blit(overlay, (0, 0))
            
            # Match end text
            end_text = self.font.render("FULL TIME", True, self.WHITE)
            self.screen.blit(end_text, (self.WIDTH//2 - end_text.get_width()//2, self.HEIGHT//2 - 80))
            
            # Score
            score_text = self.large_font.render(f"{teams[0].score} - {teams[1].score}", True, self.WHITE)
            self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, self.HEIGHT//2 - 30))
            
            # Team names
            team1_name = self.small_font.render(teams[0].name, True, self.WHITE)
            team2_name = self.small_font.render(teams[1].name, True, self.WHITE)
            
            self.screen.blit(team1_name, (self.WIDTH//2 - score_text.get_width()//2 - team1_name.get_width() - 10, self.HEIGHT//2 - 20))
            self.screen.blit(team2_name, (self.WIDTH//2 + score_text.get_width()//2 + 10, self.HEIGHT//2 - 20))
            
            # Result text
            if teams[0].score > teams[1].score:
                result_text = f"{teams[0].name} wins!"
            elif teams[1].score > teams[0].score:
                result_text = f"{teams[1].name} wins!"
            else:
                result_text = "It's a draw!"
                
            result_render = self.font.render(result_text, True, self.WHITE)
            self.screen.blit(result_render, (self.WIDTH//2 - result_render.get_width()//2, self.HEIGHT//2 + 20))
            
            # Play again button
            play_again_button = pygame.Rect(self.WIDTH//2 - 75, self.HEIGHT//2 + 70, 150, 40)
            pygame.draw.rect(self.screen, self.WHITE, play_again_button, border_radius=5)
            
            play_again_text = self.font.render("Play Again", True, self.PURPLE)
            self.screen.blit(play_again_text, (play_again_button.centerx - play_again_text.get_width()//2, 
                                            play_again_button.centery - play_again_text.get_height()//2))
            
            return play_again_button
        
        return None
    
    def check_settings_click(self, pos, settings_areas, settings, teams):
        """Handle clicks in the settings menu"""
        # Check if we're clicking or dragging the slider
        if settings.slider_dragging:
            if pygame.mouse.get_pressed()[0]:  # Left button still pressed
                # Update the slider position based on mouse x position
                slider_track = settings_areas["slider_track"]
                min_speed = 0.1
                max_speed = 2.0
                
                # Calculate new speed based on mouse position
                rel_x = max(0, min(pos[0] - slider_track.left, slider_track.width))
                new_speed = min_speed + (rel_x / slider_track.width) * (max_speed - min_speed)
                
                # Round to 1 decimal place for precision
                settings.rotation_speed = round(new_speed, 1)
                return False
            else:
                # Mouse button released, stop dragging
                settings.slider_dragging = False
        
        # Normal click handling for settings areas
        for setting, area in settings_areas.items():
            if area.collidepoint(pos):
                if setting == "close":
                    # Apply settings and close
                    self.apply_settings(settings, teams)
                    return True
                elif setting == "slider_track":
                    # Start dragging the slider
                    settings.slider_dragging = True
                    # Update slider position immediately
                    min_speed = 0.1
                    max_speed = 2.0
                    rel_x = max(0, min(pos[0] - area.left, area.width))
                    settings.rotation_speed = round(min_speed + (rel_x / area.width) * (max_speed - min_speed), 1)
                elif setting in ["team1_name", "team2_name"]:
                    # Activate text input for this setting
                    settings.active_setting = setting
                    settings.text_input = getattr(settings, setting)
                return False
        
        # Click outside any setting area
        settings.active_setting = None
        return False
    
    def apply_settings(self, settings, teams):
        """Apply the current settings to the game"""
        if settings.active_setting:
            # Save current text input to the active setting
            if settings.active_setting == "team1_name":
                settings.team1_name = settings.text_input
                teams[0].update_name(settings.text_input)
            elif settings.active_setting == "team2_name":
                settings.team2_name = settings.text_input
                teams[1].update_name(settings.text_input)
            elif settings.active_setting == "rotation_speed":
                try:
                    # Convert to float for numerical settings
                    settings.rotation_speed = float(settings.text_input)
                except ValueError:
                    # If conversion fails, keep the previous value
                    pass
        
        settings.active_setting = None
        
        # Even if no active setting, ensure teams always use current settings
        teams[0].update_name(settings.team1_name)
        teams[1].update_name(settings.team2_name)
    
    def handle_key_events(self, event, settings, teams):
        """Handle key events for text input"""
        if settings.active_setting is None:
            return
            
        if event.key == pygame.K_RETURN:
            # Save the input
            self.apply_settings(settings, teams)
        elif event.key == pygame.K_BACKSPACE:
            # Remove last character
            settings.text_input = settings.text_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            # Cancel editing
            settings.active_setting = None
        else:
            # Add character
            # Limit rotation speed to numerical input
            if settings.active_setting == "rotation_speed":
                if event.unicode.isdigit() or event.unicode == '.':
                    settings.text_input += event.unicode
            else:
                # For text fields, limit length
                if len(settings.text_input) < 10:
                    settings.text_input += event.unicode