from playsound import playsound

class AudioManager:    
    def __init__(self):
        pass

    def ring_bell(self, audio_name):
        playsound(f"./data/sounds/{audio_name}")

if __name__ == "__main__":
    adm = AudioManager()
    adm.ring_bell("mp3.mp3")