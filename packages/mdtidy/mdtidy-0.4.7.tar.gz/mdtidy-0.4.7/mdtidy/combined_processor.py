from mdtidy.gemini_processor import process_gemini_conversation
from mdtidy.gpt_processor import process_gpt_conversation
import re
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

def print_welcome_message():
    welcome_art = r"""
    __  __ _____ _____ _     _       
   |  \/  |  __ \_   _(_)   | |      
   | \  / | |  | || |  _  __| |_   _ 
   | |\/| | |  | || | | |/ _` | | | |
   | |  | | |__| || |_| | (_| | |_| |
   |_|  |_|_____/_____|_|\__,_|\__, |
                                __/ |
                               |___/ 
    """
    print(Fore.CYAN + welcome_art)
    print(Fore.GREEN + "Welcome to MDtidy!".center(50))
    print(Fore.YELLOW + "This tool processes GPT and Gemini conversation data into structured Jupyter notebooks.".center(50))
    print(Fore.MAGENTA + "Please enter the conversation URL to begin or type 'exit' to quit.".center(50))
    print("\n" + "=" * 50 + "\n")

def print_farewell_message():
    farewell_art = r"""
       ______                ____            _ 
      |  ____|              |  _ \          | |
      | |__ __ _ _ __ ___   | |_) |_   _  __| |
      |  __/ _` | '__/ _ \  |  _ <| | | |/ _` |
      | | | (_| | | |  __/  | |_) | |_| | (_| |
      |_|  \__,_|_|  \___|  |____/ \__,_|\__,_|
                                               
    """
    print(Fore.CYAN + farewell_art)
    print(Fore.YELLOW + "Thanks for using MDtidy!".center(50))
    print(Fore.GREEN + "We hope you found it helpful.".center(50))
    print(Fore.MAGENTA + "Have a great day and happy data processing!".center(50))
    print("\n" + "=" * 50 + "\n")

def process_conversation() -> None:
    print_welcome_message()

    def get_url_and_process():
        while True:
            url = input(Fore.CYAN + "Enter the conversation URL (or type 'exit' to quit): " + Style.RESET_ALL).strip()
            if url.lower() == 'exit':
                return None
            if re.match(r'^https://chatgpt\.com/share/[0-9a-fA-F-]{36}$', url):
                print(Fore.GREEN + "\nProcessing GPT conversation...")
                process_gpt_conversation(url)
                return "GPT"
            elif re.match(r'^https://g.co/gemini/share/[a-zA-Z0-9]+$', url):
                print(Fore.GREEN + "\nProcessing Gemini conversation...")
                process_gemini_conversation(url)
                return "Gemini"
            else:
                print(Fore.RED + "\nInvalid URL format. Please enter a valid GPT or Gemini conversation URL or type 'exit' to quit.")

    first_type = get_url_and_process()
    if not first_type:
        print_farewell_message()
        return

    while True:
        proceed = input(Fore.CYAN + "Would you like to process another conversation? (yes/no): " + Style.RESET_ALL).strip().lower()
        if proceed == 'no':
            print_farewell_message()
            break
        elif proceed == 'yes':
            second_type = get_url_and_process()
            if not second_type:
                print_farewell_message()
                break
        else:
            print(Fore.RED + "\nInvalid response. Please enter 'yes' or 'no'.")
