# libraries
import networkx as nx
import numpy as np
import planarity
import progressbar


def get_network_PMFG(corr_matrix):
    
    """
    This function creates a filtered network starting from a correlation matrix using PMFG algorithm
        :param corr_matrix (numpy 2D-array)
        :return: returns filtered network (networkx Graph)
    """
    
    # get the list of links in decreasing order of weight
    rholist = []
    n = len(corr_matrix)
    for i in range(n):
        for j in range(n):
            if i > j:  # matrix is symmetric
                if corr_matrix[i][j] != 0:
                    rholist.append([abs(float(corr_matrix[i,j])), i, j]) # weight, node1, node2

    # sort the list in decreasing order
    rholist.sort(key=lambda x: x[0])
    rholist.reverse() 

    # initialize filtered matrix
    m = len(rholist) 
    filtered_matrix = np.zeros((n, n))
    control = 0
    
    # filtered graph
    G = nx.Graph()
    
    # get the filtered adjacency matrix using the PMFG algorithm
    # iterate over ordered edges
    for t in range(m):
            
        # stopping condition
        if control <= 3 * (n - 2) - 1:
                
            # get the current edge
            i = rholist[t][1]
            j = rholist[t][2]
            filtered_matrix[i,j] = rholist[t][0]

            # add the edge to the Graph
            G.add_edge(int(i), int(j), weight=filtered_matrix[i,j])
                
            # if the obtained G is not planarity we remove the edge
            if planarity.is_planar(G) == False:
                    
                # remove edge
                filtered_matrix[i,j] = 0
                control = control + 1
                G.remove_edge(int(i), int(j))
                    
        else:
            break
                    
    return filtered_matrix, G
