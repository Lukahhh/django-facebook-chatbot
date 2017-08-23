from django.shortcuts import render

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import os, json, requests
from pprint import pprint

from fb_bot.process import process

def post_facebook_message(fbid, received_message):
    access_token = os.environ["FB_MESS_ACCESS_TOKEN"]
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % (access_token)

    message_list = process(received_message)

    for message in message_list:
        response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": message}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
        print("Status:")
        pprint(status.json())

# Create your views here.
class Bot(generic.View):
    def get(self, request, *args, **kwargs):
        verify_token = os.environ["FB_MESS_VERIFY_TOKEN"]
        if self.request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token.')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incomming_message = json.loads(self.request.body.decode('utf-8'))

        for entry in incomming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    print("Message:")
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])

        return HttpResponse()
