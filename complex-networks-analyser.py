import networkx as nx
from matplotlib import pyplot as pl

def stat_moment(graph, moment):
	value = 0
	for node in graph.nodes_iter():
		value += graph.degree(node) ** moment
	return value / graph.number_of_nodes()

def process_graph(graph, name):
	degree_histogram = nx.degree_histogram(graph)
	number_of_nodes = nx.number_of_nodes(graph)

	for index in range(len(degree_histogram)):
		degree_histogram[index] = degree_histogram[index] / number_of_nodes

	m1 = stat_moment(graph, 1)
	m2 = stat_moment(graph, 2)
	variance = m2 - (m1 ** 2)
	print('M1: {:.5f}'.format(m1))
	print('M2: {:.5f}'.format(m2))
	print('Variance: {:.5f}'.format(variance))
	pl.title('Degree distribution: '+ name)
	pl.loglog(degree_histogram, 'b.')
	pl.show()


Ga = nx.MultiGraph()
with open('./out.topology', 'rb') as f:
	next(f,'')
	for line in f:
		edges = line.split()
		for i in range(int(edges[2])):
			Ga.add_edge(edges[0],edges[1])

Gb = nx.Graph()
with open('./out.opsahl-powergrid', 'rb') as f:
	next(f,'')
	next(f,'')
	Gb = nx.read_edgelist(f, nodetype=int)


process_graph(Ga, 'Internet Topology')
process_graph(Gb, 'Power Grid')