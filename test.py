import subprocess

def playsound(text):
    command = 'speak.py "' + text + '"' 
    process = subprocess.Popen(['python', 'speak.py', 'text'])

playsound('hello')