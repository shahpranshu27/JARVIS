import speech_recognition as sr
import subprocess
import pyttsx3
from decouple import config
from datetime import datetime
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message, get_random_joke
# from functions.os_ops import open_Calculator, open_camera, open_Chrome, open_cmd, open_Notepad
from functions.os_ops import open_camera
from pprint import pprint
# from google.cloud import speech

engine = pyttsx3.init('sapi5')

# set Race i.e. speed of speech
engine.setProperty('rate',190)

# set Volume
engine.setProperty('volume',1.0)

# set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()
USERNAME = config('USER')
BOTNAME = config('BOTNAME')
def greetUser():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if(hour>=6) and (hour<12):
        speak(f"Good Morning {USERNAME}")
        print(f"Good Morning {USERNAME}")
    elif(hour>=12) and (hour<16):
        speak(f"Good afternoon {USERNAME}")
        print(f"Good afternoon {USERNAME}")
    elif(hour>=16) and (hour<20):
        speak(f"Good evening {USERNAME}")
        print(f"Good evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")
    
def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio).lower()
        print(f"You said: {query}")

        return query
    except sr.UnknownValueError:
        print("Sorry I couldn't understand what you said. Could you please repeat again??")
        # return None
    except sr.RequestError as e:
        print(f"Error connecting to Google Speech Recognition service; {e}")
        # return None

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == '__main__':
    greetUser()
    while True:
        # query = take_user_input().lower()
        query = take_user_input()

        # ... (Local operations)
        if query:

            if 'open notepad' in query: # what more I can do is, whatever i speak, it can start typing in the notepad
                # open_Notepad()
                execute_command('notepad')
            
            elif 'hi' in query or 'how are you' in query:
                speak("Hello sir, I am great. Thank you for asking. How are you?")
            
            elif 'i am good' in query or 'i am great' in query:
                speak("I am so glad to hear that. Hope you are having a lovely day!")
            
            elif 'open calculator' in query or 'open calc' in query: 
                # open_Calculator()
                execute_command('calc')

            elif 'open camera' in query: # what I can do more is, if i say 'click', the camera would capture the photo and store it in the specified folder
                open_camera()
                # execute_command('start camera')

            elif 'open chrome' in query: 
                # open_Chrome()
                execute_command('start chrome')
            
            elif 'open brave' in query:
                execute_command('start brave')
            
            elif 'open command prompt' in query or 'open cmd' in query:
                # open_cmd()
                execute_command('start cmd')

            elif "today's date" in query or "today's day" in query:
                now = datetime.now()
                today_date = now.date()
                today_day = datetime.now().strftime("%A")
                speak(f"Today's date is : {today_date}")
                print(today_date)
                speak(f"And, today's day is : {today_day}")
                print(today_day)
            
            elif 'current time' in query or 'time' in query:
                hour = datetime.now().hour
                minute = datetime.now().minute
                second = datetime.now().second
                microsecond = datetime.now().microsecond
                speak(f"Current time is : {hour}:{minute}:{second}.{microsecond}")
                print(f"Current time: {hour}:{minute}:{second}.{microsecond}")
            
            # elif 'screenshot' in query:

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f"Your IP Address is {ip_address}")
                speak("For your convenience, I am printing it on screen sir!")
                print(ip_address)
            
            elif 'wikipedia' in query:
                speak("What do you want to search on Wikipedia?")
                search_query = take_user_input().lower()
                results = search_on_wikipedia(search_query)
                speak(f"According to Wikipedia, {results}")
                speak("For your convenience, I am printing it on screen sir!")
                print(results)
                speak(f"For more information about {search_query}, you can read it on Wikipedia page itself!")
                execute_command(f'start https://en.wikipedia.org/wiki/{search_query.replace(" ", "_")}')

            elif 'youtube' in query:
                speak("What do you want to play on YouTube?")
                video = take_user_input().lower()
                play_on_youtube(video)
            
            elif 'search on google' in query:
                speak("What do you want to search on Google?")
                search_query = take_user_input().lower()
                search_on_google(search_query)
            
            elif 'send whatsapp message' in query:
                speak("On what number should I send the message?")
                number = input("Enter the number: ")
                speak("What is the message?")
                message = take_user_input().lower()
                send_whatsapp_message(number, message)
            
            elif 'send an email' in query:
                # ... (Get email details)
                # receiver_address = "shahpranshu2712@gmail.com"
                # subject = "Hi"
                # Message = "Hi"
                # send_email(receiver_address, subject, Message)
                # speak("I have sent the email.")
                speak("On what email address do I send sir? Please enter in the console : ")
                receiver_address = input("Enter the email address : ")
                speak("What should be the subject sir?")
                subject = take_user_input().capitalize()
                speak("What is the message sir?")
                Message = take_user_input().capitalize()
                if send_email(receiver_address, subject, Message):
                    speak("I have sent the email sir.")
                else:
                    speak("Something went wrong while I was sending an email sir. Please check the error log sir")

            elif 'joke' in query:
                speak("Hope you like this one!")
                joke = get_random_joke()
                speak(joke)
                pprint(joke)
            
            elif 'advice' in query:
                speak("Here's an advice for you!")
                advice = get_random_advice()
                speak(advice)
                pprint(advice)
            
            # elif 'trending movies' in query:
            #     # ... (Get trending movies)
            #     trending_movies = get_trending_movies()
            #     speak(f"Some of the trending movies are: {get_trending_movies()}")
            #     speak("For your convenience, I am print it on screen sir!")
            #     print(*get_trending_movies(), sep='\n')
            
            elif 'news' in query:
                speak("I am reading out the latest news headlines.")
                news_headlines = get_latest_news()
                speak(news_headlines)
                pprint(news_headlines)
            
            elif 'weather' in query:
                speak("Which city's weather report do you want?")
                city = take_user_input().lower()
                weather, temperature, feels_like = get_weather_report(city)
                speak(f"The current temperature is {temperature}, and it feels like {feels_like}. Weather type is : {weather}")
                pprint({"Description": weather, "Temperature": temperature, "and it feels like": feels_like})

            elif 'thank you' in query:
                speak("you are very welcome sir!")
            
            elif 'stop' in query or 'exit' in query or 'bye' in query:
                speak("Exiting the program! It was my pleasure that I could help you!")
                speak("Have a great day Sir!")
                break
        else:
            speak("Sorry I couldn't understand what you said. Could you please repeat again??")
