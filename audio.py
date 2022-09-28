from playsound import playsound
import os

class AudioManager:    
    def __init__(self, sounds_dir_path='./data/sounds'):
        self.sounds_dir_path = sounds_dir_path

    def ring_bell(self, audio_name):
        try:
            playsound(os.path.join(self.sounds_dir_path, audio_name))
        except:
            playsound(os.path.join(self.sounds_dir_path, "mp3.mp3"))

if __name__ == "__main__":
    adm = AudioManager()
    adm.ring_bell("mp3.mp3")