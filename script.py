import aiml
import os
import time
import argparse
from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image 
from time import ctime 
import speech_recognition as sr

import pyautogui
#from gtts import gTTS
#from pygame import mixer
import pyttsx
mode = "text"
voice = "pyttsx"
terminate = ['bye', 'buy', 'shutdown', 'exit', 'quit', 'gotosleep', 'goodbye']
ttext=False
tvoice=False
class GUI:
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_gui()
        
    def initialize_gui(self): # GUI initializer
        self.root.title("R.O.S.S The Personal Assistant") 
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()


    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Response Area:', font=("Monotype Corsiva", 14)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Monotype Corsiva", 13))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=25)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def voice_listen(self):
        response = listen()
        self.send_vpa("You : "+response)
        textExecute(response)

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Message Entry Area:', font=("Monotype Corsiva", 14)).pack(side='top', anchor='w',padx=15,pady=15)
        #img = ImageTk.PhotoImage(Image.open("1.png"))
        #Label(frame, image = img).pack(side='right')
        #photo1 = PhotoImage(file="1.png")
        #Button(frame, width=155, height=55, image=photo1, text="optional text", bg='green').pack(side='right', padx=2, pady=2)
        Button(frame,text='voice',bg='green',command=self.voice_listen).pack(side='right',padx=10,pady=10)
        self.enter_text_widget = Text(frame, width=40, height=3, font=("Monotype Corsiva", 13))
        self.enter_text_widget.pack(side='left', padx=15,pady=13)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_enter_key_pressed(self, event):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        self.send_chat()
        self.clear_text()
        textExecute(data)

    def clear_text(self):
        self.enter_text_widget.delete('end')

    def send_chat(self):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        self.chat_transcript_area.insert('end',"You : " + data + '\n')
        self.chat_transcript_area.yview(END)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def send_vpa(self,baka):
        self.chat_transcript_area.insert('end', baka + '\n')
        self.chat_transcript_area.yview(END)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)

    


        
def offline_speak(jarvis_speech):
    engine = pyttsx.init()
    engine.say(jarvis_speech)
    engine.runAndWait()


def speak(jarvis_speech):
    offline_speak(jarvis_speech)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        gui.send_vpa(r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        speak(
            "I couldn't understand what you said! Would you like to repeat?")
        return(listen())
    except sr.RequestError as e:
        gui.send_vpa("Could not request results from " +
            "Google Speech Recognition service; {0}".format(e))

def textExecute(response):
    if "take a note" in response:
        file=open("note.txt", "a")
        speak("Sure Tell me!")
        response = listen()
        response=response.split(" ")
        file.write("\n"+' '.join(response))
        file.close()
        speak("Note Taken Sir.")
    if "lock my PC" in response:
        os.system("rundll32.exe user32.dll,LockWorkStation")
    if "put my laptop in sleep mode" in response:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    if "minimise Windows" in response:
        os.system('''powershell -command "(new-object -com shell.application).minimizeall()"''')
    if "open Task view" in response :
        pyautogui.keyDown("win")
        pyautogui.press("tab")
        pyautogui.keyUp("win")
    if "exit" in response :
        pyautogui.keyDown("alt")
        pyautogui.press("f4")
        pyautogui.keyUp("alt")
    if "show start menu" in response :
        pyautogui.press("win")
    if "take screenshot" in response or "screenshot" in response :
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
            gui.send_vpa("R.O.S.S : I Think Internet is Disconnected")
        else:
            speak("Internet Connection is fine Sir")
            gui.send_vpa("R.O.S.S : Internet Connection is fine Sir")
    if "what time is it" in response or "what is the time now" in response:
        speak(ctime())
        gui.send_vpa("R.O.S.S : "+ctime())
    jarvis_speech = kernel.respond(response)
    gui.send_vpa("R.O.S.S : " + jarvis_speech)
    speak(jarvis_speech)


root = Tk()
gui=GUI(root)
if __name__ == '__main__':
    
    kernel = aiml.Kernel()
    #self.send_vpa(self.kernel)
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")

    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()