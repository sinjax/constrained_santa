# -*- coding: utf-8 -*-
#!/usr/bin/env python

import random
import codecs
from IPython import embed
import sys, smtplib,string,copy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

people = {
	u"jade":{"invalid":[u"charlie"],"email":"EMAILS_REMOVED"},
	u"charlie":{"invalid":[u"jade"],"email":"EMAILS_REMOVED"},
	u"sina":{"invalid":[u"emma"],"email":"EMAILS_REMOVED"},
	u"emma":{"invalid":[u"sina"],"email":"EMAILS_REMOVED"},	
	u"al":{"invalid":[u"patrick",u"rikki",u"joss"],"email":"EMAILS_REMOVED"},
	u"joss":{"invalid":[u"al"],"email":"EMAILS_REMOVED"},
	u"darren":{"invalid":[],"email":"EMAILS_REMOVED"},
	# u"lucy":{"invalid":[u"darren"], "email":"EMAILS_REMOVED"},
	u"paul":{"invalid":[],"email":"EMAILS_REMOVED"},
	u"patrick":{"invalid":[u"rikki",u"al",u"briony"],"email":"EMAILS_REMOVED"},
	u"rikki":{"invalid":[u"al",u"patrick"],"email":"EMAILS_REMOVED"},
	u"briony":{"invalid":[u"patrick"],"email":"EMAILS_REMOVED"}

}
fromaddr = "ss@ecs.soton.ac.uk"

def unicodeEmail(utfMsg,subject):
	msg = MIMEMultipart("alternative")
	part1 = MIMEText(utfMsg,"plain", "utf-8")
	msg["Subject"] = subject
	msg.attach(part1)
	print msg.as_string().encode('ascii')
	return msg.as_string().encode('ascii')
	

def sendPairs(pairs,toOveride=None,subject=u""):
	# The actual mail send
	print sys.argv
	server = smtplib.SMTP('smtp.ecs.soton.ac.uk')
	server.login( sys.argv[1] , sys.argv[2] )
	
	for msg in pairs:
		toAddress = msg[2]
		if toOveride is not None:
			toAddress = toOveride
		# print fromaddr
		# unicodeMail = unicodeEmail(msg[0]%msg[1])
		unicodeMail = msg[0]%msg[1]
		# print toAddress
		# print unicodeMail
		server.sendmail(fromaddr, toAddress, unicodeEmail(unicodeMail,subject%msg[1]))

	server.quit()

def printPairs(pairs,name="santa"):
	print "Here are the %s pairs:"%name
	for msg in pairs:
		print msg[1]['from'], msg[1]['target'], "With this email: %s"%(msg[2])

def pairThePeople(people,msg,existing=None):
   a = None
   while True:
       try:
           a = _pairThePeople(people,msg,existing)
           break
       except Exception, e:
       		pass
   return a
def _pairThePeople(people,msg,existing=None):
	if existing is not None:
		existing = dict([(data['person'],set([data['target']])) for (x,data,x) in existing])
	else:
		existing = {}
	
	availablePeople = set([x for x in people.keys()])

	# Choose the invalid people first
	constraintKeys = [(len(people[person]['invalid']) + len(existing.get(person,set([]))),person) for person in people]
	constraintKeys.sort()
	constraintKeys.reverse()
	
	# Randomising the constrained people's order
	constraintKeysFixed = []
	constraintKeysDict = dict()
	current = []
	for x in constraintKeys:
		if(not x[0] in constraintKeysDict):
			current = random.sample(current,len(current))
			for y in current:
				constraintKeysFixed += [y]
			current = []
			constraintKeysDict[x[0]] = []
		current += [x]
	
	# fix for last entry
	current = random.sample(current,len(current))
	for y in current:
		constraintKeysFixed += [y]
	constraintKeysDict[x[0]] = []
	# done randomising the constrained people's order
	
	messages = []
	# history = []
	constraintKeys = random.sample(constraintKeys,len(constraintKeys)) # completely random
	# constraintKeys = constraintKeysFixed # random inside invalid
	# otherwise no random, same order every time
	
	# Read the code
	code = codecs.open("santa.py",encoding="utf-8").read()
	for order,person in constraintKeys:
		# history += ["Picking for %s"%person]
		toaddrs  = [people[person]['email']]
		# history += ["Available people: %s"%str(availablePeople)]
		# history += ["Available people: %s"%str(availablePeople)]
		validPeople = availablePeople - (set(people[person]['invalid'])|set([person])|existing.get(person,set([])))
		# history += ["Allowable people include %s"%str(validPeople)]
		# Let them have who they live with?
		if(len(validPeople) == 0): 
			# print "Nope, ballsed it, try again..."
			# print "here's the history: "
			# print "\n".join(history)
			raise Exception("Something went wrong, try the script again")
		target = random.sample(validPeople,1)
		# history += ["Picked %s"%str(target)]
		availablePeople -= set(target)
		people[target[0]]['invalid'] += [person]
		# history += ["Remaining available %s"%str(availablePeople)]
		messages.append([msg,{"person":person,"target":target[0],"code":code,"from":person},toaddrs])
	return messages

def printPairs(pairs):

	for pairing in pairs:
		print "from %s -> to %s"%(pairing[1]["from"], pairing[1]["target"])

def confirm(pairs):
	sending = set([])
	recieving = set([])
	for pairing in pairs:
		sending = sending | set([pairing[1]["from"]])
		recieving = recieving | set([pairing[1]["target"]])

	if not len(recieving) == len(sending):
		return False,"more sending than getting"
	if not recieving == sending:
		return False,"Recieving is not equal to sending"
	if not recieving == set(people.keys()):
		return False,"Failed! recieving does not equal the people"
	
	print sending
	print recieving
	return True,"passed"

def cpeople():
	return copy.deepcopy(people)

def go():
	try:

		mainMessage = u"""
also, send me a reply so I know it worked please :-)

PLEASE DO NOT INCLUDE THIS MESSAGE IN YOUR REPLY. 
if you do I'll know who your secret santa is and that will make me a SAD PANDA.

no one did this last year, let's make this 4 in a row people!

this is the second santa assignment of 2013. This is the correct one. Please disregard previous santa

--- Blurb ---

Greetings, friends. Last year Al was your santa operator (sant-o-perator), this year you're back with Sina
This year brought to you in glorious unicode, so: メリークリスマスのブタ!
	
The main present limit is still £20. This worked well for the last four years, and there didn't seem to be any objections. Don't worry if that seems 
like a stretch - simply make something yourself, claiming that "you can't put a price on hard work". Or, buy something cheap, and wildly inflate the price - nobody 
will know! 

HOWEVER. The mini-santa is being altered this year against the principles of 
"the rikki plan". Instead of buying a small toy/game/book for around £5 for an individual person, this year
everyone is asked to go out and spend £5 on a toy the whole group can enjoy. This is basically what
ends up happening anyway, for example: the buffy board game went down a treat... and everyone loves atmosphere.
Note that if you buy a book for the group you'll be expected to read passages from the book.

But yeah... a little toy...a small game...a puzzle... again from a charity shop or Ebay for around £5 that the whole
group can enjoy. 

To recap: main present: £20 LIMIT for a specific person, small present, 5 GBP, charity shop/Ebay, "a toy for the group". 

Let's make it REAL!

For your pleasure, here is the code (in python)
--- CODE ---
%(code)s
------"""

		bigSanta = u"""
Your secret Santa is: %(target)s. Go out and buy %(target)s a gift under £20. 
"""+mainMessage
		bigSantaPairs = pairThePeople(copy.deepcopy(people),bigSanta)
		# smallSantaPairs = None
		smallSanta = u"""
Your mini-secret Santa is: everyone! Go out and buy a single mini-gift under £5 that everyone can enjoy on the day. From a charity shop, or second-hand from Ebay.
	""" + mainMessage
		smallSantaPairs = pairThePeople(people,smallSanta,bigSantaPairs)
		# First test, print the santas
		# printPairs(bigSantaPairs,"Big Santa")
		# printPairs(smallSantaPairs,"Small Santa")
		# Second test, send the santa emails, send them all to sina
		# sendPairs(bigSantaPairs,fromaddr,subject=u"Main-Secret Santa For %(person)s")
		# sendPairs(smallSantaPairs,fromaddr,subject=u"Mini-Secret Santa For all your friends!")
		# Real thing, send the santa emails!
		sendPairs(bigSantaPairs,subject=u"Main-Secret Santa For %(person)s")
		sendPairs(smallSantaPairs,subject=u"Mini-Secret Santa For all your friends!")
		
		return [bigSantaPairs,smallSantaPairs]
	except Exception, e:
		raise e

if __name__ == '__main__':
	go()