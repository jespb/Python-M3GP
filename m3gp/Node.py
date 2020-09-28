from .Constants import *
from random import randint, random

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

class Node:
	left = None
	right = None
	value = None

	def __init__(self,depth=MAX_DEPTH, left=None,value=None,right=None,full=False):
		if value == None:
			#i = randint(0,len(getTerminals())+len(OPERATORS)-1) # randint(a,b) = [a,b]
			#if i < len(OPERATORS) and depth > 1:
			if depth>1 and (random()<0.5 or full ==True ):
				i = randint(0,len(OPERATORS)-1)
				self.value = i
				self.left = Node(depth-1)
				self.right = Node(depth-1)
			else:
				self.value = randint(0,len(getTerminals())-1) # Sem literais
		else:
			self.left = left
			self.right=right
			self.value=value

	def __str__(self):
		if self.left == None:
			if isinstance(self.value,str):
				return self.value
			else:
				return getTerminals()[self.value]
		else:
			try:
				return "( " + str(self.left) + " " + OPERATORS[self.value] + " " + str(self.right) + " )"
			except:
				print(self.value)
				print(1/0)


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

	def getRandomNode(self, value=None):
		'''
		Returns a random Node within this Node.
		'''
		if value == None:
			value = randint(0,self.getSize()-1)
		if value == 0:
			return self

		left_size = self.left.getSize()
		if value <= left_size :
			return self.left.getRandomNode(value-1)
		else:
			return self.right.getRandomNode(value-left_size-1)



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
			return Node(left = None, value=self.value, right = None)
		else:
			return Node(left = self.left.clone(), value=self.value, right=self.right.clone())


	def calculate(self, sample):
		'''
		Returns the calculated value of a sample.
		'''
		if self.left == None:
			if isinstance(self.value,str):
				return float(self.value)
			else:
				return sample[self.value]
		else:
			if self.value == 0: #+
				return self.left.calculate(sample) + self.right.calculate(sample)
			if self.value == 1: #-
				return self.left.calculate(sample) - self.right.calculate(sample)
			if self.value == 2: #*
				return self.left.calculate(sample) * self.right.calculate(sample)
			if self.value == 3: #/
				right = self.right.calculate(sample)
				return self.left.calculate(sample) if right == 0 else self.left.calculate(sample) / self.right.calculate(sample)

	def isLeaf(self):
		'''
		Returns True if the Node had no sub-nodes.
		'''
		return self.left == None

	def getSemantics(self):
		'''
		Returns the semantic of a Node.
		'''
		ts = getTrainingSet()
		sem = []
		for sample in ts:
			sem.append(self.calculate(sample))
		return sem

	def redirect(self, other):
		'''
		Assigns the content of another Node to this Node.
		'''
		self.value = other.value
		self.left = other.left
		self.right = other.right

	def prun(self):
		'''
		Simplifies this Node
		'''
		semantics = self.getSemantics()
		semantics.sort()
		if semantics[0]== semantics[-1] and len(semantics)>1:
			self.value = str(semantics[0])
			self.left = None
			self.right = None
		# [+, -, *, /]
		
		# +
		if self.value == 0:
			# 0 + X == X
			if not self.isLeaf() and ( self.left.isLeaf() and self.left.value == "0.0" ):
				self.redirect(self.right)

			# X + 0 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value == "0.0" ):
				self.redirect(self.left)

			# X + X == 2 * X
			if not self.isLeaf() and ( str(self.right) == str(self.left) ):
				self.value = 2
				self.left = Node(value = "2.0")

		# - 
		if self.value == 1:
			# X - 0 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value == "0.0" ):
				self.redirect(self.left)

			# X - X == 0
			if not self.isLeaf() and ( str(self.right) == str(self.left) ):
				self.redirect( Node(value="0.0") )

		# * 
		if self.value == 2:
			# X * 0 == 0,  0 * X == 0
			if not self.isLeaf() and ( (self.left.isLeaf() and self.left.value=="0.0") or (self.right.isLeaf() and self.right.value=="0.0") ):
				self.redirect( Node(value="0.0") )

			# 1 * X == X
			if not self.isLeaf() and ( self.left.isLeaf() and self.left.value == "1.0" ):
				self.redirect(self.right)

			# X * 1 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value == "1.0" ):
				self.redirect(self.left)

		# //
		if self.value == 3:
			# X // 0 == 1
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value=="0.0" ):
				self.redirect( Node(value="1.0") )

			# X // 1 == X
			if not self.isLeaf() and ( self.right.isLeaf() and self.right.value=="1.0" ):
				self.redirect(self.left)

			# X // X == 1
			if not self.isLeaf() and ( str(self.right) == str(self.left) ):
				self.redirect( Node(value="1.0") )

		if self.left != None:
			self.left.prun()

		if self.right != None:
			self.right.prun()	
