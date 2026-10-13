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


def get_stats(user: str) -> dict | None:
    url = f"https://api.chess.com/pub/player/{user}/stats"
    headers = {"User-Agent": "chess.com-user-stats-cli/1.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error 404: User {user} doesn't exist on Chess.com.\n")
        elif e.code == 410:
            print(f"Error 410: Data for {user} is permanently unavailable.\n")
        elif e.code == 429:
            print(f"Error 429: Too many requests for {user}. Please wait.\n")
        else:
            print(f"Error: API returned HTTP {e.code}.\n")
        return None


def display_stats(user: str, stats: dict) -> None:
    rapid = stats.get("chess_rapid", {}).get("last", {}).get("rating", "N/A")
    blitz = stats.get("chess_blitz", {}).get("last", {}).get("rating", "N/A")
    bullet = stats.get("chess_bullet", {}).get("last", {}).get("rating", "N/A")

    print()
    print(f"User {user}.")
    print("Ratings:")
    print(f"Rapid: {rapid}.")
    print(f"Blitz: {blitz}.")
    print(f"Bullet: {bullet}.")
    print()


def main() -> int:
    print("== Chess.com User Stats ==")

    while True:
        print()
        user = input("Type the username: ").strip()
        if not user:
            print("You didn't enter a username")
            continue
        if " " in user:
            print("Error: Username cannot contain spaces.")
            continue

        print(f"Fetching data for {user}...", flush=True)
        stats = get_stats(user)

        if stats:
            display_stats(user, stats)

        while True:
            clear_input_buffer()
            repeat = input("Do you want to search another user? (Y/n): ").strip().lower()
            if repeat in ["n", "no"]:
                print("Goodbye!")
                return 0
            elif repeat in ["y", "yes", ""]:
                break
            else:
                print("Invalid input! Please type Y or n.")
    return 0

if __name__ == "__main__":
    sys.exit(main())