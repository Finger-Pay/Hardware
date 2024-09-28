import pyttsx3
from flask import Flask, request, jsonify
import multiprocessing
import time

app = Flask(__name__)

# Global variables
stored_message = None
tts_queue = multiprocessing.Queue()
tts_process = None

def text_to_speech_worker(queue):
    engine = pyttsx3.init()
    while True:
        try:
            text = queue.get(block=True, timeout=1)
            if text == "STOP":
                break
            engine.say(text)
            engine.runAndWait()
        except multiprocessing.queues.Empty:
            continue
        except Exception as e:
            print(f"TTS Error: {e}")
            time.sleep(1)  # Wait a bit before trying again

def start_tts_process():
    global tts_process
    if tts_process is None or not tts_process.is_alive():
        tts_process = multiprocessing.Process(target=text_to_speech_worker, args=(tts_queue,))
        tts_process.start()

def text_to_speech(text):
    tts_queue.put(text)

@app.route('/message', methods=['GET'])
def get_message():
    global stored_message
    if stored_message is not None:
        message_to_send = stored_message
        stored_message = None
        return jsonify({"message": message_to_send})
    else:
        return jsonify({"error": " "}), 404

@app.route('/receive', methods=['POST'])
def receive_message():
    global stored_message 
    data = request.json
    if data and 'message' in data:
        stored_message = data['message']
        text_to_speech(stored_message)
        return jsonify({"status": "Message received"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    start_tts_process()
    try:
        app.run(host='0.0.0.0', port=5001)
    finally:
        tts_queue.put("STOP")
        if tts_process:
            tts_process.join(timeout=5)
            if tts_process.is_alive():
                tts_process.terminate()

                
# import pyttsx3
# from flask import Flask, request, jsonify

# app = Flask(__name__)
# # Variable to store the incoming message
# stored_message = None  # Initially no message
# def text_to_speech(text):
#     # Initialize the text-to-speech engine
#     # global engine
#     engine = pyttsx3.init()
#         # Speak the text
#     engine.say(text)
#     engine.runAndWait()  # Wait until the speech is finished
#         # Optional: wait for a few seconds before looping again

# # Route to send the message (GET)
# ### This route will be used by the hardware to get the message
# @app.route('/message', methods=['GET'])
# def get_message():
#     global stored_message
#     if stored_message is not None:
#         message_to_send = stored_message  # Capture the message

#         stored_message = None  # Reset the message after sending it
#         return jsonify({"message": message_to_send})
#     else:

#         return jsonify({"error": " "}), 404

# # Route to receive data from outside (POST)
# ### This route will be used by the outside world to send the message
# @app.route('/receive', methods=['POST'])
# def receive_message():
#     global stored_message 
#     data = request.json  # Expecting JSON data from the POST request
#     if data and 'message' in data:
#         stored_message = data['message']
#         # engine = pyttsx3.init()
#         #   # Update the stored message
#         # engine.say(stored_message)
#         # engine.runAndWait()
#         text_to_speech(stored_message)
#         return jsonify({"status": "Message received"}), 200
#     else:
#         return jsonify({"error": "Invalid data"}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)







#### steps -- pip install py3-tts  or pyttsx3


# import pyttsx3

# engine = pyttsx3.init(driverName='espeak')
# engine = pyttsx3.init(driverName='nsss')  # Default macOS driver
# text = "Testing macOS native TTS."
# engine.say(text)
# engine.runAndWait()