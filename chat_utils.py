import socket
import time
import json

# use local loop back address by default
CHAT_IP = '127.0.0.1'
# CHAT_IP = socket.gethostbyname(socket.gethostname())
# CHAT_IP = socket.gethostbyname(socket.gethostname())
import os
CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

menu = "\n++++Click the corresponding button on the \n \
        side column or type the command\n \n\
        Time?: calendar time in the system\n \n\
        Who?: to find out who else are there\n \n\
        k _key_: type k as message entry to set your own key to \n \
        encode messages\n  \n\
        Connet: to connect to the _peer_ and chat\n \n\
        Search poem _#_: type to get number <#> sonnet\n\n \
        Quit: to leave the chat system\n\n"

S_OFFLINE   = 0
S_CONNECTED = 1
S_LOGGEDIN  = 2
S_CHATTING  = 3

SIZE_SPEC = 5

CHAT_WAIT = 0.2

def parse_list(s):
    s = s.strip()[1:-1]
    
    result = []
    current_item = ""
    inside_list = 0
    
    for char in s:
        if char == '[':
            inside_list += 1
            current_item += char
        elif char == ']':
            inside_list -= 1
            current_item += char
        elif char == ',' and inside_list == 0:
            result.append(parse_list(current_item) if '[' in current_item else int(current_item.strip()))
            current_item = ""
        else:
            current_item += char
    
    if current_item:
        result.append(parse_list(current_item) if '[' in current_item else int(current_item.strip()))
    
    return result

def encrypt_message(key, plaintext):
    plaintext = plaintext.split(' ')
    encrypted_list = []
    key_sum = 0
    for char in key:
        key_sum += ord(char)
    for word in plaintext:
        temp_list = []
        for char in word:
            temp_list.append(ord(char) * key_sum)
        encrypted_list.append(temp_list)
    ciphertext = str(encrypted_list)
    return ciphertext

def decrypt_message(key, ciphertext):
    encrypted_list = parse_list(ciphertext)
    key_sum = 0
    for char in key:
        key_sum += ord(char)
    plaintext = ''
    for word in encrypted_list:
        for char in word:
            plaintext += chr(int(char) // key_sum)
        plaintext += ' '
    plaintext = plaintext.rstrip()
    return plaintext

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    else:
        print('Error: wrong state')

def mysend(s, msg,key=None):

    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    
    total_sent = 0
    while total_sent < len(msg) :
        sent = s.send(msg[total_sent:])
        if sent==0:
            print('server disconnected')
            break
        total_sent += sent

def myrecv(s):
    #receive size first
    size = ''
    
    while len(size) < SIZE_SPEC:
       
        text = s.recv(SIZE_SPEC - len(size)).decode()
   
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    #now receive message
    msg = ''
    while len(msg) < size:
        
        text = s.recv(size-len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
 
    return (msg)

def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text) # message goes directly to screen
