#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
import subprocess
from PIL import Image, ImageTk  # For advanced formats like JPG
# car_image = PhotoImage(file="chat_system/Images/RacingRedCar.png")


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""


    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold",
                       anchor = "center")
                
        self.pls.place(relheight = 0.15,
                       relx = 0.35, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 14 bold")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.15)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
          
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
  
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 665, #195 of them should be the column 
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 0.71)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#666e75")
          
        self.line.place(relwidth = 0.71,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
        # The column
        self.sideColumn = Label(self.Window,
                                bg = "#ABB2B9",
                                height = 550
                                )
        self.sideColumn.place(relwidth = 0.29,
                              relx = 0.71)
        
        #Search Poem in the side column
        self.entryPoem = Entry(self.Window,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")       
    
        self.entryPoem.place(relwidth = 0.25,
                            relheight = 0.075,
                            rely = 0.300,
                            relx = 0.73)
        
        self.entryGame = Entry(self.Window,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")       
    
        self.entryGame.place(relwidth = 0.25,
                            relheight = 0.075,
                            rely = 0.4700,
                            relx = 0.73)
        #Search chat history in the side column
        # self.entrySearch = Entry(self.Window,
        #                       bg = "#2C3E50",
        #                       fg = "#EAECEE",
        #                       font = "Helvetica 13")       
    
        # self.entrySearch.place(relwidth = 0.25,
        #                     relheight = 0.075,
        #                     rely = 0.450,
        #                     relx = 0.73)
        #Connect with people
        self.entryPeople = Entry(self.Window,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")       
    
        self.entryPeople.place(relwidth = 0.25,
                            relheight = 0.075,
                            rely = 0.14,
                            relx = 0.73)

        
        # The label bottom  
        self.labelBottom = Label(self.Window,
                                 bg = "#8898a8",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 0.71,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 10,
                                height = 2,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.78,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.20)
        # The quit button
        close_button = Button(self.Window, text="Close",font = "Helvetica 10 bold", command=lambda: self.quitApp())
        close_button.place(relx=0.8, rely=0.9)

        # create a time button
        self.time = Button(self.sideColumn,
                                text = "🕤 Time?",
                                relief="flat",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                height = 4,
                                bg = "#ABB2B9",
                                command = lambda : self.timeButton())
          
        self.time.place(relx = 0.6,
                             rely = 0.001,
                             relheight = 0.004, 
                             relwidth = 0.3)
        # create a who button
        self.who = Button(self.sideColumn,
                                text = "👫 Who?",
                                font = "Helvetica 10 bold", 
                                width = 10,
                                height = 2,
                                bg = "#ABB2B9",
                                command = lambda : self.whoButton())
          
        self.who.place(relx = 0.1,
                             rely = 0.001,
                             relheight = 0.004, 
                             relwidth = 0.3)
        # create a poem sending button
        self.poem = Button(self.sideColumn,
                                text = "📜 Search Poem",
                                font = "Helvetica 10 bold", 
                                width = 100,
                                height = 2,
                                bg = "#ABB2B9",
                                command = lambda : self.poemButton())
          
        self.poem.place(relx = 0.1,
                             rely = 0.0245,
                             relheight = 0.003, 
                             relwidth = 0.8)
        # create a search history button
        # self.search = Button(self.sideColumn,
        #                         text = "Search Chat History",
        #                         font = "Helvetica 10 bold", 
        #                         width = 10,
        #                         height = 2,
        #                         bg = "#ABB2B9",
        #                         command = lambda : self.searchButton()) #!!!!! Don't forget to change it
          
        # self.search.place(relx = 0.1,
        #                      rely = 0.034,
        #                      relheight = 0.003, 
        #                      relwidth = 0.80)
        # create a connect button
        self.connect = Button(self.sideColumn,
                                text = "🤝 Connect",
                                font = "Helvetica 10 bold", 
                                width = 10,
                                height = 2,
                                bg = "#ABB2B9",
                                command = lambda : self.connectButton()) #!!!!! Don't forget to change it
          
        self.connect.place(relx = 0.1,
                             rely = 0.014,
                             relheight = 0.003, 
                             relwidth = 0.80)
          
        self.textCons.config(cursor = "arrow")
        # create a gaming button
        self.buttonGame = Button(self.sideColumn,
                                 text="🐍 Become a snake!",
                                 font="Helvetica 10 bold",
                                 width=20,
                                 bg="#ABB2B9",
                                 command=self.gameButton)

        self.buttonGame.place(relx=0.1,
                              rely=0.0355,
                              relheight=0.003,
                              relwidth=0.80)
        # create a racing car image
        # self.racingCar = Label(self.sideColumn,
        #                       image = car_image)       
    
        # self.racingCar.place(relwidth = 0.25,
        #                     relheight = 0.075,
        #                     rely = 0.450,
        #                     relx = 0.73)
        # self.racingCar.image = car_image
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)

    # function to send the time
    def timeButton(self):  
        self.my_msg = "time"

    # Function to send the Poem
    def poemButton(self):
        user_input = self.entryPoem.get()
        self.my_msg = 'p' + user_input
        self.entryPoem.delete(0, END)
    # Function to start the game
    def gameButton(self):
        user_input = self.entryGame.get()
        self.my_msg = 'g' + user_input
        self.entryPoem.delete(0, END)
    # Function to Quit 
    def quitApp(self):
        self.my_msg = "q"
        
    
    # # Function to send the search history key word
    # def searchButton(self):
    #     user_input = self.entrySearch.get()
    #     self.my_msg = '? ' + user_input
    #     self.entrySearch.delete(0, END)
    # Function to send the people to be connected
    def connectButton(self):
        user_input = self.entryPeople.get()
        self.my_msg = 'c ' + user_input
        self.entryPeople.delete(0, END)

    # function to send the people who are online
    def whoButton(self):  
        self.my_msg = "who"

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()
