import commands
import urllib
import urllib2
import json
from twisted.web import client
from twisted.internet import reactor, defer

token = "173353654:AAG3Xxh92Aei4IP5ofTLohZitLFk4qv08YM"

def handleMessageResponse(results):
    print("finished replying!")
    print(results)

def reply(chat_id, message):
    result = str(commands.getstatusoutput(message))
    params = { 'chat_id' : chat_id, 'text' : result }
    param_string = urllib.urlencode(params)
    url = "https://api.telegram.org/bot{0}/sendMessage?{1}".format(token, param_string)
    print("replying")
    client.getPage(url).addCallback(handleMessageResponse)
    
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
        reply(82066642, text)
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
