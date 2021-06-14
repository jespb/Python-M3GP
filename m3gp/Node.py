import numpy as np

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
#

class Node:
	left = None
	right = None
	value = None


	def __init__(self):
		pass


	def create(self, rng, operators=None, terminals=None, depth=None,full=False):
		if depth>1 and (rng.random()<0.5 or full ==True ):
			self.value = operators[rng.randint(0,len(operators)-1)]
			self.left = Node()
			self.left.create(rng, operators, terminals, depth-1)
			self.right = Node()
			self.right.create(rng, operators, terminals, depth-1)
		else:
			self.value = terminals[rng.randint(0,len(terminals)-1)] # Sem literais


	def copy(self, left=None,value=None,right=None):
		self.left = left
		self.right=right
		self.value=value


	def __str__(self):
		if self.left == None:
			return str(self.value)
		else:
			return "( " + str(self.left) + " " + str(self.value) + " " + str(self.right) + " )"


	def getSize(self):
		'''
		Returns the total number of nodes within this Node.
		'''
		if self.left == None:
			return 1
		else:
			return self.left.getSize() + 1 + self.right.getSize()


	def getDepth(self):
		'''
		Returns the depth of this Node.
		'''
		if self.left == None:
			return 1
		else:
			return 1 + max(self.left.getDepth(),self.right.getDepth())


	def getRandomNode(self, rng, value=None):
		'''
		Returns a random Node within this Node.
		'''
		if value == None:
			value = rng.randint(0,self.getSize()-1)
		if value == 0:
			return self

		left_size = self.left.getSize()
		if value <= left_size :
			return self.left.getRandomNode(rng, value-1)
		else:
			return self.right.getRandomNode(rng, value-left_size-1)


	def swap(self, other):
		'''
		Swaps the content of two nodes.
		'''
		l = self.left
		v = self.value
		r = self.right
		self.left = other.left
		self.value = other.value
		self.right = other.right
		other.left = l
		other.value = v
		other.right = r


	def clone(self):
		'''
		Returns a clone of this node.
		'''
		if self.left == None:
			n = Node()
			n.copy(left = None, value=self.value, right = None)
			return n
		else:
			n = Node()
			n.copy(left = self.left.clone(), value=self.value, right=self.right.clone())
			return n



	def calculate(self, sample):
		'''
		Returns the calculated value of a sample.
		'''
		if self.left == None:
			try:
				return np.array( sample[self.value] )#.astype("float64")
			except:
				return np.array( [float(self.value)]*sample.shape[0] )

				
		else:
			if self.value == "+": #+
				return self.left.calculate(sample) + self.right.calculate(sample)
			if self.value == "-": #-
				return self.left.calculate(sample) - self.right.calculate(sample)
			if self.value == "*": #*
				return self.left.calculate(sample) * self.right.calculate(sample)
			if self.value == "/": #/
				right = self.right.calculate(sample)
				right = np.where(right==0, 1, right)
				return self.left.calculate(sample) / right


	def isLeaf(self):
		'''
		Returns True if the Node had no sub-nodes.
		'''
		return self.left == None

	def getSemantics(self,tr_x):
		'''
		Returns the semantic of a Node.
		'''		
		return self.calculate(tr_x)

	def redirect(self, other):
		'''
		Assigns the content of another Node to this Node.
		'''
		self.value = other.value
		self.left = other.left
		self.right = other.right

	def prun(self, tr_x):
		'''
		Simplifies this Node
		'''
		semantics = self.getSemantics(tr_x)
		semantics.sort()
		if semantics[0]== semantics[-1] and len(semantics)>1:
			self.value = str(semantics[0])
			self.left = None
			self.right = None
		# [+, -, *, /]
		
		# +
		if self.value == "+":
			# 0 + X == X
			if not self.isLeaf() and ( self.left.isLeaf() and self.left.value == "0.0" ):
				self.redirect(self.right)

			# X + 0 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value == "0.0" ):
				self.redirect(self.left)

			# X + X == 2 * X
			if not self.isLeaf() and ( str(self.right) == str(self.left) ):
				self.value = "*"
				n = Node()
				n.copy(value = "2.0")
				self.left.redirect( n )

		# - 
		if self.value == "-":
			# X - 0 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value == "0.0" ):
				self.redirect(self.left)

			# X - X == 0
			if not self.isLeaf() and ( str(self.right) == str(self.left) ):
				n = Node()
				n.copy(value = "0.0")
				self.redirect( n )

		# * 
		if self.value == "*":
			# X * 0 == 0,  0 * X == 0
			if not self.isLeaf() and ( (self.left.isLeaf() and self.left.value=="0.0") or (self.right.isLeaf() and self.right.value=="0.0") ):
				n = Node()
				n.copy(value = "0.0")
				self.redirect( n )

			# 1 * X == X
			if not self.isLeaf() and ( self.left.isLeaf() and self.left.value == "1.0" ):
				self.redirect(self.right)

			# X * 1 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value == "1.0" ):
				self.redirect(self.left)

		# //
		if self.value == "/":
			# X // 0 == 1
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value=="0.0" ):
				n = Node()
				n.copy(value = "1.0")
				self.redirect( n )

			# X // 1 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value=="1.0" ):
				self.redirect(self.left)

			# X // X == 1
			if not self.isLeaf() and ( str(self.right) == str(self.left) ):
				n = Node()
				n.copy(value = "1.0")
				self.redirect( n )

		if self.left != None:
			self.left.prun(tr_x)

		if self.right != None:
			self.right.prun(tr_x)	
