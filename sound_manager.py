import pygame
import os

pygame.mixer.init()

class SoundManager:
    def __init__(self):
        self.muted = False

        base_path = "sounds"

        self.sounds = {}
        sound_files = {
            "hit_block": "hit_block.wav",
            "hit_paddle": "hit_paddle.wav",
            "lose_life": "lose_life.wav",
            "game_over": "game_over.wav",
            "start": "start.wav",
            "level_up": "level_up.wav"
        }

        for key, filename in sound_files.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                self.sounds[key] = pygame.mixer.Sound(path)
            else:
                print(f"File {path} not found!")
                self.sounds[key] = None

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.stop()

    def play_hit_block(self):
        if not self.muted and self.sounds.get("hit_block"):
            self.sounds["hit_block"].play()

    def play_hit_paddle(self):
        if not self.muted and self.sounds.get("hit_paddle"):
            self.sounds["hit_paddle"].play()

    def play_lose_life(self):
        if not self.muted and self.sounds.get("lose_life"):
            self.sounds["lose_life"].play()

    def play_game_over(self):
        if not self.muted and self.sounds.get("game_over"):
            self.sounds["game_over"].play()

    def play_start(self):
        if not self.muted and self.sounds.get("start"):
            self.sounds["start"].play()

    def play_level_up(self):
        if not self.muted and self.sounds.get("level_up"):
            self.sounds["level_up"].play()

sounds = SoundManager()