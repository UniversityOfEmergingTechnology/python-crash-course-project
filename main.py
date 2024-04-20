import os
import speech_recognition as sr
from gtts import gTTS
import webbrowser
import datetime
from openai import OpenAI
from config import apikey

client = OpenAI(api_key = apikey)

def say(text):
    tts = gTTS(text=text , lang='en')
    tts.save("speech.mp3")
    os.system("afplay speech.mp3")

def chat(prompt):
    chat = f"Mudit : {prompt}\n"
    print(chat)
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if response.choices:
        responseAudio = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=response.choices[0].message.content,  
        )
        chat = f"AI : {response.choices[0].message.content}\n"
        print(chat) 
        responseAudio.stream_to_file("output.mp3")
        os.system("afplay output.mp3")


def ai(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if response.choices:
        message_content = response.choices[0].message.content
        print(message_content)
    else:
        print("No response received")
        return
    
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    
    answer = response.choices[0].message.content

    with open(f"Openai/{''.join(prompt.split("intelligence")[1:]).strip()}.txt","w") as f:
        f.write(answer)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio , language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        say("Say that again please...")
        return "None"
    return query
 

if __name__ == '__main__':
    say("Hello , I am a virtual assistant. How can I help you?")
    while True:
        query = takeCommand()
        sites = [
            ["youtube", "https://www.youtube.com/"] , 
            ["google" , "https://www.google.com/"] , 
            ["github" , "https://www.github.com/"]
        ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir")
                webbrowser.open(site[1])

        if "open music".lower() in query.lower():
            musicPath = ""
            os.system(f"open {musicPath}")

        elif "the time".lower() in query.lower():
            time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {time}")
        
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "using artificial intelligence".lower() in query.lower():
            ai(query)
        elif "exit".lower() in query.lower():
            say("Goodbye sir Have a nice day")
            exit()
        else:
            say("Chatting")
            chat(query)