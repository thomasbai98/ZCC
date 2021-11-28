File Tree Diagram
|-cli.py
|-userinfo.json
|-Readme.md
|-test.py
|-api
   |-ticketapi.py

File Explanation
cli.py: the CLI program 
userinfo.json: the json file store the user email and token
Readme.md: the readme file
test.py: the unit test program for all the api call functions
api/ticketapi.py: contain functions related to api call

Dependencies
Python 3.7
Python Requests library https://docs.python-requests.org/
Python sys library
Python threading library
Python enum library
Python json library

***
The development and testing of the program are all under Windows Subsystem Linux environment
***

Usage (CLI tool)
1. Install all the dependencies
2. Complete the userinfo.json
   format: {"email":"your@email.com","token":"yourtoken"}
3. Run a linux terminal window
4. Type in command "python3 cli.py"
5. Follow the instructions to use the program
 
Usage (Unit test)
1. Install all the dependencies
2. Complete the userinfo.json
   format: {"email":"your@email.com","token":"yourtoken"}
3. Run a linux terminal window
4. Type in command "python3 test.py"


*Due to limit in api call, when displying all tickets in list this CLI can only show the first 100 tickets