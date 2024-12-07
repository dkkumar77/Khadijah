import speech_recognition as sr
import pyttsx3
import os
import time
from word2number import w2n
import datetime
import platform
import psutil
import random
import socket
import subprocess
import json

engine = pyttsx3.init()
engine.setProperty('rate', 200) 
engine.setProperty('volume', 1) 


def speak_error():
    responses = [
        "Sorry, I didn't understand that.",
        "Would you mind saying that again?",
        "I'm unsure of what you requested.",
        "I couldn't catch that. Could you repeat it?",
        "I didn't quite get that. Could you try again?",
        "I didn't understand, can you say it differently?"
    ]
    response = random.choice(responses)
    speak(response)


def intro():
    intro_response = [
        ""
    ]

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
        speak_error()
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
    speak(f"Total disk space: {disk.total / (1024 ** 3):.2f} GB, Free disk space: {disk.free / (1024 ** 3):.2f} GB")
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

def file_operations():
    speak("File Operations Options: Create File, Read File, Write to File, Delete File")
    option = listen()
    if "create file" in option:
        speak("Please say the name of the file to create.")
        filename = listen()
        if filename:
            with open(filename, "w") as file:
                file.write("Sample Text")
            speak(f"File {filename} created successfully.")
        else:
            speak("File name is missing.")
    elif "read file" in option:
        speak("Please say the file name to read.")
        filename = listen()
        if filename:
            try:
                with open(filename, "r") as file:
                    content = file.read()
                    speak(f"File content: {content}")
            except FileNotFoundError:
                speak("File not found.")
    elif "write to file" in option:
        speak("Please say the file name to write to.")
        filename = listen()
        if filename:
            speak("Please say the content to write.")
            content = listen()
            if content:
                with open(filename, "a") as file:
                    file.write(content)
                speak(f"Content written to {filename} successfully.")
            else:
                speak("Content is missing.")
    elif "delete file" in option:
        speak("Please say the file name to delete.")
        filename = listen()
        if filename:
            try:
                os.remove(filename)
                speak(f"File {filename} deleted successfully.")
            except FileNotFoundError:
                speak("File not found.")
        else:
            speak("File name is missing.")
    else:
        speak("Invalid option for file operations.")

def netpen_sh():

    if not os.path.exists("name.txt"):
        speak("I don't know your name yet. Please tell me your name.")
        user_name = input("Enter your name: ")  
        with open("name.txt", "w") as f:
            f.write(user_name)
    else:
        with open("name.txt", "r") as f:
            user_name = f.read().strip()

    speak(f"Welcome, {user_name}, to the Network Penetration Toolkit. I'll help you with all of your networking needs.")
    
    speak("Welcome to the Network Penetration Toolkit. I'll help you with all of your networking needs.")
    speak("Select an option by speaking out the command or option number.")

    while True:
        print("Options:")
        print("1. IP Flush")
        print("2. DNS Lookup")
        print("3. Ping Test")
        print("4. TCPDump Toolkit")
        print("5. Clear Screen")
        print("6. NMAP Toolkit")
        print("7. Port Analyzer")
        print("8. Traceroute")
        print("9. Shutdown")
        print("10. Restart")
        print("11. System Info")
        print("12. CPU Usage")
        print("13. Memory Usage")
        print("14. Disk Usage")
        print("15. Network Usage")
        print("16. File Operations")
        print("17. Exit")
        
        query = listen()

        if query:
            try:
                query_number = w2n.word_to_num(query.lower())
            except ValueError:
                query_number = None  

            if query_number == 1 or query in ["ip flush"]:
                ip_flush()
            elif query_number == 2 or query in ["dns lookup"]:
                speak("Please say the domain for DNS lookup.")
                domain = listen()
                if domain:
                    dns_lookup(domain)
            elif query_number == 3 or query in ["ping test"]:
                speak("Please type the IP address to ping.")
                ip = input("Enter the IP address: ").strip()
                if ip:
                    speak(f"You entered the IP address: {ip}. Performing ping test.")
                    ping_test(ip)
                    with open("ip_addresses.txt", "a") as file:
                        file.write(f"Pinged IP Address: {ip}\n")
                    speak(f"The IP address {ip} has been saved to the file.")
            elif query_number == 4 or query in ["tcpdump"]:
                tcpdump_toolkit()
            elif query_number == 5 or query in ["clear screen"]:
                clear_screen()
            elif query_number == 6 or query in ["nmap"]:
                nmap_toolkit()
            elif query_number == 7 or query in ["port analyzer"]:
                port_analyzer()
            elif query_number == 8 or query in ["traceroute"]:
                speak("Please say the IP address for traceroute.")
                ip = listen()
                if ip:
                    traceroute(ip)
            elif query_number == 9 or query in ["shutdown"]:
                shutdown_system()
            elif query_number == 10 or query in ["restart"]:
                restart_system()
            elif query_number == 11 or query in ["system info"]:
                system_info()
            elif query_number == 12 or query in ["cpu usage"]:
                check_cpu_usage()
            elif query_number == 13 or query in ["memory usage"]:
                check_memory_usage()
            elif query_number == 14 or query in ["disk usage"]:
                check_disk_usage()
            elif query_number == 15 or query in ["network usage"]:
                check_network_usage()
            elif query_number == 16 or query in ["file operations"]:
                file_operations()
            elif query_number == 17 or query in ["exit"]:
                exit_program()
            else:
                speak("Invalid command. Please try again.")
        time.sleep(1)
        
if __name__ == "__main__":
    netpen_sh()
