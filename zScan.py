import argparse
import json
import os
from contextlib import suppress
from datetime import datetime
from alive_progress import alive_bar
from dns import resolver
import signal
import sys

# Global variables
subdomains_found = []
scan_StartTime = datetime.now()

# We parse the required commandline arguments
parser = argparse.ArgumentParser(description='zScan is a Subdomain enumeration tool made by Tzero86')
parser.add_argument('-sd', '--domain', help='Single Domain to enumerate', required=True)
parser.add_argument('-dl', '--domlist', help='Custom domain file to use', required=False)
parser.add_argument('-sl', '--sublist', help='Custom subdomains file to use', required=False)
parser.add_argument('-o', '--output', help='Output file', required=False)
args = parser.parse_args()
domain = args.domain
custom_sublist = args.sublist
custom_domlist = args.domlist
output_file = args.output

# a function to clear the terminal screen
def clear_screen():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


# we load the domains file and return a list with all the subdomains
def load_subdoms():
    with open('./lists/subdomains-top1million-110000.txt', 'r') as f:
        filecontents = f.read()
        subdoms = filecontents.splitlines()
    return subdoms


# we ask the user for a custom subdomains file to load
def load_subdoms_file():
    with open(input('[*] Enter the path to the file containing the subdomains: '), 'r') as f:
        filecontents = f.read()
        subdoms = filecontents.splitlines()
    return subdoms


# here we take care of scanning each subdomain and checking if it's alive
def scan_subdomains():
    subdomains = load_subdoms()
    print(f'[*] Starting to scan for valid subdomains for {domain}')
    total = len(subdomains)
    print(f'[!] A total of {total} subdomains will be scanned. Please be patient!')
    print(f'[!] You can press CRTL+C at any time to terminate the scan and save the results.')
    with alive_bar(total, spinner='dots', length=10, theme='smooth') as bar:
        for subdomain in subdomains:
            bar.title = f'[*] Scanning: {domain}'
            bar.text(f'Testing {subdomain}.{domain}')
            # we suppress the exceptions that might occur
            with suppress(resolver.NXDOMAIN, resolver.NoAnswer, resolver.Timeout, resolver.NoNameservers):
                # we use the dns.resolver library to check if the subdomain is alive
                if resolver.resolve(f'{subdomain}.{domain}', 'A').response.answer:
                    # if the subdomain is alive, we add it to the list of subdomains found
                    subdomains_found.append(subdomain)
            # we update the progress bar
            bar()
    print(f'\n[+] Scan Finished, Subdomains found: {subdomains_found}')
    save_subdomains()


# we save the subdomains found to a file
def save_subdomains():
    # Output json template
    output_json = {
        "zScan": {
            "domain_scanned": f'{domain}',
            "total_subdomains_found": f'{len(subdomains_found)}',
            "scan_start_date": f'{scan_StartTime}',
            "scan_end_date": f'{datetime.now()}',
            "subdomains_found": subdomains_found
        }
    }
    with open(f'./results/{domain}_subdomains.txt', 'w') as f:
        f.write(f'{json.dumps(output_json, indent=4)}')
    print(f'[*] Subdomains saved to {domain}_subdomains.txt')


# we handle the signals that might occur
def signal_handler(sig, frame):
    print('\n\n')
    print('[!] Terminate request received, saving scan results and exiting...')
    save_subdomains()
    sys.exit(0)


# takes care of the start of the program and prints the banner
def start():
    banner = '''
    
    ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ╚══███╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
      ███╔╝ ███████╗██║     ███████║██╔██╗ ██║
     ███╔╝  ╚════██║██║     ██╔══██║██║╚██╗██║
    ███████╗███████║╚██████╗██║  ██║██║ ╚████║
    ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
   ─▌ A subdomain enumeration tool by Tzero86 ▐─
    '''
    clear_screen()
    print(banner)
    print('[*] Loading zScan a quick subdomain scanner, inspired by Joe Helle\'s python3 series.')
    signal.signal(signal.SIGINT, signal_handler)
    scan_subdomains()


if __name__ == '__main__':
    start()
