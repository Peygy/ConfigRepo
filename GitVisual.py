from graphviz import Digraph
import zlib
import os.path as path
from os import listdir

#D:\Programming\MIREA\Конфиг\Практика5\ConfigRepo

class GitVisual:
	def __init__(self, repo_path: str):
		self.repo_path = repo_path
		self.repo_name = repo_path.split('\\')[-1]
		self.dot = Digraph(comment=f'Commits graph for {self.repo_name}', strict=True)

	def get_branches(self) -> list:
		return listdir(path.join(self.repo_path, ".git", "refs", "heads"))

	def get_head_path(self) -> str:
		with open(path.join(self.repo_path, ".git", "HEAD")) as f:
			return f.readline().strip().split(" ")[1]

	def read_tree(self, hash: str) -> list:
		with open(path.join(self.repo_path, ".git", "objects", hash[:2], hash[2:]), 'rb') as f:
			raw_data = zlib.decompress(f.read()).split(b'\x00')
			delim = raw_data[1].split()[0]
			return [i.split()[-1].decode() for i in raw_data if delim in i]

	def read_commit(self, hash: str):
		with open(path.join(self.repo_path, ".git", "objects", hash[:2], hash[2:]), 'rb') as f:
			raw_data = zlib.decompress(f.read()).split(b'\x00')
			commit_message = raw_data[1].split(b'\n\n')[1].decode()
			files = ""
			parent_message = None
			sections = raw_data[1].split(b'\n')
			for section in sections:
				if b'tree' in section:
					files = '\n'.join(self.read_tree(section.split()[1].decode()))
				if b'parent' in section:
					parent_message = self.read_commit(section.split()[1].decode())
			child_message = commit_message + "\n" + files
			if parent_message is not None:
				self.add_edge(parent_message, child_message)
			return child_message

	def build_graph(self):
		for branch in self.get_branches():
			with open(path.join(self.repo_path, ".git", "refs", "heads", branch)) as f:
				self.dot = Digraph(comment=f'Commits graph for {self.repo_name}, branch {branch}', strict=True)
				self.read_commit(f.readline().strip())
				self.render_graph(f'input.dot')

	def render_graph(self, output_file='commit_graph', view=True):
		self.dot.format = 'png'
		self.dot.render(output_file, view=view)

	def add_edge(self, parent_message: str, child_message: str):
		self.dot.edge(parent_message, child_message)


if __name__ == "__main__":
	repo_path = "D:\Programming\MIREA\Конфиг\Практика5\ConfigRepo"
	if path.exists(repo_path):
		git = GitVisual(repo_path)
		git.build_graph()
