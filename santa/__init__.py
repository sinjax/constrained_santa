class Constraints(object):
	"""Santa constraints"""
	def __init__(self):
		super(Constraints, self).__init__()
		self.constraints = {}


	def add_constraints(self,person,constraints):
		cons = self.constraints.get(person,[])
		cons += constraints
		self.constraints[person] = cons
	def add_constraint(self,person,other):
		self.addConstraints(person,[other])
	
	def is_allowed(self,person,other):
		return\
			other not in self.constraints.get(person,[])\
			and person is not other