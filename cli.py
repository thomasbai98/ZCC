import sys
import json
from api.ticketapi import *
from enum import Enum
import threading

# a state machine for the viewer
class State(Enum):
    Init = 0
    Menu = 1
    ID = 2
    Ticket = 3

# format output
padding = 10*" "

# read userinfo from a json file
def get_user_info():
    userinfo = open("userinfo.json")
    data = json.load(userinfo)
    userinfo.close()
    return data

# check user info and give initial instruction, initialize data
def greeting():
    data = get_user_info()
    auth = (data["email"]+"/token", data["token"])
    assert get_count(auth)[0]!="failed", "Invalad email-token pair"
    print(padding,"Greeting ",data["email"])
    help(State.Init)
    return State.Init, auth

# help output for each state
def help(state):
    if state == State.Init:
        print(padding, "*Press 'm' to view all tickets")
        print(padding, "*Press 't' to view one ticket")
        print(padding, "*Press 'q' to quit")
        return
    if state == State.Menu:
        print(padding, "*Press 'n' to view next page")
        print(padding, "*Press 'p' to view previous page")
        print(padding, "*Press 't' to view one ticket")
        print(padding, "*Press 'q' to quit")
        return
    if state == State.Ticket:
        print(padding, "*Press 'm' to view all tickets")
        print(padding, "*Press 't' to view one ticket")
        print(padding, "*Press 'q' to quit")
        return
    if state == State.ID:
        print(padding, "*Type in ticket ID to view that tickets")
        print(padding, "*Press 'm' to view all tickets")
        print(padding, "*Press 'q' to quit")
        return

#goodbye output
def goodbye():
    print(padding,"Bye")

#validate input and do corresponding output
def process_input(input,state,auth,page):
    # init state: when user enter the CLI
    if state == State.Init:
        if input not in ["m","t","q"]:
            return state,page
        else:
            # user goes to ticket list
            if input == "m":
                result=list_tickets(auth,page)
                # change state if the API call is successful
                if result != "fail":
                    state = State.Menu
            else:
                # user quit
                if input == "q":
                    goodbye()
                    return None,None
                else:
                    # user goes to show one ticket
                    state = State.ID
        return state, page
    # state menu: when user is shown a list of tickets
    if state == State.Menu:
        if input not in ["n","p","t","q"]:
            return state,page
        else:
            # user goes to previous page
            if input == "p":
                page -= 1
                result = list_tickets(auth,page)
                # no previous page
                if result == "too small page":
                    page+=1
                    print(padding,"No previous page")
                # there is previous page
                else:
                    list_tickets(auth, page)
            else:
                # user goes to previous page
                if input == "n":
                    page += 1
                    result = list_tickets(auth, page)
                    # there is no next page
                    if result == "too large page":
                        page -= 1
                        print(padding,"No next page")
                    # there is next page
                    else:
                        list_tickets(auth, page)
                else:
                    # user quit
                    if input == "q":
                        goodbye()
                        return None, None
                    # user wants to show one ticket
                    else:
                        state = State.ID
        return state, page
    # state id: user input id for the ticket to be shown
    if state == State.ID:
        # user goes back the ticket list
        if input=="m":
            result = list_tickets(auth, page)
            if result != "fail":
                state = State.Menu
        else:
            # user quit
            if input == "q":
                goodbye()
                return None, None
            else:
                # the id inputted is invalid
                if not input.isdigit():
                    print(padding,input," is not a valid ID")
                # the id inputted is valid, do an api call
                else:
                    get_ticket_by_id(auth,int(input))
                    state = State.Ticket
        return state, page
    # user is viewing one ticket
    if state == State.Ticket:
        if input not in ["m","q","t"]:
            return state, page
        # user goes back to ticket list
        if input=="m":
            result = list_tickets(auth, page)
            if result != "fail":
                state = State.Menu
        # user quit
        else:
            if input == "q":
                goodbye()
                return None, None
            # user want to view one ticket
            else:
                state = State.ID
        return state, page
    return state, page




# read from sys.stdin
def parse_input():
    readinput = sys.stdin.readline()
    if readinput[-1]=="\n":
        readinput = readinput[:-1]
    return readinput

def main_thread():
    # get input
    readinput = parse_input()
    global state
    global page
    # update state
    state, page = process_input(readinput, state, auth, page)
    if state==None and page==None:
        exit(0)
    print()
    help(state)

def main_loop():
    while True:
        thread = threading.Thread(target=main_thread)
        thread.start()
        thread.join()
        try:
            sys.stdin.flush()
        except:
            # the program is ended
            exit(0)

if __name__=="__main__":
    state, auth = greeting()
    # current page in menu
    page = 0
    main_loop()



