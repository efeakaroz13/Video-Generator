import pyttsx3
import time 

engine = pyttsx3.init(driverName="nsss")
voices = engine.getProperty("voices")
for v in voices:

    
    try:
        v.languages[0].split("en")[1]
    
        engine.setProperty("voice", v.id)
        print("====SPEAKING====")
        print(voices.index(v))
        print(v)
        newVoiceRate = 145
        engine.setProperty("rate", newVoiceRate)

        engine.save_to_file("Pick a voice sir!", f"fiverr/V{voices.index(v)}.mp3")


        engine.runAndWait()

    except:
        pass