"""
Settings Module
Manages game settings and configuration.
"""

class Settings:
    def __init__(self):
        # Team names
        self.team1_name = "Team A"
        self.team2_name = "Team B"
        
        # Game settings
        self.rotation_speed = 0.5     # Degrees per frame
        self.match_duration = 30      # Seconds (represents 90 minutes)
        
        # Text input settings
        self.active_setting = None
        self.text_input = ""
        
        # Slider settings
        self.slider_dragging = False
    
    def format_time(self, seconds):
        """Format time as minutes:seconds in match time (based on 90 minutes)"""
        # Calculate match time (90 minutes scaled to match_duration seconds)
        match_seconds = seconds
        match_minutes = int((match_seconds / self.match_duration) * 90)
        match_seconds_remainder = int((match_seconds % (self.match_duration / 90)) * 60)
        
        return f"{match_minutes}'{match_seconds_remainder:02d}"
    
    def apply_setting(self, setting_name, value):
        """Apply a new setting value"""
        if setting_name == "team1_name":
            self.team1_name = value
        elif setting_name == "team2_name":
            self.team2_name = value
        elif setting_name == "rotation_speed":
            try:
                self.rotation_speed = float(value)
            except ValueError:
                # If conversion fails, keep the previous value
                pass