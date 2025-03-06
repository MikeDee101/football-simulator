"""
Football Simulator Main File
Run this file to start the game.
"""
import pygame
import sys
from game import FootballSimulator

def main():
    # Create and run the game
    game = FootballSimulator()
    game.run()

if __name__ == "__main__":
    main()
