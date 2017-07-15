# Shodanwave 

Shodanwave is a tool for exploring and obtaining information from cameras specifically Netwave IP Camera. The tool uses a search engine called shodan that makes it easy to search for cameras online.

What does the tool to? Look, a list!

 * Search 
 * Brute force
 * SSID and WPAPSK Password Disclosure
 * E-mail, FTP, DNS, MSN Password Disclosure 
 * Exploit
 
This is an example of shodan wave running, the password was not found through raw force so the tool tries to leak the camera's memory. If the tool finds the password it does not try to leak the memory.

[![asciicast](https://asciinema.org/a/G7gVOiReMiv43V8wlMbB4mm9B.png)](https://asciinema.org/a/G7gVOiReMiv43V8wlMbB4mm9B?autoplay=1)

### How to use?
To use shodanwave you need an api key which you can get for free at https://www.shodan.io/, then you need to follow the next steps.

### Installation

```
$ cd /opt/
$ git clone https://github.com/fbctf/shodanwave.git
$ cd shodanwave
$ pip install -r requirements.txt
```
### Usage
```
Usage: python shodanwave.py -u usernames.txt -w passwords.txt  -k Shodan API key
       python shodanwave.py --help 
         __              __                                   
   _____/ /_  ____  ____/ /___ _____ _      ______ __   _____ 
  / ___/ __ \/ __ \/ __  / __ `/ __ \ | /| / / __ `/ | / / _ \
 (__  ) / / / /_/ / /_/ / /_/ / / / / |/ |/ / /_/ /| |/ /  __/
/____/_/ /_/\____/\__,_/\__,_/_/ /_/|__/|__/\__,_/ |___/\___/ 
                                                              

This tool is successfully connected to shodan service
Information the use of this tool is illegal, not bad.

usage: shodanwave.py [-h] [-s SEARCH] [-u USERNAME] [-w PASSWORD] [-k ADDRESS]

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        Default Netwave IP Camera
  -u USERNAME, --username USERNAME
                        Select your usernames wordlist
  -w PASSWORD, --wordlist PASSWORD
                        Select your passwords wordlist
  -k ADDRESS, --shodan ADDRESS
                        Shodan API key
  -l LIMIT, --limit LIMIT
                        Limit the number of registers responsed by Shodan
  -o OFFSET, --offset OFFSET
                        Shodan skips this number of registers from response
  -t OUTPUT, --output OUTPUT
                        Save the results


```
### Attention
Use this tool wisely and not for evil. To get the best performece of this tool you need to pay for shodan to get full API access
Options --limit and --offset may need a paying API key and consume query credits from your Shodan account.

### References:

 * [Shodan API](https://www.shodan.io/)  search engine for Internet-connected devices.
 * [Requests](http://docs.python-requests.org/en/master/) Requests: HTTP for Humans
 * [Netwave Exploit](https://www.exploit-db.com/exploits/41236/) Netwave IP Camera - Password Disclosure
