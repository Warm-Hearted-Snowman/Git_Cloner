import requests
from bs4 import BeautifulSoup
from subprocess import check_call
from os import mkdir, chdir, path
from colorama import init, Fore, Style

init()

def show_menu():
    print(Fore.BLUE + 'Choose one of the following options:')
    print('1. Enter a custom username.')
    print('2. Use a pre-set list of usernames.')
    print('0. Exit')
    choice = input(Fore.GREEN+ 'Enter your choice: ')
    if choice == '1':
        print(Fore.YELLOW + '[*] Custom Mode Selected' + Style.RESET_ALL)
        user_name = input(Fore.BLUE + 'Enter Username: ' + Style.RESET_ALL)
        return [user_name]
    elif choice == '2':
        print(Fore.YELLOW + '[*] Pre-set Mode Selected\nUsers:')
        with open('users.txt', 'r') as f:
            users = [user.strip() for user in f]
        for user in users:
            print(f"- {user}")
        print(Style.RESET_ALL)
        return users
    elif choice == '0':
        return ['0']
    else:
        print(Fore.RED + 'Invalid choice. Please enter 1 or 2.' + Style.RESET_ALL)
        return show_menu()

while True:
    users = show_menu()
    if users == ['0']:
        brexit = input(Fore.RED + 'Have you already exited? (y/n):'+ Fore.GREEN)
        if brexit == 'y':
            print(Fore.YELLOW + '[*] Goodbye!' + Fore.RESET)
            break
    else:
        for user_name in users:
            repo_page = requests.get(f'https://github.com/{user_name}?tab=repositories')
            if repo_page.status_code != 404:
                repo_soup = BeautifulSoup(repo_page.text, 'html.parser')
                try:
                    mkdir('users')
                except:
                    pass
                chdir('users')
                try:
                    mkdir(user_name)
                except FileExistsError as e:
                    print(Fore.RED + f"[-] The '{user_name}' directory already exists." + Style.RESET_ALL)
                chdir(user_name)
                print(Fore.CYAN + f'[+] Start cloning for {user_name.upper()}:')
                for link in ['https://github.com' + card.find('a').get('href') for card in repo_soup.find_all('h3', attrs={'class': "wb-break-all"})]:
                    repo_name = path.basename(link)
                    print(Fore.YELLOW + f'[*] {repo_name}:' + Style.RESET_ALL)
                    if path.isdir(repo_name):
                        print(Fore.YELLOW + f'[!] {repo_name} repository already exists' + Style.RESET_ALL)
                    else:
                        print(Fore.GREEN)
                        check_call(['git', 'clone', link])
                        print(Fore.GREEN + f'[+] Successfully cloned {repo_name}' + Style.RESET_ALL)
                chdir('..')
                chdir('..')
            else:
                print(Fore.RED + f"[-] UserName: '{user_name}' is Invalid." + Style.RESET_ALL)