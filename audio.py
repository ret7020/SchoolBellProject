from playsound import playsound
import os

class AudioManager:    
    def __init__(self):
        pass

    def ring_bell(self, audio_path):
        print("Starting bell")
        try:
            playsound(audio_path)
        except:
            print("[ERR] Can't play audio file")
       

if __name__ == "__main__":
    adm = AudioManager()
    adm.ring_bell("mp3.mp3")
