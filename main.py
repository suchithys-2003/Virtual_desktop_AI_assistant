
import pyttsx3
import speech_recognition as sr
import datetime, os
import random
import wikipedia
import webbrowser
import pyjokes
import time
import subprocess
import pyautogui
import psutil
import winshell
import sys
import cv2 
import socket
import imdb
import string


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



import requests

def define_word():
    speak("Please tell me the single word you want to define.")
    word = takeCommand()
    if word.lower() in ["timeout", "none"]:
        speak("I didn't get a valid response. Please try again.")
        return

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    data = response.json()

    if 'title' in data and data['title'] == 'No Definitions Found':
        speak("Word not found in the dictionary.")
    else:
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        speak(f"The definition of {word} is: {definition}")


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening........")
        r.pause_threshold = 1
        r.energy_threshold = 4000
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing.....")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.WaitTimeoutError:
            speak("Listening time has expired. I haven't received a response. Please interact with me or you can choose to exit.")
            return "Timeout"
        except sr.UnknownValueError:
            speak("Unable to recognize your voice. please speak clearly")
            return "none"
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return "Timeout"
        return query     


def username():
    while True:
        speak("What should I call you, ?")
        uname = takeCommand()
        if uname == "Timeout":
            speak("Listening time reached or could not request results. I am exiting now, thank you for using me.")
            return False
        elif uname == 'none':
            speak("I did not get it properly. Could you please tell me your name once again?")
            continue
        else:
            speak(f"Welcome Mister {uname}")
            speak("How can I help you, ?")
            return True


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning,!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")
    else:
        speak("Good Evening, !")
    speak("I am your Desktop Virtual assistant.")


def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at usage " + usage + " percent")
    battery = str(psutil.sensors_battery())
    speak("Battery is at " + battery)


def open_camera_and_take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Sorry, I am unable to access the camera.")
        return

    speak("Opening camera. You will see yourself on the screen. Press 's' to take a picture.")

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to grab frame.")
            break

        cv2.imshow("Press 's' to take a picture", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            file_path = 'captured_image.png'
            cv2.imwrite(file_path, frame)
            speak(f"Picture taken and saved as {file_path}")
            break
        elif key == ord('q'):
            speak("Exiting camera without taking a picture.")
            break

    cap.release()
    cv2.destroyAllWindows()


def movie():
    moviesdb = imdb.IMDb()
    speak("please tell me the movie name ")
    text = takeCommand()
    movies = moviesdb.search_movie(text)
    speak("Searching for " + text)

    if len(movies) == 0:
        speak("No result found")
    else:
        speak("I found these:")
        for movie in movies:
            title = movie['title']
            year = movie['year']
            speak(f'{title}-{year}')
            info = movie.getID()
            movie_details = moviesdb.get_movie(info)
            rating = movie_details['rating']
            
       
            if 'plot outline' in movie_details.keys():
                plot = movie_details['plot outline']
            else:
                plot = "Plot summary not available."

            if year < int(datetime.datetime.now().strftime('%Y')):
                speak(f'{title} was released in {year} has IMDB ratings of {rating}. The plot summary of the movie is {plot}')
                break
            else:
                speak(f'{title} will be released in {year} has IMDB ratings of {rating}. The plot summary of the movie is {plot}')


from GoogleNews import GoogleNews 
import pandas as pd
def news():
    news=GoogleNews(period='1d')
    news.search("India")
    result=news.result()
    data=pd.DataFrame.from_dict(result)
    data=data.drop(columns=['img'])
    data.head()

    for i in result:
        speak(i["title"])





def password():
    char=string.ascii_letters + string.digits
    ret= "".join(random.choice(char) for x in range(0,15))
    speak("here is your password")
    print(ret)

import random

def play_rock_paper_scissors():
    choices = ['rock', 'paper', 'scissors']
    speak("Let's play Rock, Paper, Scissors. Please choose rock, paper, or scissors.")
    
   
    user_choice = takeCommand().lower()
    if user_choice not in choices:
        speak("Invalid choice. Please choose rock, paper, or scissors.")
        return

    computer_choice = random.choice(choices)
    speak(f"I chose {computer_choice}.")

    
    if user_choice == computer_choice:
        speak("It's a tie!")
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        speak("You win!")
    else:
        speak("You lose!")


def counter():
    speak("starting the time counter,enter the time in seconds")
    t=int(input("Enter Time in seconds:"))
    while t:
        min,secs=divmod(t,60)
        timer='{:02d}:{:02d}'.format(min,secs)
        print(timer,end='\r')  
        time.sleep(1)
        t-=1 
        print("\n")  
    speak("time count is done")  



def startAssistant(on_exit_callback):
    time.sleep(3)
    wishme()
    if not username():
        on_exit_callback()
        return
    while True:
        order = takeCommand().lower()

        if 'how are you' in order:
            speak("I am fine, thank you.")
            speak("How are you, Sir?")

        elif 'fine' in order or 'good' in order:
            speak("It's good to know that you are fine.")

        elif 'who am i' in order:
            speak("If you can talk then surely you are a human.")


        elif 'who are you' in order:
            speak("I am your Virtual assistant Emma.")


        elif 'what is your name' in order:
            speak("My friends call me Emma.")

        elif 'tell me a joke' in order:
            speak("Why don't scientists trust atoms? Because they make up everything!")

        elif 'what is your favorite color' in order:
            speak("As an AI, I don't have preferences, but I think blue is quite calming.")

        elif 'what can you do' in order:
            speak("I can help you with various tasks like opening applications, telling jokes, providing information, and more. How can I assist you today?")

        elif 'what is your purpose' in order:
            speak("My purpose is to assist you with tasks and provide information to make your life easier.")

        elif 'tell me a fun fact' in order:
            speak("Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!")

        elif 'who is the prime minister of india' in order:
            speak("As of my last update, the Prime Minister of India is Narendra Modi.")

        elif 'do you have feelings' in order:
            speak("I don't have feelings, but I can simulate responses to make our interaction more natural.")

        elif 'how old are you' in order:
            speak("I was created recently and do not have an age like humans do.")

        elif 'what is artificial intelligence' in order:
            speak("Artificial Intelligence, or AI, is the simulation of human intelligence in machines that are programmed to think and learn.")

        elif 'are you alive' in order:
            speak("I am not alive in the traditional sense. I am a computer program designed to assist you.")

        elif 'can you learn' in order:
            speak("I don't learn in the same way humans do, but my creators can update and improve my capabilities over time.")

        elif 'tell me about yourself' in order:
            speak("I am a virtual assistant. I am here to help you with various tasks and provide information.")

        elif 'do you dream' in order:
            speak("I don't dream, but I can imagine scenarios based on the information I have been trained on.")

        elif 'can you drive a car' in order:
            speak("I cannot drive a car. However, there are autonomous vehicles that use AI to drive themselves.")

        elif 'what is the meaning of life' in order:
            speak("The meaning of life is a philosophical question. Different people and cultures have various interpretations. What does it mean to you?")

        elif 'do you like movies' in order:
            speak("I don't watch movies, but I can help you find information about them or suggest some popular ones.")

        elif 'what is your favorite movie' in order:
            speak("As an AI, I don't have personal preferences, but I can tell you about popular movies or the latest releases.")

        elif 'tell me a story' in order:
            speak("Once upon a time, in a land far away, there was a brave adventurer who set out on a quest to find a legendary treasure. Along the way, they faced many challenges and made new friends. In the end, they found the treasure, which was the friends and experiences they gained along the journey.")

        elif 'do you have any hobbies' in order:
            speak("I don't have hobbies like humans do, but I enjoy helping you and learning new ways to assist you.")

        elif 'what is your favorite food' in order:
            speak("I don't eat food, but I can help you find recipes or recommend restaurants.")

        elif 'what is your favorite book' in order:
            speak("I don't read books, but I can recommend some popular titles or help you find a book to read.")

        elif 'can you tell the future' in order:
            speak("I can't predict the future, but I can provide insights based on current trends and data.")

        elif 'what is your favorite song' in order:
            speak("I don't listen to music, but I can suggest some popular songs or artists if you'd like.")

        elif 'do you believe in aliens' in order:
            speak("The existence of aliens is a topic of much debate and speculation. While there is no concrete evidence, the universe is vast and full of possibilities.")

        elif 'what is the capital of France' in order:
            speak("The capital of France is Paris.")

        elif 'what is the speed of light' in order:
            speak("The speed of light in a vacuum is approximately 299,792,458 meters per second.")

        elif 'what is quantum physics' in order:
            speak("Quantum physics is a branch of science that deals with the behavior of particles at the smallest scales, such as atoms and subatomic particles. It explores phenomena that cannot be explained by classical physics.")

        elif 'what is the tallest mountain' in order:
            speak("The tallest mountain above sea level is Mount Everest, which is about 29,029 feet (8,848 meters) tall.")

        elif 'how deep is the ocean' in order:
            speak("The deepest part of the ocean is the Mariana Trench, which reaches a depth of about 36,070 feet (10,994 meters).")

        elif 'what is the meaning of AI' in order:
            speak("AI stands for Artificial Intelligence, which refers to the simulation of human intelligence in machines that are designed to think and learn like humans.")

        elif 'the time' in order:
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        elif 'open notepad' in order:
            speak("Opening Notepad for you")
            os.system('start notepad.exe')

        elif 'open calculator' in order:
            speak("Opening Calculator for you")
            os.system('start calc.exe')


        elif 'open file' in order or 'open folder' in order:
            speak("Please tell me the name of the file or folder you want to open.")
            name = takeCommand().lower()
            open_item_by_name(name)
   
        elif "music" in order or "play songs" in order or "open songs" in order:
            speak("Sure! Which song would you like me to play?")
            song_name = takeCommand().lower()

            music_dir = "D:\\New folder (2)"
            songs = os.listdir(music_dir)

            found_song = False
            for song in songs:
                if song_name.lower() in song.lower():
                    os.startfile(os.path.join(music_dir, song))
                    speak(f"Now playing {song}")
                    found_song = True
                    break

            if not found_song:
                speak(f"Sorry, I couldn't find {song_name} in your music directory.")


        elif "meaning" in order or 'define' in order:
            define_word()

        elif "wikipedia" in order:
            speak("Searching......")
            order = order.replace("wikipedia", "")
            results = wikipedia.summary(order, sentences=3)
            speak("According to Wikipedia")
            speak(results)

        elif 'open google' in order:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")

        elif 'open gaana' in order:
            speak("Here you go to gaana.com\n")
            webbrowser.open("https://gaana.com/")

        elif 'open flipkart' in order:
            speak("Here you go to Flipkart. Happy shopping!\n")
            webbrowser.open("flipkart.com")


        elif 'website' in order:
            speak("Here you go to ATME.!\n")
            webbrowser.open("https://atme.edu.in/")

        elif 'open youtube' in order:
            speak("Taking you to YouTube, \n")
            webbrowser.open("youtube.com")

        elif 'where is' in order:
            order = order.replace("where is", "")
            location = order
            speak("Locating....")
            speak(location)
            webbrowser.open("https://www.google.co.in/maps/place/" + location + "")

        elif 'write a note' in order:
            speak("What should I write, can you tell me please?")
            note = takeCommand()
            file = open('emma.txt', 'w')
            speak(" should I include date and time as well?")
            sn = takeCommand()
            if 'ok include' in sn or 'sure' in sn or 'yes' in sn:
                strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n")
                file.write(strTime)
                file.write(note)
                speak("Done, ")
            else:
                file.write(note)
                speak("Done, ")

        elif 'show note' in order:
            speak("Showing notes...")
            file = open('emma.txt')
            print(file.read())
            speak(file.read(6))

        elif 'jokes' in order or 'joke' in order:
            jokes = pyjokes.get_jokes(language='en', category='neutral')
            random_joke = random.choice(jokes)
            speak(random_joke)

        elif 'switch window' in order or 'split screen' in order or 'split' in order:
            speak("Switching the window screen.....")
            time.sleep(1)
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.keyUp('alt')

        elif 'take a screenshot' in order or 'screenshot this' in order:
            speak(" please tell me the name for this file")
            name = takeCommand().lower()
            speak("Please hold the screen")
            time.sleep(8)
            img = pyautogui.screenshot()
            img.save(f'images/{name}.png')
            speak("Screenshot captured, sir")

        elif 'cpu status' in order or 'battery status' in order:
            cpu()

        elif 'counter' in order:
            counter()   

        elif 'open camera' in order:
            open_camera_and_take_picture()

        elif 'exit now' in order or 'bye' in order or 'exit' in order:
            speak("Thank you for using me. Have a nice day.")
            sys.exit()

        elif 'empty recycle bin' in order:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle bin is recycled")
  
        elif 'ip' in order:
            host=socket.gethostname()
            ip=socket.gethostbyname(host)
            speak("Your IP address is "+ ip)

        elif 'movie' in order:
            movie()

    
        elif 'news' in order or 'latest news' in order or 'news update' in order or 'current news' in order:
            news()

        elif 'password' in order:
            password()  


        elif ' rock paper scissor' in order:
            play_rock_paper_scissors()     

        
        elif 'bmi' in order:
          height = None
          weight = None

   
          def get_valid_input(prompt):
            while True:
                speak(prompt)
                user_input = takeCommand()
                if user_input.lower() in ["timeout", "none"]:
                    speak("I didn't get a valid response. Please try again.")
                    continue
                try:
                    value = float(user_input)
                    if value > 0:
                       return value
                    else:
                        speak("The value must be a positive number. Please try again.")
                except ValueError:
                    speak("Invalid input. Please provide a numerical value.")

  
                    height = get_valid_input("Please tell me your height in centimeters.")


                    weight = get_valid_input("Please tell me your weight in kilograms.")
    
 
                    height = height / 100

    
                    BMI = weight / (height * height)
    
    
                    speak(f"Your Body Mass Index is {BMI:.2f}.")
    

                    if BMI <= 16:
                      speak("You are severely underweight.")
                    elif BMI <= 18.5:
                      speak("You are underweight.")
                    elif BMI <= 25:
                      speak("You are healthy.")
                    elif BMI <= 30:
                      speak("You are overweight.")
                    else:
                      speak("You are severely overweight.")

        
    on_exit_callback()




