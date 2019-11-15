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

	def __init__(self,depth=MAX_DEPTH, left=None,value=None,right=None):
		if value == None:
			i = randint(0,len(getTerminals())+len(OPERATORS)) # randint(a,b) = [a,b]
			if i < len(OPERATORS) and depth > 1:
				self.value = i
				self.left = Node(depth-1)
				self.right = Node(depth-1)
			else:
				self.value = randint(0,len(getTerminals()))-1
				if self.value == -1:
					self.value *= random()
		else:
			self.left = left
			self.right=right
			self.value=value

	def __str__(self):
		if self.left == None:
			return str(-self.value if self.value < 0 else getTerminals()[self.value])
		else:
			return "( " + str(self.left) + " " + OPERATORS[self.value] + " " + str(self.right) + " )"

	def getSize(self):
		if self.left == None:
			return 1
		else:
			return self.left.getSize() + 1 + self.right.getSize()

	def getDepth(self):
		if self.left == None:
			return 1
		else:
			return 1 + max(self.left.getDepth(),self.right.getDepth())

	def getRandomNode(self, value=None):
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
		if self.left == None:
			return Node(left = None, value=self.value, right = None)
		else:
			return Node(left = self.left.clone(), value=self.value, right=self.right.clone())


	def calculate(self, sample):
		if self.left == None:
			return -self.value if self.value < 0 else sample[self.value]
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
