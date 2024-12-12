from chat_utils import *
import json
import hashlib
import base64
from snake2 import run_game 
class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.key='1'

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
    def get_key(self):
        return self.key

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        print('Normal Connect!!')
        msg = json.dumps({"action": "connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)
    def connect_game_to(self, peer):
        # msg = json.dumps({"action":"connect_game", "target":peer})
        # mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            # self.peer = peer
            # self.out_msg += 'You can play game with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Start playing game by yourself \n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
# ==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
# ==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in + "\n"

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'k':
                    key = my_msg[1:]
                    self.key = key.strip()

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                            self.state = S_CHATTING
                            self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                            self.out_msg += '-----------------------------------\n'  
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                
                elif my_msg[0] == 'g' :
                    peer = my_msg[1:]
                    peer = peer.strip()
                    mysend(self.s, json.dumps({"action":"connect_game", "target":peer}))
                    if self.connect_game_to(peer) == True:
                    
                        # self.state = S_GAME
                        
                        # self.out_msg += 'Connect to ' + peer + '. Start playing!\n\n'
                        # self.out_msg += '-----------------------------------\n'
                        my_score = [0]
                        in_game=[True]
                        run_game(my_score,in_game)
                        while in_game[0]:
                            
                            pass
                        my_score=str(my_score[0])
                        print (my_score)
                        
                        mysend(self.s, json.dumps({"action":"game over", "score":my_score}))
                        ranking=json.loads(myrecv(self.s))["results"]
                        self.out_msg += ranking
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    term = encrypt_message(self.key,term)
                    encrypt_term = term[:-1][1:]
                    print(encrypt_term)
                    mysend(self.s, json.dumps(
                        {"action": "search", "target": encrypt_term}))
                    search_rslt = json.loads(myrecv(self.s))["results"]
                    rslt_lst = search_rslt.split('\n')
                    new_rslt = ''
                    for line in rslt_lst:
                        new_rslt += decrypt_message(self.key,line) + '\n'
                    #search_rslt = decrypt_message(self.key,search_rslt)
                    if (len(new_rslt)) > 0:
                        self.out_msg += new_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps(
                        {"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu
            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err:
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg

                if peer_msg["action"] == "connect":

                    # ----------your code here------#
                    self.state = S_CHATTING
                    self.out_msg += "Request from " + peer_msg['from'] + '\n'
                    self.out_msg += 'You are connected with ' + peer_msg['from'] + '. Chat away!\n\n'
                    self.out_msg += '-----------------------------------\n'
                elif peer_msg["action"] == "connect_game":
                    print("Peer: Game Connected!!!!!!!!!!!!!!!!")
                    # self.state = S_GAME
                    peer_score = [0]
                    in_game_peer=[True]
                    run_game(peer_score,in_game_peer)
                    while in_game_peer[0]:  
                        pass
                    peer_score=str(peer_score[0])
                    print (peer_score)
                    mysend(self.s, json.dumps({"action":"game over", "score":peer_score}))
                    ranking=json.loads(myrecv(self.s))["results"]
                    self.out_msg += ranking
                    # self.out_msg += 'Your score is' + str(peer_score) + '\n'
                    # # self.out_msg += 'You are connected with ' + self.peer
                    # self.out_msg += '. Start playing\n\n'
                    # self.out_msg += '------------------------------------\n'
                    
                    # ----------end of your code----#

# ==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
# ==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                self.out_msg += "[" + self.me + "]" + my_msg +"\n"
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                else:
                    my_msg = encrypt_message(self.key,my_msg)#byte
                #msg=base64.b64encode(my_msg).decode('utf-8')#str
                    mysend(self.s, json.dumps(
                        {"action": "exchange", "from": "[" + self.me + "]", "message": my_msg}))
                
            if len(peer_msg) > 0:    # peer's stuff, coming in

                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                # Just a test
                # self.out_msg += peer_msg
                if peer_msg["action"] == "exchange":
                    #msg=base64.b64decode(peer_msg["message"])
                    message = decrypt_message(self.key, peer_msg["message"])
                   
                    self.out_msg += peer_msg["from"] + message + "\n"
                elif peer_msg["action"] == "disconnect":
                    
                    self.state = S_LOGGEDIN
                    self.out_msg += "everyone left, you are alone\n"
                elif peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"]+ " " + "joined" + ")/n"
                # ----------end of your code----#

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
# ==============================================================================
# invalid state
# ==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
