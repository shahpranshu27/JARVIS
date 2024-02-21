import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
import ssl
# J.A.R.V.I.S. project with functionalities open camera, open chrome, open cmd, find ip address, get trending movies, get latest news, get joke, get advice, send message on whatsapp, send email,  get current weather report, search on google, search on wikipedia, play video on youtube made in python

def find_my_ip():
    ip_address = requests.get("https://api64.ipify.org?format=json").json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query,sentences = 2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")
def send_email(reciever_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = reciever_address
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        # ssl : secure sockets layer -> ssl.create_default_context() is a valuable tool for establishing secure network connections in Python applications, simplifying the process while upholding security best practices.
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
            # s.starttls()
            s.login(EMAIL, PASSWORD)
            # s.send_message(email)
            s.sendmail(EMAIL, reciever_address, email.as_string())
        
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending an email : {e}")
        return False

NEWS_API_KEY = config("NEWS_API_KEY")

def get_latest_news():
    news_headlines = []
    params = {'language' : 'en'}
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country?=in&apiKey={NEWS_API_KEY}&category=general", params).json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")

def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

# TMDB_API_KEY = config("TMDB_API_KEY")

# def get_trending_movies():
    # trending_movies = []
    # res = requests.get(
    #     f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    # results = res["results"]
    # for r in results:
    #     trending_movies.append(r["original_title"])
    # return trending_movies[:5]
    # trending_movies = []
    # url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"

    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()  # Raise an exception for non-200 status codes
    #     data = response.json()
    #     results = data["results"]
    #     for r in results:
    #         trending_movies.append(r["original_title"])
    #     return trending_movies[:5]

    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching trending movies: {e}")
    #     return None
    
    # except requests.exceptions.RequestException as e:
    #     print(f"General error fetching trending movies: {e}")  # Catch other potential errors
    #     return None

def get_random_joke():
    headers = {'Accept': 'application/json'}
    res = requests.get("https://icanhazdadjoke.com/", headers=headers)
    # status code 200 -> It indicates that the request was successful, and the server has returned the requested information
    if res.status_code == 200:
        try:
            return res.json()["joke"]
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON. Response content:", res.content)
    else:
        print(f"Failed to retrieve joke. Status code: {res.status_code}")

    return "Sorry, couldn't fetch a joke at the moment."
