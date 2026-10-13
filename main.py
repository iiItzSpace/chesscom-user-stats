import sys
import json
import urllib.request
import urllib.error

import os
if os.name == 'nt':
    import msvcrt
else:
    import termios

def clear_input_buffer():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def get_stats(user):
    url = f"https://api.chess.com/pub/player/{user}/stats"
    headers = {"User-Agent": "chess.com-user-stats-cli/1.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            print("user exists")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error 404: User {user} doesn't exist on Chess.com.")
        elif e.code == 410:
            print(f"Error 410: Data for {user} is permanently unavailable.")
        elif e.code == 429:
            print(f"Error 429: Too many requests for {user}. Please wait.")
        else:
            print(f"Error: API returned HTTP {e.code}.")
        return None

def display_stats():
    pass

def main():
    print("== Chess.com User Stats ==")

    while True:
        user = input("\nType the username: ").strip()
        if not user:
            print("You didn´t enter an username")
            continue

        print(f"Fetching data for {user}...", flush=True)
        stats = get_stats(user)

        while True:
            clear_input_buffer()
            repeat = input("Do you want to search another user? (Y/n): ").strip().lower()
            if repeat in ["n", "no"]:
                print("Goodbye!")
                return
            elif repeat in ["y", "yes", ""]:
                break
            else:
                print("Invalid input! Please type Y or n.")

if __name__ == "__main__":
    sys.exit(main())