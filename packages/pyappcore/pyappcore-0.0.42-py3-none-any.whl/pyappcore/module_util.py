#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union
import builtins
import os
from .str_util import GetSplitFilePath


#------------------------------------------------------------------------
# 노드.
#------------------------------------------------------------------------
class Node:
	name : str
	path : str
	isPackage : bool
	parent : Node
	children : list

	def __init__(self, name : str = "", path : str = "", parent : Node = None, isPackage : bool = False):
		self.name = name
		self.path = path # fullname
		self.isPackage = isPackage
		self.parent = parent		
		self.children = list()

	def __repr__(self, level : int = 0):
		ret = "\t" * level + repr(self.name) + "\n"
		for child in self.children:
			ret += child.__repr__(level + 1)
		return ret
	
	def AddChild(self, childNode):
		childNode.parent = self
		self.children.append(childNode)
	
	@staticmethod
	def IsPackage(path : str) -> bool:
		if not os.path.isdir(path):
			return False
		
		initFilePath = os.path.join(path, "__init__.py")
		if not os.path.isfile(initFilePath):
			return False

		return True

	@staticmethod
	def BuildTree(path : str, parent : Node = None) -> Node:
		name = os.path.basename(path)
		node = Node(name, path, parent, True)
		for childName in os.listdir(path):
			childPath = os.path.join(path, childName)
			if os.path.isdir(childPath):
				if Node.IsPackage(childPath):
					child = Node.BuildTree(childPath, node)
					node.AddChild(child)
			else:
				cpath, cname, cextension = GetSplitFilePath(childPath)				
				if not cextension.endswith(".py"):
					continue
				if cname == "__init__":
					continue
				child = Node(cname, childPath, parent, False)
				node.AddChild(child)
		return node

	@staticmethod
	def PrintTree(node : Node, prefix : str = "", usePrint : bool = True, moduleFullNames : dict[str, str] = None) -> None:
		if node.isPackage:
			path = f"{prefix}.{node.name}" if prefix else node.name
			if usePrint:
				builtins.print(f"package: {path}")
			for child in node.children:
				Node.PrintTree(child, path, usePrint, moduleFullNames)
		else:
			path = f"{prefix}.{node.name}" if prefix else node.name
			if usePrint:
				builtins.print(f"module: {path}")
			if not moduleFullNames is None:
				moduleFullNames[path] = node.name

	@staticmethod
	def GetModuleNames(node : Node) -> dict[str, str]:
		moduleFullNames = dict()
		Node.PrintTree(node, "", False, moduleFullNames)
		return moduleFullNames