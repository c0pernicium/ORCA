import time
import os
import multiprocessing
import socket
from datetime import datetime
import pytz
import re
import requests

start_time = time.time()

def color_orca(text):
    return text.replace("ORCA", "\033[95mORCA\033[0m")

def color_text(text):
    text = re.sub(r"(\d+(\.\d+)?)", r"\033[93m\1\033[0m", text)  
    text = re.sub(r"(\(|\))", r"\033[38;5;214m\1\033[0m", text)  
    return text

def show_info():
    banner = [
        r"   ____  ____  _________ ",
        r"  / __ \/ __ \/ ____/   |",
        r" / / / / /_/ / /   / /| |",
        r"/ /_/ / _  _/ /___/ ___ |",
        r"\____/_/ |_|\____/_/  |_|",
        r"                          "
    ]

    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    sys_info = [
        "\033[95mORCA Version 0.0.1\033[0m",
        f"\033[92mUptime: {hours}h {minutes}m {seconds}s\033[0m",
        f"\033[91mCPU Cores: {multiprocessing.cpu_count()}\033[0m",
        f"\033[94mCWD: {os.getcwd()}\033[0m",
        f"\033[96mHostname: {socket.gethostname()}\033[0m"
    ]

    max_banner_width = max(len(line) for line in banner) + 10

    for i in range(len(banner)):
        left = "\033[95m" + banner[i] + "\033[0m"
        right = sys_info[i] if i < len(sys_info) else ""
        print(f"{left.ljust(max_banner_width)}{right}")

    print("")

def main():
    print(color_orca("Welcome to ORCA"))

    while True:
        try:
            command = input("> ").strip()
        except KeyboardInterrupt:
            print()
            continue

        if command == "":
            print("\033[2J\033[H", end="")
            continue

        if command.lower() == "help":
            print(color_orca("ORCA Help Menu"))
            print(color_orca("echo") + "    - Repeat given text")
            print(color_orca("clear") + "   - Clear the screen")
            print(color_orca("quit") + "    - End the session")
            print(color_orca("info") + "    - Show ORCA info")
            print(color_orca("calc") + "    - Simple calculator")
            print(color_orca("time") + "    - Show current time")
            print(color_orca("new") + "     - Create a new file")
            print(color_orca("open") + "    - Display file contents")
            print(color_orca("write") + "   - Append text to a file")
            print(color_orca("delete") + "  - Delete a file")
            print(color_orca("fetch") + "   - Fetch data from a URL")
            print(color_orca("list") + "    - List system files")
            continue

        if command.lower() == "quit":
            print(color_orca("Exiting ORCA. Goodbye!"))
            break

        if command.lower() == "clear":
            print("\033[2J\033[H", end="")
            continue

        if command.lower() == "info":
            show_info()
            continue

        if command.startswith("echo"):
            rest = command[4:].strip()
            if not rest.startswith("(") or not rest.endswith(")"):
                print("Usage: echo (text)")
                continue
            text = rest[1:-1]
            print(color_text(color_orca(text)))
            continue

        if command.startswith("calc"):
            parts = command[4:].strip().split()
            if len(parts) != 3:
                print("Usage: calc number operator number (e.g., calc 5 + 3)")
                continue
            try:
                num1 = float(parts[0])
                op = parts[1]
                num2 = float(parts[2])
                if op == "+":
                    result = num1 + num2
                elif op == "-":
                    result = num1 - num2
                elif op == "*":
                    result = num1 * num2
                elif op == "/":
                    if num2 == 0:
                        print("Error: Division by zero")
                        continue
                    result = num1 / num2
                else:
                    print("Invalid operator. Use +, -, *, /")
                    continue
                print(color_text(f"Result: {result}"))
            except ValueError:
                print("Invalid numbers. Usage: calc number operator number")
            continue

        if command.lower() == "time":
            central = pytz.timezone("US/Central")
            now = datetime.now(central)
            print(color_text(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"))
            continue

        if command.startswith("new"):
            rest = command[3:].strip()
            if not rest.startswith("(") or not rest.endswith(")"):
                print("Usage: new (filename)")
                continue
            filename = rest[1:-1].strip()
            if os.path.exists(filename):
                print(f"File '{filename}' already exists.")
                continue
            open(filename, "w").close()
            print(f"File '{filename}' created.")
            continue

        if command.startswith("open"):
            rest = command[4:].strip()
            if not rest.startswith("(") or not rest.endswith(")"):
                print("Usage: open (filename)")
                continue
            filename = rest[1:-1].strip()
            if not os.path.exists(filename):
                print(f"File '{filename}' does not exist.")
                continue
            with open(filename, "r") as f:
                content = f.read()
            print(color_text(content))
            continue

        if command.startswith("write"):
            parts = re.findall(r"\((.*?)\)", command)
            if len(parts) != 2:
                print("Usage: write (filename) (text_to_append)")
                continue
            filename, text = parts
            if not os.path.exists(filename):
                print(f"File '{filename}' does not exist.")
                continue
            with open(filename, "a") as f:
                f.write(text + "\n")
            print(f"Text appended to '{filename}'.")
            continue

        if command.startswith("delete"):
            rest = command[6:].strip()
            if not rest.startswith("(") or not rest.endswith(")"):
                print("Usage: delete (filename)")
                continue
            filename = rest[1:-1].strip()
            if not os.path.exists(filename):
                print(f"File '{filename}' does not exist.")
                continue
            os.remove(filename)
            print(f"File '{filename}' deleted.")
            continue

        if command.startswith("fetch"):
            parts = re.findall(r"\((.*?)\)", command)
            if len(parts) != 1:
                print("Usage: fetch (url)")
                continue
            url = parts[0].strip()
            if not url:
                print("URL cannot be empty.")
                continue
            try:
                headers = {"User-Agent": "ORCA Shell/0.0.1"}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    import json
                    print(json.dumps(response.json(), indent=4))
                else:
                    print(response.text)
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch URL: {e}")
            continue

        if command.lower() == "list":
            files = os.listdir()
            for f in files:
                print(f)
            continue

        if command:
            print(color_text(color_orca(f"Unknown command: {command}. Type 'help' for commands.")))

if __name__ == "__main__":
    main()
