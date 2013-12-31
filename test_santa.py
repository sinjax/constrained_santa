import oldsanta as santa
import copy
from IPython import embed

def test_pair():
	broken = 0
	for x in range(10000):
		pairs = santa.pairThePeople(santa.cpeople(),"")
		passed,msg = santa.confirm(pairs)
		if not passed:
			broken += 1
			print msg
	if broken is 0:
		print "all passed"
	else:
		print "Failures: %d"%broken
	
