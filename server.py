from flask import Flask, jsonify,render_template
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import threading

r = sr.Recognizer()
app = Flask(__name__)
CORS(app)
responses = [] 

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def recognize_speech():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.5)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
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
                tts_thread = threading.Thread(target=SpeakText, args=(MyText,))
                tts_thread.start()
                return MyText
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "Request Error"
    except sr.UnknownValueError:
        print("Please Speak")
        return ""  # Replaced unknown error

@app.route('/')
def myfun():
    responseStr = recognize_speech()
    responses.append(responseStr)
    return jsonify(responses)

if __name__ == '__main__':
    app.run(debug=True)
