from graphviz import Digraph
import zlib
import os.path as path
from os import scandir

class GitHistoryVisualizer:
	def __init__(self):
		self.dot = Digraph()
		self.repoPath = "D:\Programming\MIREA\Конфиг\Практика5\ConfigRepo"
		self.repoName = self.repoPath.split('\\')[-1]


	def ReadTree(self, commitHash):
		treePath = path.join(self.repoPath, ".git\\objects", commitHash[:2], commitHash[2:])
		with open(treePath, 'rb') as file:
			decompressedData = zlib.decompress(file.read())
			data = decompressedData.split(b'\x00')
			div = data[1].split()[0]

			result = []
			for i in data:
				if div in i:
					result.append(i.split()[-1].decode())

			return result


	def ReadCommit(self, commitHash):
		commitPath = path.join(self.repoPath, ".git\\objects", commitHash[:2], commitHash[2:])
		with open(commitPath, 'rb') as file:
			data = zlib.decompress(file.read()).split(b'\x00')
			sections = data[1].split(b'\n')
			commitData = data[1].split(b'\n\n')[1].decode()

			files = ""
			headData = None

			for section in sections:
				if b'tree' in section:
					files = '\n'.join(self.ReadTree(section.split()[1].decode()))
				if b'parent' in section:
					headData = self.ReadCommit(section.split()[1].decode())

			subData = f"{commitData}\n{files}"
			if headData is not None:
				self.AddBlock(headData, subData)

			return subData


	def AddBlock(self, headData, subData):
		self.dot.edge(headData, subData)


	def GetBranches(self):
		branchesDir = path.join(self.repoPath, ".git\\refs\\heads")
		branches = []

		for entry in scandir(branchesDir):
			branches.append(entry.name)

		return branches

	def BuildDotGraph(self):
		for branch in self.GetBranches():
			branchPath = path.join(self.repoPath, ".git\\refs\\heads", branch)
			with open(branchPath) as file:
				self.dot.format = 'png'
				self.ReadCommit(file.readline().strip())
				self.dot.render('input')
				self.dot.format = 'dot'
				self.dot.render('input')


if __name__ == "__main__":
	visualizer = GitHistoryVisualizer()
	visualizer.BuildDotGraph()