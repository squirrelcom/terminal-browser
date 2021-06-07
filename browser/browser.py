import sys
import os
import requests
from bs4 import BeautifulSoup
from collections import deque
from colorama import init, Fore
init(autoreset=True)

dir_name = sys.argv[1]

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

history = deque()


def get_site_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    real_site = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"])
    useful_string = ""
    for page in real_site:
        if page.name == "a":
            useful_string += Fore.BLUE + page.text
        useful_string += page.text + "\n"
    return useful_string


def save_site_content(data, path):
    history.append(path)
    with open(os.path.join(dir_name, path), "w") as f:
        f.write(data)


def go_site(site):
    address = site if site.startswith("https://") else f"https://{site}"
    site_content = get_site_content(address)
    # site_in_blue = Fore.BLUE + it_is_the_site
    save_site_content(site_content, site)
    print(site_content)


def go_back():
    if len(history) > 1:
        history.pop()
        with open(os.path.join(dir_name, history.pop()), 'r') as f:
            print(f.read())
    else:
        print("No tabs in history yet!")


while True:
    command = input("Squirrel-Navigator!! Search for a Url >>")
    if command == "exit":
        break
    if command == "back":
        go_back()
    elif "." in command:
        go_site(command)
    else:
        print("Error: Squirrel-Navigator could not locate that URL")
