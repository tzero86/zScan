import argparse
import json
import os
from contextlib import suppress
from datetime import datetime
from alive_progress import alive_bar
from dns import resolver
import signal
import sys
from rich import print, print_json

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
    if custom_sublist:
        # if the user provided a custom subdomains file, we load that file and return a list with all the subdomains
        with open(custom_sublist, 'r') as f:
            subdomains = f.read().splitlines()
        return subdomains
    else:
        # if the user does not provides a custom list, we use the seclists.org subdomain list
        with open('./lists/subdomains-top1million-110000.txt', 'r') as f:
            filecontents = f.read()
            subdoms = filecontents.splitlines()
        return subdoms


# here we take care of scanning each subdomain and checking if it's alive
def scan_subdomains():
    subdomains = load_subdoms()
    print(f'[*] Starting to scan [cyan]{domain}[/] for valid subdomains... ')
    total = len(subdomains)
    print(f'[!] A total of [cyan]{total}[/] subdomains will be scanned. [bold]Please be patient![/]')
    print(f'[!] You can press [bold][cyan]CRTL+C[/][/] at any time to terminate the scan and save the results.')
    with alive_bar(total, spinner='dots', length=12, theme='smooth') as bar:
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
    if output_file:
        # if the user provided an output file, we save the results to that file
        with open(output_file, 'w') as f:
            json.dump(output_json, f, indent=4)
        print(f'[+] Scan Finished, showing results: ')
        print_json(json.dumps(output_json, indent=4))
        print(f'[+] Results saved to: [purple]{output_file}[/]')
    else:
        # if the user did not provide an output file, we save the results to a default file
        with open(f'./results/{domain}_zScan_results.json', 'w') as f:
            json.dump(output_json, f, indent=4)
        print(f'[+] Scan Finished, showing results: ')
        print_json(json.dumps(output_json, indent=4))
        print(f'[+] Results saved to: [purple]./results/{domain}_zScan_results.json[/]')


# we handle the signals that might occur
def signal_handler(sig, frame):
    print('\n\n')
    print('[red][!] Terminate request received, saving scan results and exiting...[/]')
    save_subdomains()
    sys.exit(0)


# takes care of the start of the program and prints the banner
def start():
    banner = '''[green]
    
    ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ╚══███╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
      ███╔╝ ███████╗██║     ███████║██╔██╗ ██║
     ███╔╝  ╚════██║██║     ██╔══██║██║╚██╗██║
    ███████╗███████║╚██████╗██║  ██║██║ ╚████║
    ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
   ─▌ A subdomain enumeration tool by [purple]Tzero86[/] ▐─[/]
    '''
    clear_screen()
    print(banner)
    print('[*] Loading [bold][purple]zScan[/][/] a quick subdomain scanner, inspired by Joe Helle\'s python3 series.')
    signal.signal(signal.SIGINT, signal_handler)
    scan_subdomains()


if __name__ == '__main__':
    start()
