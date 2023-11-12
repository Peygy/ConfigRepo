import os
import zlib

def read_git_object(sha):
    object_path = os.path.join('.git', 'objects', sha[:2], sha[2:])
    with open(object_path, 'rb') as f:
        content = zlib.decompress(f.read()).decode('utf-8')
    return content

def parse_commit(commit_data):
    lines = commit_data.split('\n')
    tree_sha = lines[0].split()[1]
    parent_shas = [line.split()[1] for line in lines[1:] if line.startswith('parent')]
    return tree_sha, parent_shas

def parse_tree(tree_data):
    lines = tree_data.split('\n')
    entries = []
    for line in lines:
        if line:
            parts = line.split()
            mode = parts[0]
            if len(parts) == 3:  # File or Directory mode
                name, sha = parts[2], parts[1]
                entries.append((mode, name, sha))
            elif len(parts) == 2 and parts[1] == 'commit':  # Submodule mode
                name, sha = parts[0], parts[1]
                entries.append((mode, name, sha))
    return entries

def build_dot_graph(sha, parent_shas):
    dot = f'digraph commit_{sha} {{\n'
    dot += f'  label = "Commit {sha}"\n'
    for parent_sha in parent_shas:
        dot += f'  commit_{parent_sha} -> commit_{sha}\n'
    dot += build_dot_tree(sha)
    dot += '}\n'
    return dot

def build_dot_tree(sha):
    tree_data = read_git_object(sha)
    entries = parse_tree(tree_data)
    dot = ''
    for mode, name, child_sha in entries:
        if mode == '100644' or mode == '040000':  # File or Directory mode
            dot += f'  {mode}_{child_sha} [label="{name}", shape={"box" if mode == "100644" else "folder"}]\n'
            dot += f'  commit_{sha} -> {mode}_{child_sha}\n'
            if mode == '040000':  # If it's a directory, recursively build its tree
                dot += build_dot_tree(child_sha)
    return dot

def main():
    # Предполагаем, что у вас есть корректный sha последнего коммита
    latest_commit_sha = '24a05845708c8eab14c7d670ec5c1ea9f29fea60'

    commit_sha = latest_commit_sha
    while commit_sha:
        commit_data = read_git_object(commit_sha)
        tree_sha, parent_shas = parse_commit(commit_data)
        dot_graph = build_dot_graph(commit_sha, parent_shas)
        print(dot_graph)

        commit_sha = parent_shas[0] if parent_shas else None

if __name__ == '__main__':
    main()