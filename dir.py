import os, argparse, subprocess, sys, threading
from queue import Queue

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

try:
    import requests
except ImportError:
    print(f"{bcolors.FAIL}requests not found. Installing...{bcolors.ENDC}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def msgload(url, wordlist, thread_num, filter_code):
    clear()
    print("""   __ __       ___ __          __            
.--|  |__.----.'  _|__.-----.--|  .-----.----.
|  _  |  |   _|   _|  |     |  _  |  -__|   _|
|_____|__|__| |__| |__|__|__|_____|_____|__|  \n""")
    print(f"{bcolors.OKGREEN}Made by horizon.sh{bcolors.ENDC}")
    print("[!] legal disclaimer: Usage of LFIchecker for attacking targets without prior mutual consent is illegal.")
    print("\n===============================")
    print(f"{bcolors.OKGREEN}URL:{bcolors.ENDC} {url}")
    print(f"{bcolors.OKGREEN}Wordlist:{bcolors.ENDC} {wordlist}")
    print(f"{bcolors.OKGREEN}Threads:{bcolors.ENDC} {thread_num}")
    print(f"{bcolors.OKGREEN}Filter Status Code:{bcolors.ENDC} {filter_code if filter_code else 'None'}")
    print("===============================\n")

    loops(url, wordlist, thread_num, filter_code)

def worker(url, queue, filter_code, log_file):
    while not queue.empty():
        path = queue.get()
        full_url = url + path.strip()
        try:
            r = requests.get(full_url)
            if (filter_code and r.status_code == filter_code) or (not filter_code and r.status_code != 404):
                print(f"{bcolors.OKGREEN}[+] {full_url} ({r.status_code}){bcolors.ENDC}")
                with open(log_file, "a") as f:
                    f.write(f"{full_url} ({r.status_code})\n")
        except requests.RequestException as e:
            print(f"{bcolors.WARNING}Request failed: {full_url} - {e}{bcolors.ENDC}")
        queue.task_done()

def loops(url, wordlist, thread_num, filter_code):
    q = Queue()
    log_file = "found_paths.log"

    with open(wordlist, "r", encoding="latin1") as f:
        for line in f:
            q.put(line)

    threads = []
    for _ in range(thread_num):
        t = threading.Thread(target=worker, args=(url, q, filter_code, log_file))
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="dir-finder")
    parser.add_argument('-u', '--url', help='URL to bruteforce. Example: https://site.com/', required=True)
    parser.add_argument('-w', '--wordlist', help='Select wordlist. Example: /usr/share/wordlists/example.txt', default='list.txt')
    parser.add_argument('-t', '--threads', help='Select threads. DEFAULT: 2', default=2, type=int)
    parser.add_argument('-c', '--code', help='Filter by specific HTTP status code', type=int)
    args = parser.parse_args()

    try:
        msgload(args.url, args.wordlist, args.threads, args.code)
    except KeyboardInterrupt:
        print(f"{bcolors.WARNING}\n[QUIT] You quit this session.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}\n[ERROR] {bcolors.ENDC} \n\n {e}")
