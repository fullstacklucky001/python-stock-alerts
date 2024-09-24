import subprocess

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True

def playsound():
    process = subprocess.Popen(['./play-sound.sh'])        

def format_currency(value):
    return f"${value:,.2f}" if value == round(value, 2) else f"${value:,.5f}".rstrip('0').rstrip('.')

