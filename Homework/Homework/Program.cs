using System;
using System.Collections.Generic;
using System.IO;
using GiGraph.Dot.Output.Options;
using GiGraph.Dot.Types.Graphs;
using GiGraph.Dot.Types.Nodes;
using GiGraph.Dot.Entities.Graphs;
using GiGraph.Dot.Extensions;
using GiGraph.Dot.Entities.Nodes;

class GitGraphVisualizer
{
    static void Main()
    {
        Console.WriteLine("Git Graph Visualizer");

        string repoPath = "D:\\Programming\\MIREA\\Конфиг\\Практика5\\ConfigRepo\\.git";

        if (repoPath != null)
        {
            var dotGraph = GenerateDotGraph(repoPath);
            SaveDotGraphToFile(dotGraph);
            Console.WriteLine("DOT file generated successfully: git_graph.dot");
        }
        else
        {
            Console.WriteLine("Not a valid git repository.");
        }
    }

    static DotGraph GenerateDotGraph(string repoPath)
    {
        var graph = new DotGraph();

        HashSet<string> processedCommits = new HashSet<string>();

        ProcessCommit(repoPath, "HEAD", graph, processedCommits);

        return graph;
    }

    static void ProcessCommit(string repoPath, string commitHash, DotGraph graph, HashSet<string> processedCommits)
    {
        if (processedCommits.Contains(commitHash))
        {
            return;
        }

        processedCommits.Add(commitHash);

        string commitPath = Path.Combine(repoPath, "objects", commitHash.Substring(0, 2), commitHash.Substring(2));

        if (File.Exists(commitPath))
        {
            string commitContent = File.ReadAllText(commitPath);
            string[] lines = commitContent.Split('\n');
            foreach (string line in lines)
            {
                if (line.StartsWith("tree "))
                {
                    string treeHash = line.Substring(5, 40);
                    ProcessTree(repoPath, treeHash, graph, processedCommits);
                }
            }
        }
    }

    static void ProcessTree(string repoPath, string treeHash, DotGraph graph, HashSet<string> processedCommits)
    {
        string treePath = Path.Combine(repoPath, "objects", treeHash.Substring(0, 2), treeHash.Substring(2));

        if (File.Exists(treePath))
        {
            string treeContent = File.ReadAllText(treePath);
            string[] lines = treeContent.Split('\n');
            foreach (string line in lines)
            {
                string[] parts = line.Split(' ');
                string objectType = parts[1];
                string objectHash = parts[2];
                string objectName = parts[3];

                var node = new DotNode(objectHash);
                node.Label = objectName;
                graph.Nodes.Add(node);

                if (objectType == "tree")
                {
                    ProcessTree(repoPath, objectHash, graph, processedCommits);
                }
                else if (objectType == "blob")
                {
                    ProcessBlob(repoPath, objectHash, objectName, graph, processedCommits);
                }
            }
        }
    }

    static void ProcessBlob(string repoPath, string blobHash, string blobName, DotGraph graph, HashSet<string> processedCommits)
    {
        var node = new DotNode(blobHash);
        node.Label = blobName;
        graph.Nodes.Add(node);
    }

    static void SaveDotGraphToFile(DotGraph graph)
    {
        try
        {
            using (StreamWriter sw = new StreamWriter("./file.dot"))
            {
                sw.WriteLine(graph.Build());
            }
            Console.WriteLine("Файл успешно создан");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Произошла ошибка при создании файла: {ex.Message}");
        }
    }

}