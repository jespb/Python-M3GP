import numpy as np

from math import log

import warnings
warnings.filterwarnings("ignore")

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2022 J. E. Batista
#

class Node:
	branches = None
	value = None


	def __init__(self):
		pass


	def create(self, rng, operators=None, terminals=None, depth=None,full=False):
		if depth>1 and (rng.random()<0.5 or full ==True ):
			op, n_args = operators[rng.randint(0,len(operators)-1)]
			self.value = op

			self.branches = []
			for i in range(n_args):
				n = Node()
				n.create(rng, operators, terminals, depth-1)
				self.branches.append(n)
		else:
			self.value = terminals[rng.randint(0,len(terminals)-1)] # Sem literais


	def copy(self,value=None, branches=None):
		self.branches = branches
		self.value=value


	def __str__(self):
		if self.branches == None:
			return str(self.value)
		else:
			if len(self.branches) == 2:
				return "( " + str(self.branches[0]) + " " + str(self.value) + " " + str(self.branches[1]) + " )"
			else:
				return str(self.value) + " ( " + " ".join( [str(b) for b in self.branches] ) + " )"


	def getSize(self):
		'''
		Returns the total number of nodes within this Node.
		'''
		if self.branches == None:
			return 1
		else:

			return 1 + sum( [b.getSize() for b in self.branches] )


	def getDepth(self):
		'''
		Returns the depth of this Node.
		'''
		if self.branches == None:
			return 1
		else:
			return 1 + max( [b.getDepth() for b in self.branches] )


	def getRandomNode(self, rng, value=None):
		'''
		Returns a random Node within this Node.
		'''
		if value == None:
			value = rng.randint(0,self.getSize()-1)
		if value == 0:
			#print(self)
			return self

		#print(value, self)
		for i in range(len(self.branches)):
			size = self.branches[i].getSize()
			if value-1 < size:
				return self.branches[i].getRandomNode(rng, value-1)
			value -= size


	def swap(self, other):
		'''
		Swaps the content of two nodes.
		'''
		b = self.branches
		v = self.value

		self.branches = other.branches
		self.value = other.value

		other.branches = b
		other.value = v


	def clone(self):
		'''
		Returns a clone of this node.
		'''
		if self.branches == None:
			n = Node()
			n.copy(value=self.value, branches = None)
			return n
		else:
			n = Node()
			n.copy(value=self.value, branches=[b.clone() for b in self.branches])
			return n



	def calculate(self, sample):
		'''
		Returns the calculated value of a sample.
		'''
		if self.branches == None:
			try:
				return np.array( sample[self.value] )#.astype("float64")
			except:
				return np.array( [float(self.value)]*sample.shape[0] )

				
		else:
			if self.value == "+": #+
				return self.branches[0].calculate(sample) + self.branches[1].calculate(sample)
			if self.value == "-": #-
				return self.branches[0].calculate(sample) - self.branches[1].calculate(sample)
			if self.value == "*": #*
				return self.branches[0].calculate(sample) * self.branches[1].calculate(sample)
			if self.value == "/": #/
				right = self.branches[1].calculate(sample)
				right = np.where(right==0, 1, right)
				return self.branches[0].calculate(sample) / right
			if self.value == "log2": # log2(X)
				res = self.branches[0].calculate(sample)
				res = np.where(res<=0, res, np.log2(res))
				return res
			if self.value == "max": # max( X0, X1, ... Xn)
				calc = [b.calculate(sample) for b in self.branches]
				a = []
				for i in range(len(calc[0])):
					a.append( max([calc[k][i] for k in range(len(calc))]) )
				return np.array(a)
				

	def isLeaf(self):
		'''
		Returns True if the Node had no sub-nodes.
		'''
		return self.branches == None

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
		self.branches = other.branches

	def prun(self, tr_x):
		'''
		Simplifies this Node
		'''
		semantics = self.getSemantics(tr_x)
		semantics.sort()
		if semantics[0]== semantics[-1] and len(semantics)>1:
			self.value = str(semantics[0])
			self.branches = None



		if self.branches!=None and len(self.branches)==1: # [log2]
			pass


		
		if self.branches!=None and len(self.branches)==2: # [+, -, *, /]
			# +
			if self.value == "+":
				# 0 + X == X
				if not self.isLeaf() and ( self.branches[0].isLeaf() and self.branches[0].value == "0.0" ):
					self.redirect(self.branches[1])

				# X + 0 == X
				if not self.isLeaf() and ( self.branches[1].isLeaf() and self.branches[1].value == "0.0" ):
					self.redirect(self.branches[0])

				# X + X == 2 * X
				if not self.isLeaf() and ( str(self.branches[1]) == str(self.branches[0]) ):
					self.value = "*"
					n = Node()
					n.copy(value = "2.0")
					self.branches[0].redirect( n )

			# - 
			if self.value == "-":
				# X - 0 == X
				if not self.isLeaf() and ( self.branches[1].isLeaf() and self.branches[1].value == "0.0" ):
					self.redirect(self.branches[0])

				# X - X == 0
				if not self.isLeaf() and ( str(self.branches[1]) == str(self.branches[0]) ):
					n = Node()
					n.copy(value = "0.0")
					self.redirect( n )

			# * 
			if self.value == "*":
				# X * 0 == 0,  0 * X == 0
				if not self.isLeaf() and ( (self.branches[0].isLeaf() and self.branches[0].value=="0.0") or (self.branches[1].isLeaf() and self.branches[1].value=="0.0") ):
					n = Node()
					n.copy(value = "0.0")
					self.redirect( n )

				# 1 * X == X
				if not self.isLeaf() and ( self.branches[0].isLeaf() and self.branches[0].value == "1.0" ):
					self.redirect(self.branches[1])

				# X * 1 == X
				if not self.isLeaf() and ( self.branches[1].isLeaf() and self.branches[1].value == "1.0" ):
					self.redirect(self.branches[0])

			# //
			if self.value == "/":
				# X // 0 == 1
				if not self.isLeaf() and ( self.branches[1].isLeaf() and self.branches[1].value=="0.0" ):
					n = Node()
					n.copy(value = "1.0")
					self.redirect( n )

				# X // 1 == X
				if not self.isLeaf() and ( self.branches[1].isLeaf() and self.branches[1].value=="1.0" ):
					self.redirect(self.branches[0])

				# X // X == 1
				if not self.isLeaf() and ( str(self.branches[1]) == str(self.branches[0]) ):
					n = Node()
					n.copy(value = "1.0")
					self.redirect( n )


		if self.branches!=None and len(self.branches)==3: # [max]
			pass




		if self.branches != None:
			for branch in self.branches:
				branch.prun(tr_x)