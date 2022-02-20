# zScan - a Super simple subdomain scanner

The other day I was catching up to Joe Helle's Python 3 tools series on YouTube and got inspired to give the subdomain scanner a try. I'm not a coder so the code could be ugly, any feedback is welcome!

````text
    ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ╚══███╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
      ███╔╝ ███████╗██║     ███████║██╔██╗ ██║
     ███╔╝  ╚════██║██║     ██╔══██║██║╚██╗██║
    ███████╗███████║╚██████╗██║  ██║██║ ╚████║
    ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
   ─▌ A subdomain enumeration tool by Tzero86 ▐─

[*] Loading zScan a quick subdomain scanner, inspired by Joe Helle's python3 series.
[*] Starting to scan for valid subdomains for facebook.com
[!] A total of 4989 subdomains will be scanned. Please be patient!
[!] You can press CRTL+C at any time to terminate the scan and save the results.
[*] Scanning: facebook.com |▍         | ⡀ 173/4989 [3%] in 9s (18.3/s, eta: 3:26) Testing autodiscover.blog.
````


## Install

    pip install -r requirements.txt

## usage

    python zscan.py -sd google.com

## See Help & options

    python zscan.py -h

```
zScan is a Subdomain enumeration tool made by Tzero86

optional arguments:
  -h, --help            show this help message and exit
  -sd DOMAIN, --domain DOMAIN
                        Single Domain to enumerate
  -dl DOMLIST, --domlist DOMLIST
                        Custom domain file to use
  -sl SUBLIST, --sublist SUBLIST
                        Custom subdomains file to use
  -o OUTPUT, --output OUTPUT
                        Output file
```

## Features

- Scan for subdomains based on given domain
- Save results to a file
- Scan progress bar
- Terminate Scan by pressing CRTL+C
- Support to specify output file to save the results to

## Currently working on

- Support for custom domain and subdomain files


## Things to fix or add

- Add support to specify a file with subdomains
- Add support to specify a file with domains
- Add support to limit the number of subdomains to scan
- TO FIX: When pressing CRTL+C, the scan output on the terminal gets messed up.



I'm going to add a few more features to this, like being able to specify how many subdomains to try. I'll be adding more features as I get the time to do so.

Thanks!

@tzero86
