import requests

# get the total number of ticket in the account. Only used to check whether email-tokoen pair is validate
def get_count(auth):
    try:
        response = requests.get("https://zccyuyanggbai.zendesk.com/api/v2/tickets/count.json",auth=auth)
    except:
        return "failed", "api call failed"
    if response.status_code<300:
        return "success","auth correct"
    else:
        return "failed","auth wrong"

# get one ticket by id
def get_ticket_by_id(auth,id):
    # add padding to format output
    padding = 10 * " "
    try:
        response = requests.get("https://zccyuyanggbai.zendesk.com/api/v2/tickets/"+str(id)+".json",auth=auth)
    except:
        print(padding,"API called failed")
        return "fail"
    # api call unsuccessful
    if response.status_code>300:
        print(padding,"Error: ",response.json()["error"])
        return "fail"

    # ID not found
    if "Error" in response.json():
        print(padding,response.json())
        return "fail"
    else:
        # print important info of the ticket
        ticket = response.json()["ticket"]
        print("ticket id: ",ticket["id"])
        print("created at: ", ticket["created_at"])
        print("requester id: ",ticket["requester_id"])
        print("subject: ",ticket["subject"])
        print("description: ", ticket["description"])
        return "success"


# get a list of all tickets
def list_tickets(auth,page):
    # add padding to format output
    padding = 10 * " "
    try:
        response = requests.get("https://zccyuyanggbai.zendesk.com/api/v2/tickets.json",auth=auth)
    except:
        print(padding,"API called failed")
        return "fail"
    # api call unsuccessful
    if response.status_code>300:
        print(padding,"Error: ",response.json()["error"])
        return "fail"
    tickets = response.json()["tickets"]
    # no ticket on the current page
    if page*25>=len(tickets):
        return "too large page"
    if page<0:
        return "too small page"
    # the last ticket to show
    if len(tickets)>25*page+25:
        upperlimit = 25*page+25
    else:
        upperlimit = len(tickets)
    # format output
    print(padding,"id"+2*" "+"subject")
    for i in range(25*page,upperlimit):
        print(padding,tickets[i]["id"],end="")
        print((4-len(str(tickets[i]["id"])))*" ",end="")
        print(tickets[i]["subject"])
    return "success", page
