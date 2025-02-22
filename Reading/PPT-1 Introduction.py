import pyttsx3

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    new_voice_rate = 100
    engine.setProperty('rate', new_voice_rate)
    engine.setProperty('voice', voice[1].id)
    engine.say(audio)
    engine.runAndWait()

phase = '''
Hello everyone, welcome. 
I’m here today to talk to you about the API (Application Programming Interface). An API is a set of instructions and standards that allows applications to interact with each other. APIs are used by a wide variety of software applications, including web browsers, mobile apps, and enterprise software.
EiPaaS is a type of integration platform that is designed to be embedded into other applications. Eipaas APIs provide a way for developers to easily integrate eiPaas functionality into their applications. Here, we will not dive into much further on development part but mainly focus on support scope.
EiPaaS (Enterprise Integration Platform as a Service) and APIs (Application Programming Interfaces) have a close relationship. In summary, EiPaaS utilizes APIs to achieve its core function of enterprise application integration. APIs are the essential communication tools that power the integrations built within the EiPaaS platform.
Feel free let me know if you have any questions and concerns. 

'''

speak(phase)
