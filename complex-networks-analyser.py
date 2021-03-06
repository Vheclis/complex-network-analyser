import powerlaw
import networkx as nx
from matplotlib import pyplot as pl


"""
    Return a given statistic moment of a graph, where moment is the number of
    the moment
"""
def stat_moment(graph, moment):
    value = 0
    for node in graph.nodes_iter():
        value += graph.degree(node) ** moment
    return value / graph.number_of_nodes()


"""
    Process a graph, calculating its average degree, variance, second moment and
    making a degree historgram (normalized), plotting it at the end
"""
def process_graph(graph, name):
    degree_histogram = nx.degree_histogram(graph)
    number_of_nodes = nx.number_of_nodes(graph)

    for index in range(len(degree_histogram)):
        degree_histogram[index] = degree_histogram[index] / number_of_nodes

    average_degree = 0
    for node in graph.nodes_iter():
        average_degree += graph.degree(node)

    average_degree /= number_of_nodes
    average_min_path = nx.average_shortest_path_length(graph)
    m1 = stat_moment(graph, 1)
    m2 = stat_moment(graph, 2)
    variance = m2 - (m1 ** 2)
    fit = powerlaw.Fit(degree_histogram)
    alpha = fit.power_law.alpha
    diameter = nx.diameter(graph)
    average_cluster_coeff = nx.average_clustering(graph)

    print('\n====== Graph {:s} ======'.format(name) )
    print('Alpha: {:.5f}'.format(alpha))
    if 2 < alpha < 3:
        print('The Graph is scale free')
    else:
        print('The Graph isnt scale free')
    print('Number of Nodes: {:.5f}'.format(number_of_nodes))
    print('Average Degree {:.5f}'.format(average_degree))
    print('Second Moment: {:.5f}'.format(m2))
    print('Variance: {:.5f}'.format(variance))
    print('Average Cluster Coefficient: {:.5f}'.format(average_cluster_coeff))
    print('Average Shortest Paths: {:.5f}'.format(average_min_path))
    print('Diameter: {:.5f}'.format(diameter))
    print('============================\n\n')
    #pl.title('Degree distribution: '+ name)
    #pl.loglog(degree_histogram, 'b.')
    #pl.show()

"""
    Return the greatest component of a given graph
"""
def greatestComponent(graph):
    return max(nx.connected_component_subgraphs(graph), key = len)


"""
    Initialize the graphs, where:
    pathFile: path to where is the file containing edge list ;
    weighted: a bool variable, True if the graph is weighted and False if not;
    directed: a bool variable, True if the graph is directed and False if not
        (it's used if you want to turn the graph to undirected);
    jumps: number of lines that need to be jumped so we can reach the list of
        edges.

"""
def initGraph(pathFile, weighted, directed, jumps):
    if(directed):
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    with open(pathFile, 'rb') as f:
        for counter in range(jumps):
            next(f,'')
        if(weighted):
            graph = nx.read_edgelist(f, nodetype = int, data=(('weight',int),))
        else:
            graph = nx.read_edgelist(f, nodetype = int)
    if(directed):
        graph = graph.to_undirected()

    return graph

#Calculating the Greates Component of each Graph
#Social Network
GCHamsterster = greatestComponent(initGraph('./connexions/social/hamster.txt', False, False, 0))
#Infrastructure Network
GCPowerGrid = greatestComponent(initGraph('./connexions/infrastructure/powergrid.txt', True, False, 0))
#Transport Network
GCEuroroad = greatestComponent(initGraph('./connexions/transport/euroroad.txt', False, False, 0))
GCUSAir = greatestComponent(initGraph('./connexions/transport/USairports.txt', True, False, 0))

process_graph(GCHamsterster, 'Hamsterstes')
process_graph(GCPowerGrid, 'Power Grid')
process_graph(GCEuroroad, 'Euroroad')
process_graph(GCUSAir, 'US Airport')
