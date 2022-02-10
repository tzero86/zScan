import argparse
from contextlib import suppress
from alive_progress import alive_bar
from dns import resolver
import signal
import sys

# Global variables
subdomains_found = []

# We parse the required commandline arguments
parser = argparse.ArgumentParser(description='Subdomain enumeration tool by Tzero86')
parser.add_argument('-d', '--domain', help='Domain to enumerate', required=True)
args = parser.parse_args()
domain = args.domain


# we load the domains file and return a list with all the subdomains
def load_subdoms():
    with open('./lists/subdomains-top1million-110000.txt', 'r') as f:
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
    with alive_bar(total, spinner='triangles', length=20, theme='smooth') as bar:
        for subdomain in subdomains:
            bar.title = f'[*] Scan progress: {domain}'
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
    with open(f'./results/{domain}_subdomains.txt', 'w') as f:
        for subdomain in subdomains_found:
            f.write(f'{subdomain}\n')
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
         .M"""bgd                               
        ,MI    "Y                               
M"""MMV `MMb.      ,p6"bo   ,6"Yb.  `7MMpMMMb.  
'  AMV    `YMMNq. 6M'  OO  8)   MM    MM    MM  
  AMV   .     `MM 8M        ,pm9MM    MM    MM  
 AMV  , Mb     dM YM.    , 8M   MM    MM    MM  
AMMmmmM P"Ybmmd"   YMbmd'  `Moo9^Yo..JMML  JMML.
    '''
    print(banner)
    print('[*] zScan is a tool to scan for subdomains based on given domain, inspired by Joe Helle\'s python3 series.')
    signal.signal(signal.SIGINT, signal_handler)
    scan_subdomains()


if __name__ == '__main__':
    start()
