import pyttsx3
import time

def text_to_speech(text, loop_count):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    for _ in range(loop_count):
        # Speak the text
        engine.say(text)
        engine.runAndWait()  # Wait until the speech is finished
        # Optional: wait for a few seconds before looping again
        time.sleep(1)

if __name__ == "__main__":
    text = input("Enter the text you want to convert to speech: ")
    loop_count = int(input("Enter the number of times to repeat: "))
    text_to_speech(text, loop_count)
