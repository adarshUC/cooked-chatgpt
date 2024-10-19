import os
import shutil
import requests
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def center_text(text):
    # Get the terminal size
    terminal_size = shutil.get_terminal_size(fallback=(80, 20))  # Default size if can't get
    width = terminal_size.columns
    
    # Calculate the number of spaces needed to center the text
    padding = (width - len(text)) // 2
    return ' ' * padding + text

def receive_api():
    api_key = os.getenv("MIMO_OPENAI_API_KEY")
    if api_key:
        print(f"{Fore.GREEN}API Key successfully retrieved: {api_key}")
    else:
        print(f"{Fore.RED}MIMO_OPENAI_API_KEY is not set. Please set it in your environment variables.")

def send_message(user_message, thread_id, api_key):
    url = "https://ai.mimo.org/v1/openai/message"
    headers = {"api-key": api_key}
    body = {"message": user_message}

    if thread_id:
        body["threadId"] = thread_id
        
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        print(f"{Fore.RED}Error: Received status code {response.status_code}")
        print(response.text)
        return None
    
    return response.json()

def main():
    # Load environment variables from .env file
    load_dotenv("D:\\Telegram Desktop\\secret.env")
    
    api_key = os.getenv("MIMO_OPENAI_API_KEY")

    if not api_key:
        return  # Exit if the API key is not set

    current_thread_id = None

    # Centered welcome message and instructions
    print(center_text(f"{Fore.GREEN}Welcome! Type your message and press Enter to send."))
    print(center_text(f"{Fore.CYAN}Type 'exit' to end the program."))
    print(center_text(f"{Fore.CYAN}Type 'new' to switch conversation thread."))
    print(center_text(f"{Fore.CYAN}Starting a new thread for you.\n"))

    while True:
        print(Fore.YELLOW + "You: ", end='')  # Print "You: " in yellow
        user_message = input()  # Take user input without color
        
        if user_message.lower() == "exit":
            break
        elif user_message.lower() == "new":
            current_thread_id = None
            print(center_text(f"{Fore.YELLOW}Started a new thread."))
            continue
        
        response_data = send_message(user_message, current_thread_id, api_key)

        if response_data:
            latest_message = response_data.get("response", "Error: No 'response' field found in API response.")
            current_thread_id = response_data.get("threadId")
            print(f"{Fore.MAGENTA}GPT: {latest_message}")
        else:
            print(f"{Fore.RED}Error: No valid response data received.")

if __name__ == "__main__":
    main()
