import networkx as nx
import functools


def write_output(out:list):
    with open('output.txt', 'w') as f:
        for line in out:
            f.write(" ".join(line)+'\n')

def create_navigation_network(navigation_list, planets_info):
    G = nx.DiGraph()
    for line in navigation_list:
        lst = line.split()
        G.add_edge(lst[0], lst[1], weight=lst[2])
        #print(G.edges[lst[0], lst[1]]['weight'])

    for line in planets_info:
        lst = line.split()
        G.nodes[lst[0]]['species_list'] = lst[1:]
        #print(G.nodes[lst[0]]['species_list'])
    return G

def add(a, b):
  return int(a) + int(b)

def compare(a, b):
    return False if int(a) < int(b) else True

def divide_aliens(real_aliens_totake):
    tot= []
    for n, i in enumerate(real_aliens_totake):
        tot.append(str(i))
        tot.append(str(n))
    return tot

def sum_successors(current_node, network, iterat):
    
    max_pnt=0
    current_pnt = 0
    
    maxmax_pnt = 0
    currentmax_pnt = 0
    current_node_t = current_node
    
    for node1 in network.successors(current_node):
        current_node_t = node1
        for i in range(iterat):
            for node in network.successors(current_node_t):
                current_pnt = functools.reduce(lambda x, y: int(x)+int(y), network.nodes[node]['species_list']) - int(network.edges[current_node_t, node]['weight'])
                
                if  current_pnt > max_pnt:
                    max_pnt_it = current_pnt
                    max_node_it = node
            
            max_pnt += max_pnt_it
            current_node_t = max_node_it
        
        
        if  max_pnt > maxmax_pnt:
                maxmax_pnt = max_pnt
                max_node = node1
            


    return max_node, network.nodes[node]['species_list']


if __name__ == '__main__':
    with open('input') as f:
        lines = f.readlines()
        
    header = lines[0].split()
    max_planets = int(header[0])
    max_fuel = int(header[1])
    max_levels = int(header[2])

    levels_limit = lines[1].split()
    planets_info = lines[2:int(max_planets)+2]
    navigation_info = lines[int(max_planets)+2:]

    network = create_navigation_network(navigation_list=navigation_info, planets_info=planets_info)

    current_fuel = 0
    current_node = '0'
    out = []
    current_levels = [0]*10
    br = False
    
    while current_fuel < max_fuel:
        max_node, max_node_species_list = sum_successors(current_node, network,2)

        
         
        #current_levels = list(map(add, current_levels, network.nodes[max_node]['species_list']))
        
        for n, i in enumerate(current_levels):
            if int(i)+int(max_node_species_list[n]) < int(levels_limit[n]):
                max_node_species_list[n]= int(max_node_species_list[n])
                current_levels[n] += int(max_node_species_list[n])
            else:
                max_node_species_list[n] = (int(levels_limit[n]) - (int(current_levels[n])))
                current_levels[n] += (int(levels_limit[n]) - (int(current_levels[n])))
            
        real_aliens_totake = max_node_species_list
        if sum(real_aliens_totake)==0: break
        
        alien_division = divide_aliens(real_aliens_totake)
        
        out_t = alien_division+ [max_node]
        out.append(out_t)
        
        if current_node == '9998': break
        current_fuel += int(network.edges[current_node, max_node]['weight'])
        
        current_node = max_node
        
    
    out[-1] = out[-1][0:-1] + ['-1']
    

    write_output(out)
