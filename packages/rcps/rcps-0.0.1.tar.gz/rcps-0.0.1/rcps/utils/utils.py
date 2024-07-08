import subprocess
from termcolor import colored
from rcps.utils._constant import _BANNER

def print_colored(text, color='green'):
    print(colored(text, color))
    
def load_menu():
    while 1:
        print("\033[H\033[J", end="")
    
        print_colored(f"""{_BANNER}    
            1. Start Server
            2. Start Client
            3. Key Logger
            4. Capture Screen
            5. Store IP
            6. Exit
            """)
            
        user_choice = input("-> ")
        
        if user_choice != "":
            return user_choice
        
        
def _run_command(command):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, text=True).stdout.read()
        return str(process)+"\n"
    
    except subprocess.CalledProcessError as e:
            return f"Error: {e}"

def get_ips():
    command = ['ipconfig', '|', 'findstr', '/i', 'ipv4']
    ip = _run_command(command)
    
    return [i.split(':')[1].strip() for i in ip.split('\n') if i != '']


if __name__ == "__main__":
    print(get_ips())