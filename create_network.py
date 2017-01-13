from __future__ import absolute_import, print_function

from collections import defaultdict
import yaml
import networkx as net
import matplotlib.pyplot as matplot

my_graph = net.Graph() # empty undirected graph
users = []
friendship_table = defaultdict(list) #dictionary of lists

with open("my_friends_info.txt", 'r') as text_file:
    for line in text_file:
        if line.startswith('{') == True:    #read in user data
            tw_user = {}
            tw_user = yaml.load(line)   #yaml parses dictionary
            users.append(tw_user)

        elif line.startswith('[') == True:  #read in follower ids
            friend_list = []
            friend_list = [follower_id.strip('[| |\n |]') for follower_id in line.split(',')]
            friendship_table[users[-1]['screen_name']] = friend_list
#Create nodes
for i in users:
    my_graph.add_node(i['screen_name'])

#Create edges by checking friendship
for i in users:
    for node in my_graph:
        if (i['id_str'] in friendship_table[node]) and not (i['screen_name'] in node):
            my_graph.add_edge(node,i['screen_name'])

#Get Degrees of each node
data = []
for node in my_graph:
    data.append(len(my_graph.edges(node)))

#Draw Network
#Print some Stats of the Network
n = net.number_of_nodes(my_graph)
text = "Number of Nodes: "+str(n)
matplot.text(x=.15,y=1.15, s=text,horizontalalignment='center',weight='bold')

avg_degree = sum(data)/len(data)
text1 = "Average Degree: " +str(avg_degree)
matplot.text(x=.15,y=1.10, s=text1,horizontalalignment='center',weight='bold')

pos = net.spring_layout(my_graph, k=.35)
net.draw_networkx(my_graph,pos)
matplot.savefig("my_friend_network_spring_layout.png")
matplot.title("My Friends")


#Display Clustering Coefficient above each node
for node in my_graph:
    cluster_coeff = str(net.clustering(my_graph,node))
    x,y = pos[node]
    matplot.text(x,y+.05,s = cluster_coeff[0:5] , bbox=dict(facecolor='blue', alpha=0.6),horizontalalignment='center')
matplot.show()

#Degree Distribution Chart
x_axis =[]
y_axis = []
n = float(n)
for i in range(max(data)+1):
    x_axis.append(i) #0,1,2,3 .....
    y_axis.append(float(data.count(i)/n))

matplot.bar(x_axis, y_axis, align='center' ,width=1.00, color="cyan")
matplot.xlabel('Degree')
matplot.ylabel('Fraction of Nodes')
matplot.title("Degree Distribution in My Friends Network")
matplot.savefig('degree_distribution.png')
matplot.show()
