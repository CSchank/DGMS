import ast
import networkx as nx
import matplotlib.pyplot as plt
from TokenGraph import TokenGraph

from Constants import *

class PythonGraph(TokenGraph):
    def __init__(self, code):
        self.tree = ast.parse(code)
        self.graph = TokenGraph()

        self.ast_to_networkx(self.tree)

    def add_const_to_graph(self, const, parent):
        if isinstance(const, str):
            for word in str.split(const):
                child = self.graph.add_node(word, is_syntax_token = True)
                self.graph.add_edge(parent,child)
        else:
            child = self.graph.add_node(str(const), is_syntax_token = True)
            self.graph.add_edge(parent, child)


    def ast_to_networkx(self, node):
        parent = None
        if isinstance(node, ast.Constant):
            # add "Constant" node
            constant_node = self.graph.add_node("Constant")

            # add node with constant
            self.add_const_to_graph(node.value, constant_node)

            return constant_node
        elif isinstance(node, ast.Name):
            # add "Name" node
            name_node = self.graph.add_node("Name")

            # add node with constant
            id_node = self.graph.add_node(node.id, is_syntax_token = True)
            self.graph.add_edge(name_node, id_node)

            return name_node
        elif isinstance(node, ast.Store):
            return self.graph.add_node("Store", is_syntax_token = True)
        elif isinstance(node, ast.AST):
            parent = self.graph.add_node(node.__class__.__name__, is_syntax_token = True)
        else:
            return self.graph.add_node(str(node), is_syntax_token = True)

        for child in ast.iter_child_nodes(node):
            child_node = self.ast_to_networkx(child)

            self.graph.add_edge(parent, child_node)

        return parent



if __name__ == "__main__":
    #code = input("Please enter the code you'd like to parse")

    code1 = "x = 1\ny = 2\nz = x + y * y"
    code2 = "print(\"Hello world\", 5)"
    code3 = "for i in range(4): print(\"Hello World {i}\")"
    code4 = "with open('file_path', 'w') as file:\n    file.write('hello world !')"
    python_graph = PythonGraph(code4)

    print(tokens_graph)

    print(ast.dump(python_graph.tree))

    networkx_graph = python_graph.graph

    python_graph.save_graph()


    # for node in ast.walk(tokens_graph.tree):
    #     if hasattr(node, 'lineno'):
    #         print("first token:", node.first_token)
    #         print(tokens_graph.get_text_range(node), node.__class__.__name__, tokens_graph.get_text(node))
    #         print("---------")

    # for layer, nodes in enumerate(nx.topological_generations(graph)):
    #     # `multipartite_layout` expects the layer as a node attribute, so add the
    #     # numeric layer value as a node attribute
    #     for node in nodes:
    #         graph.nodes[node]["layer"] = layer

    # print(labels)
    # for word in words: print(word, labels[word])

    # for i in range(len(words)-1):
    #     graph.add_edge(words[i],words[i+1], edge_attr=word_ordering)

    # pos = nx.multipartite_layout(graph, subset_key="layer", align="horizontal")

    # for k in pos:
    #     pos[k][1] = -pos[k][1]

    # show_labels = True

    # nx.draw(graph, pos=pos, with_labels=not show_labels)

    # edge_labels = {}
    # for fr, to, dict in list(graph.edges(data=True)):
    #     edge_labels[(fr,to)] = dict['edge_attr']

    # nx.draw_networkx_edge_labels(graph, pos, edge_labels)
    # if show_labels: nx.draw_networkx_labels(graph, pos=pos, labels=labels)
    # plt.show()