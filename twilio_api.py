import urllib2

from twilio_config import *


def send_sms(segment, body):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, URL, ACCOUNT_KEY, ACCOUNT_TOKEN)
    auth_handler = urllib2.HTTPBasicAuthHandler(passman)
    # auth_handler.add_password(realm=None,
    #                           uri=URL,
    #                           user=ACCOUNT_KEY,
    #                           passwd=ACCOUNT_TOKEN)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    req = urllib2.Request(URL)
    req.add_data('sms=True&Segment=%s&Body=%s' % (segment, body))
    f=urllib2.urlopen(req)
    print f.read()

if __name__ == "__main__":
    send_sms("DevOps","hello from twilio")