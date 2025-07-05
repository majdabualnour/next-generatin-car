import speech_recognition as sr
import pyttsx3
#import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser as web
import test
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        
        r.adjust_for_ambient_noise(source)
        print("Please say something ")
        audio = r.listen(source)
        print("Reconizing Now ... ")
        try:
            hhhh = r.recognize_google(audio)
            hhhh = hhhh.lower()
            if 'run' in hhhh:
                hhhh = hhhh.replace('run', '')
                print(hhhh)
            print("You have said : " +hhhh)
        except Exception as e:
            print("Error : " + str(e))
    return hhhh
    
def run_alexa():
    talk('what do you what me to do for you')
    command = main()
    print(command)
    # if 'play' in command:
        
    #     song = command.replace('play', '')
    #     talk('playing ' + song)
    #     pywhatkit.playonyt(song)
    #     print('playing ' + song)

        
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        print('Current time is ' + time)
        test.signlang('Current time is ' + time)
        
    elif 'youtube' in command:
        talk('opening youtupe')

        
        print('opening youtupe')
        web.open("https://www.youtube.com")


    elif 'search' in command:
        link = 'https://www.google.com/search?q={}'.format(command)
        web.open(link)
        m=('searching abuot:{}'.format(command))
        talk('search abuot:{}'.format(command))
        print('search abuot:{}'.format(command))

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info) 
        #test.signlang(info)        
    elif 'date' in command:
        date = datetime.datetime.now().strftime('%A,%d,%B,%Y')
        talk('its ' + date)
        test.signlang('its ' + date)  
        print('its ' + date)
    elif 'i love you' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
          
        talk(pyjokes.get_joke())
        test.signlang(pyjokes.get_joke())  
    elif 'facebook' in command:
        talk('opening facebook')
    elif 'self mode' in command:
        
        talk('self mode on')
        return 'self'
    elif 'save mode' in command:
        talk('save mode on')
        return 'save'
    elif 'turn left' in command:
        talk('turning left')
        return'ofl'
    elif 'turn right' in command:
        talk('turning right')
        return 'ol'
    elif 'go straight' in command:
        talk('go straight')
        return 'os'    
    elif 'open the back' in command:
        talk('opening the back')
        return 'ob'
    elif 'open the door' in command:
        talk('opening the door')
        return 'od'   
    elif 'closing the back' in command:
        talk('opening the back')
        return 'cb'
    elif 'close the door' in command:
        talk('closing the door')
        return 'cd'       
    # elif 'air' in command:
        
    #     if 'turn on' in command:
    #         talk('turning on the Air conditioning')
    #         return 'oa'
    #     elif 'off' in command:
    #         talk('turning off the Air conditioning')
    #         return 'ofa'
    # elif 'pump' in command:
        
    #     if 'on' in command:
    #         talk('turning on the pump')
    #         return 'op'
    #     elif 'off' in command:
    #         talk('turning off the pump')
    #         return 'ofp'
    # elif 'house' in command:
        
    #     if 'on' in command:
    #         talk('turning on the house')
    #         return 'oh'
    #     elif 'off' in command:
    #         talk('turning off the house')
    #         return 'ofh'
    else:
        talk('Please say the command again.')
