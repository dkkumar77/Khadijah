import pvporcupine
import struct
import pyaudio
import speech_recognition as sr
import pyttsx3
import os
import time
import platform
import psutil
import random
import socket
import subprocess
import json
from word2number import w2n
import datetime

  

porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_PATH])

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

engine = pyttsx3.init()
engine.setProperty('rate', 200) 
engine.setProperty('volume', 1) 
voices = engine.getProperty('voices')

female_voice = None
for voice in voices:
    if "female" in voice.name.lower(): 
        female_voice = voice
        break

if female_voice:
    engine.setProperty('voice', female_voice.id)  


def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source) 

    try:
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble connecting.")
        return None

def log_event(event):
    with open("event_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {event}\n")

def system_info():
    log_event("Fetching system information")
    speak("Fetching system information.")
    if platform.system() == "Windows":
        os.system("systeminfo")
    else:
        os.system("uname -a")  

def check_cpu_usage():
    log_event("Checking CPU usage")
    speak("Checking CPU usage.")
    cpu_usage = psutil.cpu_percent(interval=1)
    speak(f"Current CPU usage is {cpu_usage}%")
    print(f"CPU Usage: {cpu_usage}%")

def check_memory_usage():
    log_event("Checking memory usage")
    speak("Checking memory usage.")
    memory = psutil.virtual_memory()
    speak(f"Total memory: {memory.total / (1024 ** 3):.2f} GB, Available memory: {memory.available / (1024 ** 3):.2f} GB")
    print(f"Total memory: {memory.total / (1024 ** 3):.2f} GB, Available memory: {memory.available / (1024 ** 3):.2f} GB")

def check_disk_usage():
    log_event("Checking disk usage")
    speak("Checking disk usage.")
    disk = psutil.disk_usage('/')
    speak(f"Total disk space: {disk.total / (1024 ** 3):.2f} Gigabytes, Free disk space: {disk.free / (1024 ** 3):.2f} GB")
    print(f"Total disk space: {disk.total / (1024 ** 3):.2f} GB, Free disk space: {disk.free / (1024 ** 3):.2f} GB")

def check_network_usage():
    log_event("Checking network usage")
    speak("Checking network usage.")
    net_io = psutil.net_io_counters()
    speak(f"Bytes sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB, Bytes received: {net_io.bytes_recv / (1024 ** 2):.2f} MB")
    print(f"Bytes sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB, Bytes received: {net_io.bytes_recv / (1024 ** 2):.2f} MB")

def get_ip_address():
    log_event("Fetching IP address")
    speak("Fetching IP address.")
    ip_address = socket.gethostbyname(socket.gethostname())
    speak(f"Your IP address is {ip_address}")
    print(f"IP Address: {ip_address}")

def ip_flush():
    log_event("Flushing IP")
    speak("Flushing IP.")
    if platform.system() == "Windows":
        os.system("ipconfig /release && ipconfig /renew")
    else:
        os.system("sudo ifconfig en0 down && sudo ifconfig en0 up") 

def dns_lookup(domain):
    log_event(f"Performing DNS lookup for {domain}")
    speak(f"Performing DNS lookup for {domain}.")
    if platform.system() == "Windows":
        os.system(f"nslookup {domain}")  
    else:
        os.system(f"dig {domain}") 

def ping_test(ip):
    log_event(f"Pinging {ip}")
    speak(f"Pinging {ip}.")
    if platform.system() == "Windows":
        os.system(f"ping {ip} -n 4") 
    else:
        os.system(f"ping {ip} -c 4") 

def tcpdump_toolkit():
    log_event("Running TCPDump toolkit")
    speak("TCPDump options are: Available NICs, Run packet dump, Packets from source, Packets from destination.")
    option = listen()

    print("You said:", option.lower())  
    
    if "tcpdump" in option.lower() or "tcp" in option.lower():
        speak("You selected the TCPDump toolkit. Please choose an option: available NICs, run packet dump, packets from source, or packets from destination.")
        option = listen()

        print("You said:", option.lower())  
        
        if "available" in option.lower():
            os.system("sudo tcpdump -D")
        elif "run" in option.lower():
            os.system("sudo tcpdump -c 50")
        elif "source" in option.lower():
            speak("Please say the source IP.")
            source_ip = listen()
            if source_ip:
                os.system(f"sudo tcpdump src {source_ip}")
        elif "destination" in option.lower():
            speak("Please say the destination IP.")
            dest_ip = listen()
            if dest_ip:
                os.system(f"sudo tcpdump dst {dest_ip}")
        else:
            speak("Invalid option for TCPDump.")
    else:
        speak("Invalid command for TCPDump toolkit.")

def nmap_toolkit():
    log_event("Running NMAP toolkit")
    speak("Running NMAP Toolkit. Scanning ports on localhost.")
    os.system("nmap -p 1-1024 localhost")

def port_analyzer():
    log_event("Running port analyzer")
    speak("Please wait while I analyze ports.")
    if platform.system() == "Windows":
        os.system("netstat -an")  
    else:
        os.system("netstat -tuln") 
 
def traceroute(ip):
    log_event(f"Running traceroute to {ip}")
    speak(f"Running traceroute to {ip}.")
    if platform.system() == "Windows":
        os.system(f"tracert {ip}")  
        os.system(f"traceroute {ip}")  

def shutdown_system():
    log_event("Shutting down system")
    speak("Shutting down the system.")
    if platform.system() == "Windows":
        os.system("shutdown /s /f /t 0")  
    else:
        os.system("sudo shutdown -h now")  

def restart_system():
    log_event("Restarting system")
    speak("Restarting the system.")
    if platform.system() == "Windows":
        os.system("shutdown /r /f /t 0") 
    else:
        os.system("sudo reboot")  

def clear_screen():
    log_event("Clearing the screen")
    if platform.system() == "Windows":
        os.system("cls")  
    else:
        os.system("clear")  

def exit_program():
    log_event("Exiting the toolkit")
    speak("Exiting the toolkit.")
    print(f"{os.getlogin()} had a successful logoff on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    exit()

def netpen_sh():
    if not os.path.exists("name.txt"):
        speak("I don't know your name yet. Please tell me your name.")
        user_name = input("Enter your name: ")  
        with open("name.txt", "w") as f:
            f.write(user_name)
        os.chmod("name.txt", 0o600)  
    
    else:
        with open("name.txt", "r") as f:
            user_name = f.read().strip()

    speak(f"Welcome, {user_name}, to the Network Penetration Toolkit. I'll help you with all of your networking needs.")
    speak("Select an option by speaking out the command or option number.")

    while True :
        print("Options:")
        print("1. IP Flush")
        print("2. DNS Lookup")
        print("3. Ping Test")
        print("4. TCPDump Toolkit")
        print("5. Clear Screen")
        print("6. NMAP Toolkit")
        print("7. Shutdown")
        print("8. Restart")
        print("9. Exit")


        command = listen()

        if command is None:
            speak("No command recognized, exiting")
            break
        if "flush" in command:
            ip_flush()
        elif "dns" in command:
            domain = input("Enter domain to lookup: ")
            dns_lookup(domain)
        elif "ping" in command:
            ip = input("Enter IP address to ping: ")
            ping_test(ip)
        elif "tcpdump" in command:
            tcpdump_toolkit()
        elif "clear" in command:
            clear_screen()
        elif "nmap" in command:
            nmap_toolkit()
        elif "shutdown" in command:
            shutdown_system()
        elif "restart" in command:
            restart_system()
        elif "exit" in command:
            exit_program()
        else:
            speak("Invalid command.")
        
        time.sleep(1) 

try:
    print("Listening for wake word...")
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake word detected!")
            netpen_sh()  
except KeyboardInterrupt:
    porcupine.delete()
    audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()
    print("Program terminated.")
