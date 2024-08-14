import os
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import json
from PIL import Image, ImageTk
from dotenv import load_dotenv

load_dotenv()

Base_URL = os.getenv('Base_URL')
key = os.getenv('key')
key2 = os.getenv('key2')

#sample
#http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=bulk

#sample historical

#base url of weater api
Base_URL = Base_URL
#api key
key = key
location = input("INPUT AREA FOR LOOKUP:")

url = Base_URL + "/forecast.json?key=" + key + "&q=" + location + "," "ON&days=5&aqi=no&alerts=no"
print(url)

#NEWS: sample:
news_headline_url = "https://newsapi.org/v2/everything?"
key2 = key2
url2 = (news_headline_url + 'q=' + location + '&' + 'apiKey=' + key2)
print(url2)

response = requests.get(url2)
parsed_news = response.json()
news = []


for article_data in parsed_news['articles']:
    title = article_data['title']
    url3 = article_data['url']
    description = article_data['description']
    print(article_data['title'],"\n",article_data['url'])
    news.append(title + "\n" + str(description) + "\n")


response = requests.get(url)
parsed_data = response.json()
print(parsed_data['location']['name'])
print(f"Current temperature: {parsed_data['current']['temp_c']}°C")
print(f"Condition: {parsed_data['current']['condition']['text']}")



# Extract the dates and temperatures for the next 5 days
dates = []
temps = []

for forecast in parsed_data['forecast']['forecastday']:
    date = forecast['date']
    temp_c = forecast['day']['avgtemp_c']
    dates.append(date)
    temps.append(temp_c)

# Plotting the graph
fig = Figure(figsize=(6.2,3))
ax = fig.add_subplot(111)
ax.plot(dates, temps, marker='D')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.set_title('3-Day Forecast for ' + location)
ax.grid(True)
#plt.tight_layout()


window = tk.Tk()
window.title("Weather APP-ELVIS")

def news_update():
    url2 = news_headline_url + 'q=' + location_entry.get() + '&' + 'apiKey=' + key2
    response = requests.get(url2)
    parsed_news = response.json()

    news_label.delete('1.0', tk.END)

    for article_data in parsed_news['articles']:
        title = article_data['title']
        description = article_data['description']
        news_label.insert(tk.END, f"{title}\n{description}\n\n")
def graph_update():
    url = Base_URL + "/forecast.json?key=" + key + "&q=" + location_entry.get() + "," "ON&days=5&aqi=no&alerts=no"
    response = requests.get(url)
    parsed_data = response.json()
    dates = []
    temps = []

    for forecast in parsed_data['forecast']['forecastday']:
        date = forecast['date']
        temp_c = forecast['day']['avgtemp_c']
        dates.append(date)
        temps.append(temp_c)

    #clearing existing graph
    ax.clear()
    # Plotting new graph
    ax.plot(dates, temps, marker='D')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('5-Day Forecast for ' + location_entry.get())
    ax.grid(True)

def action():
    news_update()
    graph_update()
    canvas.draw()

#image
# Open the PNG image file
# Directory where your image is located
#directory = r"C:\Users\Elvis.Eziokwu\Downloads" - old directory
directory = r"C:\Users\elvis\Downloads"    #new directory
# Image file name
filename = "weather.png"

# Construct the full path
image_path = os.path.join(directory, filename)
png_image = Image.open(image_path)
# Convert the PIL image to a tkinter-compatible format
tk_image = ImageTk.PhotoImage(png_image)

'''
left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, side=tk.TOP, expand=True)

image_label = tk.Label(left_frame, text="Picture", bg="#2E8BC0")
image_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
image_label.configure(image=tk_image)
image_label.image = tk_image

right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

button = tk.Button(master=right_frame, text="SEARCH",width=15,height=2,bg="#145DA0",fg="white",command=action)
button.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

location = tk.Label(master=right_frame, text="LOCATION LOOKUP",foreground="black", background="#B1D4E0",width=50, height=4)
location.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

#creat entry
location_entry = tk.Entry(master=right_frame, fg="blue", bg="white", width=50)
location_entry.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


news_label = tk.Label(master=right_frame, text=news[:10], foreground="white", background="#0C2D48", width=100, height=100)
news_label.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

'''
left_frame = tk.Frame(window)
left_frame.grid(row=0, column=0, sticky="nsew")

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

image_label = tk.Label(left_frame, text="Picture", bg="#2E8BC0")
image_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
image_label.configure(image=tk_image)
image_label.image = tk_image

right_frame = tk.Frame(window)
right_frame.grid(row=0, column=1, sticky="nsew")

location = tk.Label(master=right_frame, text="LOCATION LOOKUP",foreground="black", background="#B1D4E0",width=50, height=4)
location.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

location_entry = tk.Entry(master=right_frame, fg="black", bg="white", width=50)
location_entry.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

button = tk.Button(master=right_frame, text="SEARCH",width=15,height=2,bg="#145DA0",fg="white",command=action)
button.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

news_label = tk.Text(master=right_frame, wrap=tk.WORD, foreground="white", background="#0C2D48", width=100, height=100)
news_label.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

# Configure row and column weights for resizing
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
'''
# Initial news text
news_headline_url = "https://newsapi.org/v2/everything?"
key2 = key2
url2 = news_headline_url + 'q=' + location + '&' + 'apiKey=' + key2
response = requests.get(url2)
parsed_news = response.json()

for article_data in parsed_news['articles']:
    title = article_data['title']
    description = article_data['description']
    news_label.config(text=f"{title}\n{description}\n\n")
'''
# Update the news_label text widget with initial news


window.mainloop()