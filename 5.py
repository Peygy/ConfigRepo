from graphviz import Digraph
import zlib
import os.path as path
from os import listdir

#D: | cd D:\Programming\MIREA\Конфиг\Практика5\ConfigRepo | dot -Tpng input.dot -o output.png

class GitVisual:
	def __init__(self, repo_path: str):
		self.repoPath = repo_path
		self.repoName = repo_path.split('\\')[-1]
		self.dot = Digraph()

	def GetBranches(self) -> list:
		return listdir(path.join(self.repoPath, ".git", "refs", "heads"))

	def GetHeadPath(self) -> str:
		with open(path.join(self.repoPath, ".git", "HEAD")) as f:
			return f.readline().strip().split(" ")[1]

	def ReadTree(self, hash: str) -> list:
		with open(path.join(self.repoPath, ".git", "objects", hash[:2], hash[2:]), 'rb') as f:
			raw_data = zlib.decompress(f.read()).split(b'\x00')
			delim = raw_data[1].split()[0]
			return [i.split()[-1].decode() for i in raw_data if delim in i]

	def ReadCommit(self, hash: str):
		with open(path.join(self.repoPath, ".git", "objects", hash[:2], hash[2:]), 'rb') as f:
			raw_data = zlib.decompress(f.read()).split(b'\x00')
			commit_message = raw_data[1].split(b'\n\n')[1].decode()
			files = ""
			parent_message = None
			sections = raw_data[1].split(b'\n')
			for section in sections:
				if b'tree' in section:
					files = '\n'.join(self.ReadTree(section.split()[1].decode()))
				if b'parent' in section:
					parent_message = self.ReadCommit(section.split()[1].decode())
			child_message = commit_message + "\n" + files
			if parent_message is not None:
				self.AddBlock(parent_message, child_message)
			return child_message

	def AddBlock(self, parent_message: str, child_message: str):
		self.dot.edge(parent_message, child_message)

	def BuildDotGraph(self):
		for branch in self.GetBranches():
			with open(path.join(self.repoPath, ".git", "refs", "heads", branch)) as f:
				self.dot.format = 'png'
				self.ReadCommit(f.readline().strip())
				self.dot.render('input')
				self.dot.format = 'dot'
				self.dot.render('input')


if __name__ == "__main__":
	repo_path = "D:\Programming\MIREA\Конфиг\Практика5\ConfigRepo"
	git = GitVisual(repo_path)
	git.BuildDotGraph()
