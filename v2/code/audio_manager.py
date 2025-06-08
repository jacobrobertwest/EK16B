import pygame
from random import choice

class AudioManager:
    def __init__(self):
        self.audio_files = self.import_audio_files()

    def import_audio_files(self):
        data = {"sword":[],"shield":[],"pain":[],"crash":[],"healing":[],"dizzy":[],"death":[],"roll":[]}
        for i in (1,2,3,4):
            data["sword"].append(pygame.mixer.Sound(f"sfx/sword/sword-{i}.ogg"))
        data["shield"].append(pygame.mixer.Sound(f"sfx/shield.ogg"))
        data["pain"].append(pygame.mixer.Sound(f"sfx/pain.ogg"))
        data["pain"].append(pygame.mixer.Sound(f"sfx/pain-low.ogg"))
        data["pain"].append(pygame.mixer.Sound(f"sfx/pain-high.ogg"))
        data["dizzy"].append(pygame.mixer.Sound(f"sfx/dizzy.ogg"))
        data["crash"].append(pygame.mixer.Sound(f"sfx/crash.ogg"))
        data["roll"].append(pygame.mixer.Sound(f"sfx/roll.ogg"))
        for audio_type in data:
            for idx, file in enumerate(data[audio_type]):
                data[audio_type][idx].set_volume(0.12)
        return data

    def play_sound(self,type,index):
        self.audio_files[type][index].play()

    def stop_sound(self,type,index):
        self.audio_files[type][index].stop()

    