"""
Football Simulator Game Logic
This module contains the main game class.
"""
import pygame
import sys
import math
import random
from pygame.locals import *

from settings import Settings
from team import Team
from ui import UI

class FootballSimulator:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.WIDTH, self.HEIGHT = 400, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Football Simulator")
        
        # Colors
        self.PURPLE = (102, 0, 153)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        
        # Game parameters
        self.fps = 60
        self.clock = pygame.time.Clock()
        
        # Create settings
        self.settings = Settings()
        
        # Field parameters
        self.field_center_x = self.WIDTH // 2
        self.field_center_y = self.HEIGHT // 2
        self.field_radius = 130
        
        # Goal parameters
        self.goal_width = 40
        self.goal_height = 15
        self.rotation = 0
        
        # Create teams
        self.teams = [
            Team(self.settings.team1_name, "team1_logo.png", 
                 [self.field_center_x - 40, self.field_center_y], 
                 [0, -3], self.RED, 30),
            
            Team(self.settings.team2_name, "team2_logo.png", 
                 [self.field_center_x + 40, self.field_center_y],
                 [0, 3], self.BLUE, 30)
        ]
        
        # Create UI manager
        self.ui = UI(self.screen, self.WIDTH, self.HEIGHT)
        
        # Game state
        self.is_playing = False
        self.game_time = 0  # in seconds
        self.scoring_team = None
        self.scoring_effect_timer = 0
        self.score_pulse_timer = 0
        self.show_settings = False
        
    def draw_field(self):
        """Draw the playing field with rotating goal"""
        # Fill background
        self.screen.fill(self.PURPLE)
        
        # Convert rotation to radians
        rotation_rad = math.radians(self.rotation)
        
        # Calculate goal position
        goal_angle_rad = math.radians(self.goal_width / (2 * self.field_radius) * 180 / math.pi)
        
        # Draw the main circle arc (everything except the goal opening)
        points = []
        num_points = 100
        start_angle = goal_angle_rad
        end_angle = 2 * math.pi - goal_angle_rad
        
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            rotated_angle = angle + rotation_rad
            x = self.field_center_x + self.field_radius * math.cos(rotated_angle)
            y = self.field_center_y + self.field_radius * math.sin(rotated_angle)
            points.append((x, y))
        
        # Draw the circle arc
        if len(points) > 1:
            pygame.draw.lines(self.screen, self.WHITE, False, points, 2)
        
        # Draw goal posts
        goal_left_angle = rotation_rad - goal_angle_rad
        goal_right_angle = rotation_rad + goal_angle_rad
        
        goal_left_inner = (
            self.field_center_x + self.field_radius * math.cos(goal_left_angle),
            self.field_center_y + self.field_radius * math.sin(goal_left_angle)
        )
        
        goal_right_inner = (
            self.field_center_x + self.field_radius * math.cos(goal_right_angle),
            self.field_center_y + self.field_radius * math.sin(goal_right_angle)
        )
        
        goal_left_outer = (
            self.field_center_x + (self.field_radius + self.goal_height) * math.cos(goal_left_angle),
            self.field_center_y + (self.field_radius + self.goal_height) * math.sin(goal_left_angle)
        )
        
        goal_right_outer = (
            self.field_center_x + (self.field_radius + self.goal_height) * math.cos(goal_right_angle),
            self.field_center_y + (self.field_radius + self.goal_height) * math.sin(goal_right_angle)
        )
        
        # Draw goal (left post, right post, back)
        pygame.draw.line(self.screen, self.WHITE, goal_left_inner, goal_left_outer, 2)
        pygame.draw.line(self.screen, self.WHITE, goal_right_inner, goal_right_outer, 2)
        pygame.draw.line(self.screen, self.WHITE, goal_left_outer, goal_right_outer, 2)
    
    def draw_teams(self):
        """Draw teams on the field"""
        for team in self.teams:
            team.draw(self.screen)
    
    def draw_scoring_effect(self):
        """Draw scoring effect overlay"""
        if self.scoring_effect_timer > 0:
            # Create transparent overlay
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            
            # Team color with alpha
            alpha = int(100 * math.sin(self.scoring_effect_timer * 10))
            # Ensure alpha is in valid range
            alpha = max(0, min(255, alpha))
            
            if self.scoring_team == 0:
                # Using explicit RGBA tuple for overlay
                overlay.fill((self.RED[0], self.RED[1], self.RED[2], alpha))
            else:
                # Using explicit RGBA tuple for overlay
                overlay.fill((self.BLUE[0], self.BLUE[1], self.BLUE[2], alpha))
                
            self.screen.blit(overlay, (0, 0))
    
    def check_goal(self, team_idx):
        """Check if a team has scored a goal"""
        team = self.teams[team_idx]
        
        # Convert team position to polar coordinates relative to field center
        dx = team.pos[0] - self.field_center_x
        dy = team.pos[1] - self.field_center_y
        dist_from_center = math.sqrt(dx*dx + dy*dy)
        
        # Calculate angle in the rotated frame
        team_angle = math.degrees(math.atan2(dy, dx))
        relative_angle = (team_angle - self.rotation + 360) % 360
        
        # Calculate half goal angle in degrees
        half_goal_angle = (self.goal_width / (2 * self.field_radius)) * (180 / math.pi)
        
        # Check if team is near or beyond boundary
        is_near_boundary = dist_from_center >= self.field_radius - team.size/2
        
        # Check if team is in goal area (angle near 0 degrees in rotated frame)
        in_goal_angle = relative_angle > 360 - half_goal_angle or relative_angle < half_goal_angle
        
        # Check if team is exiting through goal
        if is_near_boundary and in_goal_angle:
            # Other team scores
            other_team = 1 if team_idx == 0 else 0
            self.teams[other_team].score += 1
            
            print(f"GOAL! Team {other_team} scores! New score: {self.teams[0].score}-{self.teams[1].score}")
            
            # Trigger scoring effects
            self.scoring_team = other_team
            self.scoring_effect_timer = 1.0  # One second
            self.score_pulse_timer = 1.0
            
            # Return the team to the center with a random velocity
            self.respawn_team(team_idx)
            
            return True
        
        return False
    
    def respawn_team(self, team_idx):
        """Reset team position after scoring"""
        team = self.teams[team_idx]
        
        # Set position near center with random offset
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-20, 20)
        team.pos = [
            self.field_center_x + offset_x,
            self.field_center_y + offset_y
        ]
        
        # Give a random velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4)
        team.vel = [
            speed * math.cos(angle),
            speed * math.sin(angle)
        ]
    
    def handle_collision(self, team_idx):
        """Handle collision with boundary and other team"""
        team = self.teams[team_idx]
        
        # Get position and velocity
        x, y = team.pos
        vx, vy = team.vel
        
        # Calculate distance from center
        dx = x - self.field_center_x
        dy = y - self.field_center_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Check if team is near boundary
        if dist > self.field_radius - team.size/2:
            # First check if this is a goal
            if self.check_goal(team_idx):
                # If it's a goal, we've already handled everything
                return
            
            # If not a goal, handle normal boundary collision
            # Calculate angle of collision
            angle = math.atan2(dy, dx)
            
            # Calculate incoming angle
            vel_angle = math.atan2(vy, vx)
            
            # Calculate reflection angle
            reflection_angle = 2 * angle - vel_angle - math.pi
            
            # Calculate new velocity
            speed = math.sqrt(vx*vx + vy*vy)
            team.vel = [
                speed * math.cos(reflection_angle),
                speed * math.sin(reflection_angle)
            ]
            
            # Move team inside boundary
            team.pos = [
                self.field_center_x + (self.field_radius - team.size/2 - 1) * math.cos(angle),
                self.field_center_y + (self.field_radius - team.size/2 - 1) * math.sin(angle)
            ]
        
        # Check for collision with other team
        other_idx = 1 if team_idx == 0 else 0
        other_team = self.teams[other_idx]
        
        dx = team.pos[0] - other_team.pos[0]
        dy = team.pos[1] - other_team.pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < team.size:
            # Calculate angle between teams
            angle = math.atan2(dy, dx)
            
            # Calculate speeds
            team_speed = math.sqrt(team.vel[0]**2 + team.vel[1]**2)
            other_speed = math.sqrt(other_team.vel[0]**2 + other_team.vel[1]**2)
            
            # Exchange velocities (with angle)
            team.vel = [
                other_speed * math.cos(angle),
                other_speed * math.sin(angle)
            ]
            
            other_team.vel = [
                -team_speed * math.cos(angle),
                -team_speed * math.sin(angle)
            ]
            
            # Separate teams
            overlap = team.size - dist
            if overlap > 0:
                team.pos[0] += overlap/2 * math.cos(angle)
                team.pos[1] += overlap/2 * math.sin(angle)
                other_team.pos[0] -= overlap/2 * math.cos(angle)
                other_team.pos[1] -= overlap/2 * math.sin(angle)
    
    def update(self):
        """Update game state"""
        # Rotate field
        if self.is_playing:
            self.rotation = (self.rotation + self.settings.rotation_speed) % 360
            
            # Update game time (seconds)
            if pygame.time.get_ticks() % 1000 < 20:  # Approximately every second
                self.game_time += 1
                
                # Check if match is over
                if self.game_time >= self.settings.match_duration:
                    self.is_playing = False
                    print(f"MATCH OVER! Final score: {self.teams[0].score}-{self.teams[1].score}")
        
        # Update teams
        for i, team in enumerate(self.teams):
            if self.is_playing:
                # Move team
                team.pos[0] += team.vel[0]
                team.pos[1] += team.vel[1]
                
                # Handle collisions (which now also checks for goals)
                self.handle_collision(i)
        
        # Update timers
        if self.scoring_effect_timer > 0:
            self.scoring_effect_timer -= 1/60  # Decrement based on FPS
            if self.scoring_effect_timer <= 0:
                self.scoring_effect_timer = 0
        
        if self.score_pulse_timer > 0:
            self.score_pulse_timer -= 1/60
            if self.score_pulse_timer <= 0:
                self.score_pulse_timer = 0
                
    def reset_game(self):
        """Reset the game to initial state"""
        # Reset teams
        self.teams[0].pos = [self.field_center_x - 40, self.field_center_y]
        self.teams[0].vel = [0, -3]
        self.teams[0].score = 0
        
        self.teams[1].pos = [self.field_center_x + 40, self.field_center_y]
        self.teams[1].vel = [0, 3]
        self.teams[1].score = 0
        
        # Reset game state
        self.rotation = 0
        self.game_time = 0
        self.is_playing = False
        self.scoring_team = None
        self.scoring_effect_timer = 0
        self.score_pulse_timer = 0
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                if self.show_settings:
                    # Handle clicks in settings menu
                    settings_areas = self.ui.draw_settings_menu(self.settings)
                    if self.ui.check_settings_click(event.pos, settings_areas, self.settings, self.teams):
                        self.show_settings = False
                elif self.game_time >= self.settings.match_duration:
                    # Handle end screen button clicks
                    play_again_button = self.ui.draw_match_end_screen(self.teams, self.game_time, self.settings)
                    if play_again_button and play_again_button.collidepoint(event.pos):
                        self.reset_game()
                else:
                    # Check if buttons were clicked
                    buttons = self.ui.draw_buttons(self.is_playing)
                    if buttons["play"].collidepoint(event.pos):
                        self.is_playing = not self.is_playing
                    elif buttons["reset"].collidepoint(event.pos):
                        self.reset_game()
                    elif buttons["settings"].collidepoint(event.pos):
                        self.show_settings = True
            
            # Also handle mouse movement for slider dragging
            if event.type == MOUSEMOTION and self.show_settings and self.settings.slider_dragging:
                settings_areas = self.ui.draw_settings_menu(self.settings)
                self.ui.check_settings_click(event.pos, settings_areas, self.settings, self.teams)
            
            if event.type == MOUSEBUTTONUP and self.settings.slider_dragging:
                self.settings.slider_dragging = False
            
            if event.type == KEYDOWN:
                self.ui.handle_key_events(event, self.settings, self.teams)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw_field()
            self.draw_teams()
            
            # Draw UI elements based on game state
            if self.show_settings:
                self.ui.draw_settings_menu(self.settings)
            elif self.game_time >= self.settings.match_duration:
                self.ui.draw_match_end_screen(self.teams, self.game_time, self.settings)
            else:
                self.ui.draw_scoreboard(self.teams, self.game_time, self.settings, self.score_pulse_timer)
                self.ui.draw_buttons(self.is_playing)
            
            # Draw scoring effect on top of everything
            self.draw_scoring_effect()
            
            # Update display and control frame rate
            pygame.display.flip()
            self.clock.tick(self.fps)