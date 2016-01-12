import commands
import urllib
import urllib2
import json
from twisted.web import client
from twisted.internet import reactor, defer
import bash

token = "173353654:AAG3Xxh92Aei4IP5ofTLohZitLFk4qv08YM"

scrollback = []

shell = bash.Shell()
scrollback.append(("_The Story So Far_", shell.readUntilBlocking()))

def handleMessageResponse(results):
    print("finished replying!")
    print(results)

def handleScrollbackResponse(results):
    print("finished sending scrollback!")
    print(results)

def sendScrollback(chat_id):
    backlog = ""
    for message, response in scrollback:
        boldMessage = "*{0}*".format(message)
        backlog += boldMessage + "\n" + response
    params = { 'parse_mode' : 'Markdown', 'chat_id' : chat_id, 'text' : backlog }
    param_string = urllib.urlencode(params)
    url = "https://api.telegram.org/bot{0}/sendMessage?{1}".format(token, param_string)
    print("replying")
    client.getPage(url).addCallback(handleScrollbackResponse)

def reply(chat_id, message):
    if message.startswith('/scrollback'):
        sendScrollback(chat_id)
        return;
    print("running command...");
    shell.runCommand(message)
    print("ran command, reading result...");
    response = shell.readUntilBlocking()
    print("got response from shell!");
    params = { 'chat_id' : chat_id, 'text' : response }
    param_string = urllib.urlencode(params)
    url = "https://api.telegram.org/bot{0}/sendMessage?{1}".format(token, param_string)
    print("replying")
    client.getPage(url).addCallback(handleMessageResponse)
    scrollback.append((message, response))
    
def getMessageId(message):
    if not 'chat' in message:
        return 0
    if not 'id' in message['chat']:
        return 0
    return message['chat']['id']

def handleUpdate(results, offset):
    print("finished polling.")
    parsed_results = json.loads(results) 
    if not parsed_results['ok']:
        print("error: {0}".format(results))
        return
    for result in parsed_results['result']:
        print("processing result {0}", result)
        if not 'message' in result:
            continue
        message = result['message']
        if not 'text' in message:
            continue
        text = message['text']
        print(text)
        reply(getMessageId(message), text)
        print("done replying")
        if not 'update_id' in result:
            print("continuing")
            continue
        if result['update_id'] >= offset:
            offset = result['update_id'] + 1
    print("updated offset is {0}".format(offset))
    checkForUpdates(offset)
    
def checkForUpdates(offset):
    print("polling...")
    params = { 'timeout' : 1000, 'offset' : offset }
    param_string = urllib.urlencode(params)
    url = "https://api.telegram.org/bot{0}/getUpdates?{1}".format(token, param_string)
    print(url)
    client.getPage(url).addCallback(handleUpdate, offset)

checkForUpdates(0)
reactor.run()
