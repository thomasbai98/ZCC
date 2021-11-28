import unittest
import json
from cli import State, process_input
from api.ticketapi import *
class Test(unittest.TestCase):

    def get_auth(self):
        userinfo = open("userinfo.json")
        data = json.load(userinfo)
        userinfo.close()
        self.auth = (data["email"] + "/token", data["token"])

    def test_userinfo(self):
        self.get_auth()
        self.assertEqual(get_count(self.auth)[0],"success")

    def test_list_tickets(self):
        self.get_auth()
        for i in range(4):
            self.assertEqual(list_tickets(self.auth,i)[0],"success")

    def test_get_ticket_by_id(self):
        self.get_auth()
        for i in range(1,11):
            self.assertEqual(get_ticket_by_id(self.auth,i),"success")
        for i in range(200,202):
            self.assertEqual(get_ticket_by_id(self.auth,i),"fail")

    # test state machine in cli
    def test_cli(self):
        self.get_auth()
        auth = self.auth
        # test init state
        state = State.Init
        self.assertEqual(process_input("a",state,auth,0),(State.Init,0))
        self.assertEqual(process_input("m",state,auth,0),(State.Menu,0))
        self.assertEqual(process_input("t",state,auth,0),(State.ID,0))
        self.assertEqual(process_input("q",state,auth,0),(None,None))
        # test menu state
        state = State.Menu
        self.assertEqual(process_input("x", state, auth, 0), (State.Menu, 0))
        self.assertEqual(process_input("p", state, auth, 0), (State.Menu, 0))
        self.assertEqual(process_input("p", state, auth, 1), (State.Menu, 0))
        self.assertEqual(process_input("n", state, auth, 0), (State.Menu, 1))
        self.assertEqual(process_input("n", state, auth, 4), (State.Menu, 4))
        self.assertEqual(process_input("t", state, auth, 0), (State.ID, 0))
        self.assertEqual(process_input("q", state, auth, 0), (None, None))
        # test id state
        state = State.ID
        self.assertEqual(process_input("m", state, auth, 0), (State.Menu, 0))
        # invalid id
        self.assertEqual(process_input("x", state, auth, 0), (State.ID, 0))
        # id out of bound
        self.assertEqual(process_input("333", state, auth, 0), (State.Ticket, 0))
        # good id
        self.assertEqual(process_input("3", state, auth, 0), (State.Ticket, 0))
        self.assertEqual(process_input("q", state, auth, 0), (None, None))
        # test ticket state
        state = State.Ticket
        self.assertEqual(process_input("xxx", state, auth, 0), (State.Ticket, 0))
        self.assertEqual(process_input("m", state, auth, 0), (State.Menu, 0))
        self.assertEqual(process_input("t", state, auth, 0), (State.ID, 0))
        self.assertEqual(process_input("q", state, auth, 0), (None, None))



if __name__ == '__main__':
    unittest.main()