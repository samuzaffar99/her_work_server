from fastapi import FastAPI, Request
# from twilio.twiml.messaging_response import MessagingResponse

# resp = MessagingResponse()
# msg = resp.message()
# msg.body('this is the response text')
# msg.media('https://example.com/path/image.jpg')

app = FastAPI()
# to run server
# uvicorn main:app --reload
# to access it from the internet
# ngrok http 8000

# Get method to test whether server is working
@app.get("/")
def read_root():
    print("called get/")
    return {"Hello": "World"}


# Twilio Calls this post method
@app.post("/")
async def print_root(request: Request):
    print("called post/")
    print(request)
    print(request.headers)
    # The data and event_handler name
    data = await request.json()
    print(data)
    # Request Source ip
    client_host = request.client.host
    print(client_host)
    return {"Hello": "World"}