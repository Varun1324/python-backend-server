from flask import Flask, jsonify
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import threading

class SpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.responses = []
        self.start_recognition()

    def SpeakText(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def recognize_speech(self):
        try:
            with sr.Microphone() as source2:
                self.r.adjust_for_ambient_noise(source2, duration=0.5)
                audio2 = self.r.listen(source2)
                MyText = self.r.recognize_google(audio2)
                MyText = MyText.lower()
                if "make this as side heading:" in MyText:
                    final_text = MyText.split("make this as side heading:")[1].strip()
                    return f"{final_text.upper()}:"
                elif "make this as text" in MyText:
                    final_text = MyText.split("make this as text:")[1].strip()
                    return final_text
                elif "make this as a point" in MyText:
                    final_text = MyText.split("make this as a point:")[1].strip()
                    return f"* {final_text}"
                elif "stop listening" in MyText:
                    print("Stopping")
                    return "Listening stopped"
                else:
                    tts_thread = threading.Thread(target=self.SpeakText, args=(MyText,))
                    tts_thread.start()
                    return MyText
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return "Request Error"
        except sr.UnknownValueError:
            print("Please Speak")
            return ""  # Replaced unknown error

    def start_recognition(self):
        # Call recognize_speech method automatically
        responseStr = self.recognize_speech()
        if responseStr:
            self.responses.append(responseStr)

app = Flask(__name__)
CORS(app)
speech_recognizer = SpeechRecognizer()

@app.route('/')
def myfun():
    return jsonify(speech_recognizer.responses)

if __name__ == '__main__':
    app.run(debug=True)
