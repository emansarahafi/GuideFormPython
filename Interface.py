#Import necessary libraries
import tkinter as tk
import tkinter.ttk as ttk
import datetime as dt
import time
import numpy as np
import matplotlib.pylab as plt
import webbrowser
import json
import asyncio
import configparser
import PIL.Image
import os

from PIL import ImageTk, Image
from collections import Counter
from datetime import date, datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (PeerChannel)
from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import *
from tkinter.ttk import *
from time import strftime

#Create window
root = tk.Tk()

#Personalize the window 
root.title("GuideForm")

#Edit the window's size
root.geometry("1080x720")
root.minsize(480,360)
canvas = tk.Canvas(root, width='1080', height='720')
canvas.configure(bg='#DCDCDC',highlightthickness=0)
canvas.place(anchor='center')

#Create frame for logo's position
frame = Frame(root, width=50, height=50)
frame.pack()
frame.place(anchor='n', relx=0.5)

# Create an object of tkinter ImageTk
img= PIL.Image.open("/Users/emansarahafi/Downloads/Telegram Files for Project/GuideForm.png")

#Resize the Image using resize method
resized_image= img.resize((200,200), PIL.Image.Resampling.LANCZOS)
new_image= ImageTk.PhotoImage(resized_image)

# Create a Label Widget to display the text or Image
label = Label(frame, image = new_image)
label.pack()
 
#Add the window's icon 
root.iconbitmap("/Users/emansarahafi/Downloads/Telegram Files for Project/GuideForm.ico")

#Add the window's background 
root.config(background='#DCDCDC')

#Add decorative dashed line
canvas.create_line(540, 250, 540, 650, dash=(10), width=1)
canvas.pack()

# Create label for explanation
txt = tk.Label(root, text="""\nTashfeen Engineering Solutions is a geotechnical, civil engineering, and software development company
\nestablished in 2020.
\nIt has worked on several projects on national & international scales.  
\nThe engineering firm will start to expand overseas, and to do so,
\na survey must be done to understand the young engineers’ qualities overseas.
\nWe chose to begin with Bahrain because the kingdom has a well-established & most recognized
\nengineering infrastructure in the Middle East.
\nThus, kindly answer our survey on our application GuideForm for our research purposes.
\nFor any inquiries, please do not hesitate to contact us on our website.""",foreground="black", height=20, width=80)
txt.configure(background='#DCDCDC')
txt.place(relx = 0.5,rely = 0.5, anchor ='e')

# Create bottom label for company's name
def callback(url):
    webbrowser.open_new(url)

pwr = tk.Label(root, text="""Powered by
Tashfeen Engineering Solutions (2022)""", cursor="hand2", fg = "blue")
pwr.configure(background='#DCDCDC',underline=True)
pwr.place(relx = 0.5,rely = 0.95, anchor ='s')
pwr.bind("<Button-1>", lambda e: callback("https://tashfeen.tech/"))

# Create Label to display the Date
w = Label(root, text=f"{dt.datetime.now():%a, %b %d %Y}", foreground="black", background='#DCDCDC', font=("helvetica", 14))
w.place(relx = 0.0,rely = 0.0, anchor ='nw')

def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, time)
    
lbl = Label(root,foreground="black",background='#DCDCDC', font=("helvetica", 14))
lbl.place(relx = 1.0,rely = 0.0, anchor ='ne')
time()

# Create function to extract data from Telegram channel
def telegram():
   # some functions to parse json date
   class DateTimeEncoder(json.JSONEncoder):
       def default(self, o):
           if isinstance(o, datetime):
               return o.isoformat()

           if isinstance(o, bytes):
               return list(o)

           return json.JSONEncoder.default(self, o)

   # Reading Configs
   config = configparser.ConfigParser()
   config.read("/Users/emansarahafi/Downloads/Telegram Files for Project/config.ini")

   # Setting configuration values
   api_id = config['Telegram']['api_id']
   api_hash = config['Telegram']['api_hash']

   api_hash = str(api_hash)

   phone = config['Telegram']['phone']
   username = config['Telegram']['username']

   # Create the client and connect
   client = TelegramClient(username, api_id, api_hash)

   async def main(phone):
       await client.start()
       print("Client Created")
       me = await client.get_me()

       my_channel = await client.get_entity('Survey2022Channel')
       messages = await client.get_messages('Survey2022Channel')
       message = messages[0]
       textmsg = print(message.raw_text)  # raw_text for no formatting

   # For Users
       offset = 0
       limit = 100
       all_participants = []

       while True:
           participants = await client(GetParticipantsRequest(
               my_channel, ChannelParticipantsSearch(''), offset, limit,
               hash = 0
           ))
           if not participants.users:
               break
           all_participants.extend(participants.users)
           offset += len(participants.users)

       all_user_details = []
       for participant in all_participants:
           all_user_details.append(
               {"id": participant.id, "first_name": participant.first_name, "last_name": participant.last_name,
                "user": participant.username, "phone": participant.phone, "is_bot": participant.bot})

       with open('user_data.json', 'w') as outfile:
           json.dump(all_user_details, outfile)

   # For Messages
       offset_id = 0
       limit = 100
       all_messages = []
       total_messages = 0
       total_count_limit = 0

       while True:
           print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
           history = await client(GetHistoryRequest(
               peer = my_channel,
               offset_id = offset_id,
               offset_date = None,
               add_offset = 0,
               limit = limit,
               max_id = 0,
               min_id = 0,
               hash = 0
           ))
           if not history.messages:
               break
           messages = history.messages
           for message in messages:
               all_messages.append(message.to_dict())
           offset_id = messages[len(messages) - 1].id
           total_messages = len(all_messages)
           if total_count_limit != 0 and total_messages >= total_count_limit:
               break

       with open('channel_messages.json', 'w') as outfile:
           json.dump(all_messages, outfile, cls = DateTimeEncoder)

       # Convert JSON file to TXT
       filename = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.json"
       
       if os.path.exists("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"):
           os.remove("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
           with open(filename, 'r') as fr:
               pre_ = fr.read()
               lines = pre_.split('\n')
               new_filename = filename.split('.')[0]+".txt" # To keep the same name except ext
               with open(new_filename, "a") as fw:
                   fw.write("\n".join(lines))
       else:
           with open(filename, 'r') as fr:
               pre_ = fr.read()
               lines = pre_.split('\n')
               new_filename = filename.split('.')[0]+".txt" # To keep the same name except ext
               with open(new_filename, "a") as fw:
                   fw.write("\n".join(lines))

   with client:
       client.loop.run_until_complete(main(phone))

#Read TXT file to graph survey results

def agegraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()

        age = ['18-20', '21-29', '30-39', '40-49', '50 or above']
        agefreq=[]
        for k in age:
          agefreq.append(file.count(k))
        cb1 = plt.pie(agefreq, labels=age, autopct='%1.1f%%')
        plt.title("Age")
        
        plt.show()

def gendergraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()

        plt.figure()

        gender = ['Male', 'Female']
        genderfreq=[]
        for k in gender:
          genderfreq.append(file.count(k))
        cb2 = plt.pie(genderfreq, labels=gender, autopct='%1.1f%%')
        plt.title("Gender")

        plt.show()

def unigraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()

        plt.figure()

        uni = ['Ahlia University (AU)', 'American University of Bahrain (AUBH)', 'Applied Science University (ASU)', 'Arab Gulf University (AGU)', 'Arabian Open University (AOU)', 'Bahrain Institute of Banking and Finance (BIBF)', 'Bahrain Polytechnic (BP)', 'Bahrain Training Institute (BTI)', 'British University of Bahrain (BUB)', 'Gulf University (GU)', 'Kingdom University (KU)', 'Royal College of Surgeons in Ireland (RCSI) - Bahrain', 'Royal University for Women (RUW)', 'University College of Bahrain (UCB)', 'University of Bahrain (UOB)', 'University of Technology Bahrain (UTB)', 'Other University']
        unifreq=[]
        for k in uni:
          unifreq.append(file.count(k))
        unilabel = ['AU', 'AUBH', 'ASU', 'AGU', 'AOU', 'BIBF', 'BP', 'BTI', 'BUB', 'GU', 'KU', 'RCSI', 'RUW', 'UCB', 'UOB', 'UTB', 'Other']
        cb3 = plt.bar(unilabel, unifreq)
        plt.title('University')
        plt.xlabel('University')
        plt.ylabel('Frequency')

        plt.show()

def majorgraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()
        
        major = ['Aerospace Engineering', 'Agricultural Engineering', 'Architectural Engineering', 'Biological Engineering', 'Biomedical Engineering', 'Chemical Engineering', 'Civil Engineering', 'Computer Engineering', 'Computer Science', 'Electrical Engineering', 'Engineering Management', 'Industrial Engineering', 'Manufacturing Engineering', 'Marine Engineering', 'Materials Science', 'Mechanical Engineering', 'Mining Engineering', 'Nuclear Engineering', 'Petroleum Engineering', 'Software Engineering', 'Systems Engineering', 'Other Major']
        majorfreq=[]
        for k in major:
          majorfreq.append(file.count(k))
        majorlabel = ['Aerospace', 'Agricultural', 'Architectural', 'Biological', 'Biomedical', 'Chemical', 'Civil', 'CE', 'CS', 'EE', 'Engineering Management', 'IE', 'Manufacturing', 'Marine', 'Materials Science', 'Mechanical', 'Mining', 'Nuclear', 'Petroleum', 'Software', 'Systems', 'Other']
        cb4 = plt.bar(majorlabel, majorfreq)
        plt.title('Which major are you enrolled in?')
        plt.xlabel('Major')
        plt.ylabel('Frequency')

        plt.show()

def nextstepgraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()

        nextstep = ['Work on a start-up', 'Work at a company', 'Enroll for graduate studies', 'Take time off', 'Other next step']
        nextstepfreq=[]
        for k in nextstep:
          nextstepfreq.append(file.count(k))
        cb5 = plt.bar(nextstep, nextstepfreq)
        plt.title('What is your next step after graduating from university?')
        plt.xlabel('Next step')
        plt.ylabel('Frequency')

        plt.show()

def langgraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()

        lang = ['Blockchain', 'C', 'C++', 'HTML', 'Java', 'JavaScript', 'MATLAB', 'PHP', 'Python', 'Other language(s)']
        langfreq=[]
        for k in lang:
          langfreq.append(file.count(k))
        cb6 = plt.bar(lang, langfreq)
        plt.title('Languages and Frameworks known')
        plt.xlabel('Languages & Frameworks')
        plt.ylabel('Frequency')

        plt.show()

def wheregraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()
        
        where = ['College', 'Online', 'Self-taught', 'Other learning method']
        wherefreq=[]
        for k in where:
          wherefreq.append(file.count(k))
        cb7 = plt.bar(where, wherefreq)
        plt.title("From where did you learn the new language(s)?")
        plt.xlabel('Learning methods')
        plt.ylabel('Frequency')

        plt.show()

def timegraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()
        
        time = ['Less than half a year', 'Half a year', 'A year', 'More than a year']
        timefreq=[]
        for k in time:
          timefreq.append(file.count(k))
        cb8 = plt.pie(timefreq, labels=time, autopct='%1.1f%%')
        plt.title("How long did you spend learning the new language(s)?")

        plt.show()

def levelgraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()
        
        level = ['1 - Not really experienced with them', '2 - Good at them', '3 - Very experienced with them']
        levelfreq=[]
        for k in level:
          levelfreq.append(file.count(k))
        cb9 = plt.pie(levelfreq, labels=level, autopct='%1.1f%%')
        plt.title("How experienced are you at the language(s) you learned on a scale from 1 to 3?")

        plt.show()

def ansgraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()
        ans = ['Yes', 'No', 'Maybe']
        ansfreq=[]
        for k in ans:
          ansfreq.append(file.count(k))
        cb10 = plt.pie(ansfreq, labels=ans, autopct='%1.1f%%')
        plt.title("Does learning the new language(s) help you in a way in your career?")

        plt.figure()

def jobgraphs():
    #Read TXT file
    # check if size of file is 0
    file_path = "/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt"
    if os.stat(file_path).st_size == 0:
        errormsg = Label(root,text = "Data in unavailable at the moment", foreground="red",background='#DCDCDC', font=("helvetica", 10))
        errormsg.place(relx=0.75, rely=0.7, anchor=CENTER)
    else:
        #Read TXT file and graph the data
        fid=open("/Users/emansarahafi/Downloads/Telegram Files for Project/channel_messages.txt")
        file = fid.read()
        
        plt.figure()
        
        job = ['Application Developer', 'Computer Engineer', 'Data Scientist', 'Programmer', 'Web Designer', 'Other career option']
        jobfreq=[]
        for k in job:
          jobfreq.append(file.count(k))
        cb11 = plt.bar(job, jobfreq)
        plt.title("What are your future career goals?")
        plt.xlabel('Career options')
        plt.ylabel('Frequency')

        plt.show()

#Create functions to access links
def openwebsite():
   new = 1
   url = "https://tashfeen.tech/"
   webbrowser.open(url,new=new)

def appwebsite():
   new = 1
   url = "http://localhost/TashfeenUniForm/appwebsite.html"
   webbrowser.open(url,new=new)

def brochure():
   new = 1
   url = "http://localhost/TashfeenUniForm/guideform.pdf"
   webbrowser.open(url,new=new)
   
def openform():
   new = 1
   url = "http://localhost/TashfeenUniForm/appsurvey.html"
   webbrowser.open(url,new=new)

#Create buttons for the interface
form_button = tk.Button(root,
                   text="Access the survey",
                   width=20,height=2,
                   command=openform)

website_button = tk.Menubutton(root,
                   text="Access the links",
                   width=20,height=2)
website_button.menu = Menu(website_button)

data_button = tk.Menubutton(root,
                   text="Access the data",
                   width=20,height=2)
data_button.menu = Menu(data_button)

#Personalize drop down menu for websites
website_button["menu"] = website_button.menu
website_button.menu.add_checkbutton(label="The application", command=appwebsite)
website_button.menu.add_checkbutton(label="The brochure", command=brochure)
website_button.menu.add_checkbutton(label="The company", command=openwebsite)

#Personalize drop down menu for data
data_button["menu"] = data_button.menu
data_button.menu.add_checkbutton(label="Age", command=lambda:[telegram(), agegraphs()])
data_button.menu.add_checkbutton(label="Gender", command=lambda:[telegram(), gendergraphs()])
data_button.menu.add_checkbutton(label="University", command=lambda:[telegram(), unigraphs()])
data_button.menu.add_checkbutton(label="Major", command=lambda:[telegram(), majorgraphs()])
data_button.menu.add_checkbutton(label="Next step", command=lambda:[telegram(), nextstepgraphs()])
data_button.menu.add_checkbutton(label="Languages known", command=lambda:[telegram(), langgraphs()])
data_button.menu.add_checkbutton(label="Learning method", command=lambda:[telegram(), wheregraphs()])
data_button.menu.add_checkbutton(label="Learning duration", command=lambda:[telegram(), timegraphs()])
data_button.menu.add_checkbutton(label="Experience rating", command=lambda:[telegram(), levelgraphs()])
data_button.menu.add_checkbutton(label="Tools & Career", command=lambda:[telegram(), ansgraphs()])
data_button.menu.add_checkbutton(label="Future career", command=lambda:[telegram(), jobgraphs()])

#Buttons' Positions
form_button.place(relx=0.75, rely=0.4, anchor=CENTER)
website_button.place(relx=0.75, rely=0.5, anchor=CENTER)
data_button.place(relx=0.75, rely=0.6, anchor=CENTER)


root.mainloop()
