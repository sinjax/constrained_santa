class Node(object):
	"""DAGNode"""
	def __init__(self,obj):
		super(Node, self).__init__()
		self.obj = obj

	def __eq__(self,other):
		return self.obj == other.obj
	def __hash__(self):
		return hash(self.obj)
	def __str__(self):
		return str(self.obj)

class Edge(object):
	"""DAG edge"""
	def __init__(self, left,right):
		super(Edge, self).__init__()
		self.left = left
		self.right = right

	def __eq__(self,other):
		return self.left == other.left and self.right == other.right
	def __hash__(self):
		return hash((self.left,self.right))



		
class DAG(object):
	"""The directed graph"""
	def __init__(self,):
		super(DAG, self).__init__()
		self._nodes = set([])
		self._leftedges = {}
		self._rightedges = {}
		self._edges = set([])
	def node(self,obj):
		node = Node(obj)
		self._nodes = self._nodes | set([node])
		return node
	def connect(self,left,right):
		edge = Edge(left,right)
		if edge in self._edges: 
			return edge
		
		if not left in self._nodes: self._nodes = self._nodes | set([left])
		if not right in self._nodes: self._nodes = self._nodes | set([right])
		if not left in self._leftedges:
			self._leftedges[left] = []
		if not right in self._rightedges:
			self._rightedges[right] = []
		self._leftedges[left] += [edge]
		self._rightedges[right] += [edge]
		self._edges = self._edges | set([edge])
		return edge
	def children(self,node):
		if not node in self._nodes:
			return []
		ret = []
		for edge in self._leftedges.get(node,[]):
			ret += [edge.right]
		return ret
	def parents(self,node):
		if not node in self._nodes:
			return []
		ret = []
		for edge in self._rightedges.get(node,[]):
			ret += [edge.left]
		return ret
	def nodes(self):
		return [x for x in self._nodes]
	def __str__(self):
		ret = []
		for x in self.nodes():
			for child in self.children(x):
				ret += ["%s -> %s"%(str(x),str(child))]
		return "\n".join(ret)
	def size(self):
		return len(self._nodes)
	def edgesize(self):
		return len(self._edges)

	def parentless_nodes(self):
		return self._nodes - set(self._rightedges.keys())

import copy
class ImutablePath(DAG):
	"""docstring for Path"""
	def __init__(self):
		super(ImutablePath, self).__init__()
		self.current = None

	def iadd(self,next):
		ret = copy.deepcopy(self)
		if self.current is None:
			ret.current = next
		else:
			ret.connect(self.current,next)
			ret.current = next
		return ret
