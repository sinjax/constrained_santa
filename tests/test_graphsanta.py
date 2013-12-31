import santa.graphsanta as graphsanta
from santa import Constraints
from santa import dag
people = {
	u"jade":{"invalid":[u"charlie"]},
	u"charlie":{"invalid":[u"jade"]},
	u"sina":{"invalid":[u"emma"]},
	u"emma":{"invalid":[u"sina"]},	
	u"al":{"invalid":[u"patrick",u"rikki",u"joss"]},
	u"joss":{"invalid":[u"al"]},
	u"darren":{"invalid":[]},
	# u"lucy":{"invalid":[u"darren"],},
	u"paul":{"invalid":[]},
	u"patrick":{"invalid":[u"rikki",u"al",u"briony"]},
	u"rikki":{"invalid":[u"al",u"patrick"]},
	u"briony":{"invalid":[u"patrick"]}

}
def confirm(pairs):
	sending = set([])
	recieving = set([])
	for sender,reciever in pairs.items():
		sending = sending | set([sender])
		recieving = recieving | set([reciever])

	if not len(recieving) == len(sending):
		return False,"more sending than getting"
	if not recieving == sending:
		return False,"Recieving is not equal to sending"
	if not recieving == set(people.keys()):
		return False,"Failed! recieving does not equal the people"
	
	return True,"passed"

def test_graphsanta():
	plist = people.keys()
	constraints = Constraints()
	for x in plist:
		constraints.add_constraints(x,people[x]["invalid"])
	for x in range(1000):
		pairs = graphsanta.allocate(plist,constraints)
		assert confirm(pairs)[0]

def test_valid_path():
	p = dag.ImutablePath()
	assert graphsanta.valid_path(p)
	p = p.iadd(p.node("a"))
	p = p.iadd(p.node("b"))
	p = p.iadd(p.node("c"))
	assert graphsanta.valid_path(p)
	p = p.iadd(p.node("a"))
	assert graphsanta.valid_path(p)
	p = p.iadd(p.node("c"))
	assert not graphsanta.valid_path(p)