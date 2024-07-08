import time
import random

"""
        .--'''''''''--.
     .'      .---.      '.
    /    .-----------.    \\
   /        .-----.        \\
   |       .-.   .-.       |
   |      /   \ /   \      |
    \    | .-. | .-. |    /
     '-._| | | | | | |_.-'
         | '-' | '-' |
          \___/ \___/
       _.-'  /   \  `-._
     .' _.--|     |--._ '.
     ' _...-|     |-..._ '
            |     |
            '.___.'
              | |
             _| |_
"""
    

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 2907
CLIENT_HOST = None
CLIENT_PORT = 2907


# _BANNER = f"""
# 01110010 01100011 01110000 01110011 01110010 01100011  
# {_LOGO}                                                     
# 01110010 01100011 01110000 01110011 01110010 01100011 
# """

_LOGO_OLD = """
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓███████▓▒░      
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓███████▓▒░ ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓███████▓▒░  
"""

_BANNER = """
 _ __ ___ _ __  ___ 
| '__/ __| '_ \/ __|
| | | (__| |_) \__ \\
|_|  \___| .__/|___/
         |_|        
"""

WELCOME_MESSAGE = f"""{_BANNER}

RCPS is a simple and lightweight tool to control remote devices connected over the same network.
"""

DOCS = """
Server side documentation:\n
    To launch the server side script, use the -s flag.\n
    Use the The ip address and port.\n\nExample usage:\n\nrcps -c -i 246.53.232.17 -p 8888
    For now, please visit the following link:\n
        https://youtu.be/-p0a9BJTEvA\n

Client side documentation:\n
    To launch the server side script, use the -c flag.\n
    Use the The ip address and port.\n\nExample usage:\n\nrcps -c -i 246.53.232.17 -p 8888
    For now, please visit the following link:\n
        https://youtu.be/-p0a9BJTEvA\n
"""

def animate(string):
  print("\033[H\033[J", end="")
  
  lines = string.split('\n')
  rnd = random.randint(0, len(lines))-1
  lines[rnd] = "   "*random.randint(0,3)+lines[rnd]
  print("\n".join(lines))
  
  time.sleep(random.uniform(0.05, 0.1))
  print("\033[H\033[J", end="")
  print(string)



if __name__ == '__main__':
  from termcolor import colored
  
  def print_colored(text, color='green'):
    print(colored(text, color))

  # while 1:
    # animate(_LOGO)
  
  print("\033[H\033[J", end="")
  print_colored(WELCOME_MESSAGE)
  
  