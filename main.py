from fastapi import FastAPI, Form, Response, Request, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# from twilio.twiml.messaging_response import MessagingResponse

# resp = MessagingResponse()
# msg = resp.message()
# msg.body('this is the response text')
# msg.media('https://example.com/path/image.jpg')


project_id = "herwork-tbs"
# Use a service account
cred = credentials.Certificate(r"C:\Users\cools\Downloads\herwork-service.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection(u'users')
services_ref = db.collection(u'services')
# cd c:/Users/cools/Desktop/GitHub/her_work_server/
# to run server
# python -m uvicorn main:app --reload
# uvicorn main:app --reload
# to access it from the internet
# ngrok http 8000
app = FastAPI()

# Get method to test whether server is working
@app.get("/")
def read_root():
    print("called get/")
    return {"Hello": "World"}


# Twilio Calls this post method
@app.post("/")
async def print_root(request: Request, From: str = Form(...), Body: str = Form(...) ):
    print("called post/")
    print(Body)
    print(type(From))
    if(Body=="!list"):
        docs = services_ref.where(u'contactNum', u'==', '+923172109965').stream()
        responseStr : str = f"Your Services:\n"
        for doc in docs:
            map = doc.to_dict()
            # print(f'{doc.id} => {map}')
            responseStr += map["serviceName"]+ "\n"
            for offer in map["offers"]:
                responseStr += offer["offerName"]+ "\n"
            responseStr += "\n"
        response = MessagingResponse()
        msg = response.message(responseStr)
        return Response(content=str(response), media_type="application/xml")
    elif(Body=="!search"):
        docs = services_ref.stream()
        responseStr : str = f"Your Results:\n"
        for doc in docs:
            map = doc.to_dict()
            if("Chef" in map["serviceName"]):
                # print(map)
                responseStr += map["serviceName"]+ " " + map["contactNum"]+"\n"
        print(responseStr)
        response = MessagingResponse()
        msg = response.message(responseStr)
        return Response(content=str(response), media_type="application/xml")
    # print(request.headers)
    # Request Source ip
    # client_host = request.client.host
    # print(client_host)
    return {"Hello": "World"}