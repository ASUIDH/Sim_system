import os
import random

import networkx as nx

def getdictGraph(basePath,queryNodeMd5):
    nodePath = os.path.join(basePath, "graph.node")
    edgePath = os.path.join(basePath, "graph.edge")
    name_id, id_name, id_type = getId(nodePath)
    queryNode = name_id[queryNodeMd5]
    typeid_type = [] # 这个就是 "categories"
    type_typeid = {}
    subGraph , pos = getSubGraph(basePath,queryNode,name_id, id_name, id_type)
    nodes = [] #nodes
    links = [] #links
    for node,attr in subGraph.nodes().items():
        nodeDict = {}
        nodeDict["id"] = str(node)
        if attr['type'] not in type_typeid:
            type_typeid[attr['type']] = len(type_typeid)
            typeid_type.append({'name' : attr['type']})
        nodeDict["category"] = type_typeid[attr['type']] # 动态编码生成id
        nodeDict["name"] = attr['name']
        nodeDict["x"] = pos[node][0] * 1000
        nodeDict["y"] = pos[node][1] * 1000
        nodeDict["symbolSize"] = 20 if id_type[node] == "pefile" else 3
        nodeDict["value"] = 100 if id_type[node] == "pefile" else 10
        # vaule 可能是大小
        # symbol size可能是lable大小，这些先不加
        nodes.append(nodeDict)
    for edge in subGraph.edges():
        linkDict = {   "source": str(edge[0]),
                       "target": str(edge[1])}
        links.append(linkDict)
    return nodes,links,typeid_type


def getSubGraph(basePath,queryNode,name_id,id_name,id_type):
    edgePath = os.path.join(basePath,"graph.edge")
    edges = getedge(edgePath)
    G = nx.Graph()
    G.add_edges_from(edges)
    nodesSet = set()
    nodesSet.add(queryNode)
    nei1 = set()
    nei1Before = set(G.neighbors(queryNode))
    for node in nei1Before:
        if '@' in id_name[node] or "?" in id_name[node]:
            continue
        if random.randint(1, 100) < 12 :
            nei1.add(node)
    nodesSet |= (nei1)
    nei2 = set()
    for node in nei1:
        nei2 |= set(G.neighbors(node))
    for node in nei2 :
        if id_type[node] == "pefile" and random.randint(1, 100) < 10 :
            nodesSet.add(node)
    subGraph =  G.subgraph(nodesSet)
    for node in nodesSet:
        subGraph.nodes[node]["type"] = id_type[node]
        subGraph.nodes[node]["name"] = id_name[node]
    pos = nx.drawing.spring_layout(subGraph)
    return subGraph,pos,
def getId(graphPath):
 name_id = {}
 id_name = {}
 id_type = {}
 with open(graphPath) as f:
     for line in f.readlines():
         arr = line.strip().split()
         id = int(arr[0])  # id是一个int
         type = arr[1]
         name = arr[2]
         name_id[name] = id
         id_name[id] = name
         id_type[id] = type
 return name_id, id_name,id_type
def getedge(edgePath):
    edges = []
    with open (edgePath) as f:
        for line in f.readlines():
            arr = [int(node) for  node in line.strip().split("\t")]
            edges.append(arr)
    return edges

if __name__ == "__main__" :
    """
    g,pos = getSubGraph(
        "D:\\MD-data\\vt\\vt",
        0
    )
    for node,att in g.nodes().items():
        print(node)
        print(att)
    print(g)
    print(pos)
    print(g.edges())
    """
    nodes,links,cat = getdictGraph("D:\\MD-data\\vt\\vt",
        "0f65ec92b0929f58442cf942d0138e05")
    print(len(nodes))
    print(len(links))
    print(cat)