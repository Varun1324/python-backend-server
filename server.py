from flask import Flask, jsonify, request
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import threading
import io

app = Flask(__name__)
CORS(app)

class SpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.responses = []
        self.keep_listening = False
        self.listen_thread = threading.Thread(target=self.start_recognition)
        self.listen_thread.start()

    def SpeakText(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def recognize_speech(self):
        try:
            with sr.Microphone() as source2:
                self.r.adjust_for_ambient_noise(source2, duration=0.5)
                print("Listening...")
                audio2 = self.r.listen(source2)
                print("Recognizing...")
                MyText = self.r.recognize_google(audio2)
                MyText = MyText.lower()
                print(f"Recognized Text: {MyText}")
                self.responses.append(MyText)  # Store response

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Could not understand audio, Please Speak Again.")

    def start_recognition(self):
        while True:
            if self.keep_listening:
                self.recognize_speech()

speech_recognizer = SpeechRecognizer()

@app.route('/')
def get_responses():
    return jsonify(speech_recognizer.responses)

@app.route('/start', methods=['POST'])
def start_listening():
    speech_recognizer.keep_listening = True
    return jsonify({"status": "Recording started"})

@app.route('/stop', methods=['POST'])
def stop_listening():
    speech_recognizer.keep_listening = False
    return jsonify({"status": "Recording stopped"})

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    audio_bytes = io.BytesIO(audio_file.read())
    audio = sr.AudioFile(audio_bytes)
    
    try:
        with audio as source:
            audio_data = sr.Recognizer().record(source)
            text = sr.Recognizer().recognize_google(audio_data)
            text = text.lower()
            print(f"Recognized Text from uploaded audio: {text}")
            speech_recognizer.responses.append(text)
            return jsonify({"status": "Audio processed", "text": text})
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500
    except sr.UnknownValueError:
        print("Could not understand audio, Please Speak Again.")
        return jsonify({"status": "Error", "message": "Could not understand audio"}), 500

if __name__ == '__main__':
    app.run(debug=True)
