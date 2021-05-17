import aiml
import os
import time
import argparse
import pyautogui
from time import ctime
pyautogui.FAILSAFE = False

mode = "text"
voice = "pyttsx"
terminate = ['bye', 'buy', 'shutdown', 'exit', 'quit', 'gotosleep', 'goodbye']


def get_arguments():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('params')
    optional.add_argument('-v', '--voice', action='store_true', required=False,
                          help='Enable voice mode')
    optional.add_argument('-g', '--gtts', action='store_true', required=False,
                          help='Enable Google Text To Speech engine')
    arguments = parser.parse_args()
    return arguments


def gtts_speak(jarvis_speech):
    tts = gTTS(text=jarvis_speech, lang='en')
    tts.save('jarvis_speech.mp3')
    mixer.init()
    mixer.music.load('jarvis_speech.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def offline_speak(jarvis_speech):
    engine = pyttsx.init()
    engine.say(jarvis_speech)
    engine.runAndWait()


def speak(jarvis_speech):
    if voice == "gTTS":
        gtts_speak(jarvis_speech)
    else:
        offline_speak(jarvis_speech)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk to J.A.R.V.I.S: ")
        audio = r.listen(source)
    try:
        print r.recognize_google(audio)
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        speak(
            "I couldn't understand what you said! Would you like to repeat?")
        return(listen())
    except sr.RequestError as e:
        print("Could not request results from " +
              "Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    args = get_arguments()

    if (args.voice):
        try:
            import speech_recognition as sr
            mode = "voice"
        except ImportError:
            print("\nInstall SpeechRecognition to use this feature." +
                  "\nStarting text mode\n")
    if (args.gtts):
        try:
            from gtts import gTTS
            from pygame import mixer
            voice = "gTTS"
        except ImportError:
            import pyttsx
            print("\nInstall gTTS and pygame to use this feature." +
                  "\nUsing pyttsx\n")
    else:
        import pyttsx

    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        # kernel.saveBrain("bot_brain.brn")

    # kernel now ready for use
    while True:
        if mode == "voice":
            response = listen()
            if "take a note" in response:
                file=open("note.txt", "a")
                speak("Sure Tell me!")
                response = listen()
                response=response.split(" ")
                file.write("\n"+' '.join(response))
                file.close()
                speak("Note Taken Sir.")
                
        else:
            response = raw_input("Talk to J.A.R.V.I.S : ")
        if "lock my PC" in response:
            os.system("rundll32.exe user32.dll,LockWorkStation")
        if "put my laptop in sleep mode" in response:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        if "minimise Windows" in response:
            os.system('''powershell -command "(new-object -com shell.application).minimizeall()"''')
        if "open task view" in response :
            pyautogui.keyDown("win")
            pyautogui.press("tab")
            pyautogui.keyUp("win")
        if "close current window" in response :
            pyautogui.keyDown("alt")
            pyautogui.press("f4")
            pyautogui.keyUp("alt")
        if "show start menu" in response :
            pyautogui.press("win")
        if "take screenshot" in response :
            pyautogui.keyDown("win")
            pyautogui.press("prtscr")
            pyautogui.keyUp("win")
        if "Volume down" in response :
            pyautogui.keyDown("win")
            pyautogui.press("f6")
            pyautogui.keyUp("win")
        if "mute audio" in response :
            pyautogui.keyDown("fn")
            pyautogui.press("f5")
            pyautogui.keyUp("fn")
        if "Decrease screen brightness" in response :
            pyautogui.press("F3")
        if "check my internet connection" in response or "check internet connection" in response:
            hostname="google.com"
            res=os.system("ping -c 1 "+hostname)
            if res==0:
                speak("I Think Internet is Disconnected")
                print("I Think Internet is Disconnected")
            else:
                speak("Internet Connection is fine Sir")
                print("Internet Connection is fine Sir")
        if "what time is it" in response or "what is the time now" in response:
            speak(ctime())
            print(ctime())
        
              
            

        if response.lower().replace(" ", "") in terminate:
            break
        jarvis_speech = kernel.respond(response)
        print "J.A.R.V.I.S: " + jarvis_speech
        speak(jarvis_speech)
