import networkx as nx
from  plfit import plfit
from matplotlib import pyplot as pl


"""
    Return a given statistic moment of a graph, where moment is the number of the moment
"""
def stat_moment(graph, moment):
    value = 0
    for node in graph.nodes_iter():
        value += graph.degree(node) ** moment
    return value / graph.number_of_nodes()


"""
    Process a graph, calculating its average degree, variance, second moment and making a 
    degree historgram (normalized), plotting it at the end
"""
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

"""
    Return the greatest component of a given graph
"""
def greatestComponent(graph):
    return max(nx.connected_component_subgraphs(graph), key = len)


""" 
    Initialize the graphs, where:
    pathFile: path to where is the file containing edge list 
    weighted: a bool variable, True if the graph is weighted and False if not
    directed: a bool variable, True if the graph is directed and False if not (it's used if you want to turn the graph to undirected)
    jumps: number of lines that need to be jumped so we can reach the list of edges

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


#Social Network
GraphSHamsterster = initGraph('./connexions/social/hamsterster.txt', False, False, 1)

#Infrastructure Network
GraphIPowerGrid = initGraph('./connexions/infrastructure/us-power-grid.txt', False, False, 2)

#Transport Network
GraphTEuroroad = initGraph('./connexions/transport/euroroad.txt', False, False, 2)
GraphTUSAir = initGraph('./connexions/transport/us-airports.txt', True, False, 2) #directed is False because we don't want to change it to undirected

#Calculating the Greates Component of each Graph
GCHamsterster = greatestComponent(GraphSHamsterster)
GCPowerGrid = greatestComponent(GraphIPowerGrid)
GCEuroroad = greatestComponent(GraphTEuroroad)
GCUSAir = greatestComponent(GraphTUSAir)

process_graph(GraphSHamsterster, 'Hamsterstes')
process_graph(GraphIPowerGrid, 'Power Grid')
process_graph(GraphTEuroroad, 'Euroroad')
process_graph(GraphTUSAir, 'US Airport')
