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
    padding = (width - len(text)) // 2
    return ' ' * padding + text

def receive_api():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"{Fore.GREEN}API Key successfully retrieved: {api_key}")
    else:
        print(f"{Fore.RED}OPENAI_API_KEY is not set. Please set it in your environment variables.")

def send_message(user_message, thread_id, api_key):
    url = "https://api.openai.com/v1/completions"
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

def save_thread_id(thread_id, filename="thread_id.txt"):
    if thread_id:
        with open(filename, "w") as f:
            f.write(thread_id)

def load_thread_id(filename="thread_id.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read().strip()
    return None

def main():
    load_dotenv("D:\\Telegram Desktop\\secret.env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(f"{Fore.RED}API Key not found. Exiting.")
        return  # Exit if the API key is not set

    thread_file = "thread_id.txt"
    current_thread_id = load_thread_id(thread_file)

    # Centered welcome message and instructions
    print(center_text(f"{Fore.GREEN}Welcome! Type your message and press Enter to send."))
    print(center_text(f"{Fore.CYAN}Type 'exit' to end the program."))
    print(center_text(f"{Fore.CYAN}Type 'new' to switch conversation thread."))
    if current_thread_id:
        print(center_text(f"{Fore.CYAN}Continuing previous thread.\n"))
    else:
        print(center_text(f"{Fore.CYAN}Starting a new thread for you.\n"))

    while True:
        print(Fore.YELLOW + "You: ", end='')
        user_message = input()

        if user_message.lower() == "exit":
            save_thread_id(current_thread_id, thread_file)
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
