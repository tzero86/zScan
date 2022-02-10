# zScan - a Super simple subdomain scanner

The other day I was catching up to Joe Helle's Python 3 tools series on YouTube and got inspired to give the subdomain scanner a try. I'm not a coder so the code could be ugly, any feedback is welcome!

````text

         .M"""bgd
        ,MI    "Y
M"""MMV `MMb.      ,p6"bo   ,6"Yb.  `7MMpMMMb.  
'  AMV    `YMMNq. 6M'  OO  8)   MM    MM    MM  
  AMV   .     `MM 8M        ,pm9MM    MM    MM  
 AMV  , Mb     dM YM.    , 8M   MM    MM    MM  
AMMmmmM P"Ybmmd"   YMbmd'  `Moo9^Yo..JMML  JMML.
    
[*] zScan is a tool to scan for subdomains based on given domain, inspired by Joe Helle's python3 series.
[*] Starting to scan for valid subdomains for google.com
[!] A total of 4989 subdomains will be scanned. Please be patient!
[!] You can press CRTL+C at any time to terminate the scan and save the results.
on 211: 
on 211: [!] Terminate request received, saving scan results and exiting...
on 211: [*] Subdomains saved to google.com_subdomains.txt
[*] Scan progress: google.com |█▊                                      | ▂▄▆ 211/4989 [4%] in 17s (12.3/s, eta: 6:27) Testing a.google.com
Process finished with exit code 0

````



## Install

    pip install -r requirements.txt

## usage

    python zscan.py -d google.com


## Features

- Scan for subdomains based on given domain
- Save results to a file
- Scan progress bar
- Terminate Scan by pressing CRTL+C

## Things to fix or add

- Add support to specify a file with subdomains
- Add support to specify a file with domains
- Add support to limit the number of subdomains to scan
- TO FIX: When pressing CRTL+C, the scan output on the terminal gets messed up.



I'm going to add a few more features to this, like being able to specify how many subdomains to try. I'll be adding more features as I get the time to do so.

Thanks!

@tzero86
