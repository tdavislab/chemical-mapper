import json
#from graph_decomposition import Graph
import os
import shutil
import linecache
import csv

# First this file needs the json file of the single component
def extract_comp(c_id,file_name):
    file = open(file_name)
    data = json.load(file)
    final_json = {'mapper':{'nodes':[],'links':[]},'connected_components':[],'col_keys':[],'categorical_cols':[]}
    c_nodes = data['connected_components'][c_id]
    # For the nodes
    for i in c_nodes:
        final_json['mapper']['nodes'].append(data['mapper']['nodes'][i])
    # For the connected components
    ar = []
    for i in range(len(c_nodes)):
        ar.append(i)
    final_json['connected_components'].append(ar)

    # For col_keys and categorical_cols
    final_json['col_keys'] = data['col_keys']
    final_json['categorical_cols'] = data['categorical_cols']
    
    # Now coming to links
    ids = []
    for i in final_json['mapper']['nodes']:
        ids.append(i['id'])
    for i in data['mapper']['links']:
        if i['source']-1 in c_nodes:
            final_json['mapper']['links'].append(i)
            
    
    folder_name = './comp_analysis/'
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.mkdir(folder_name)
    with open('./comp_analysis/final_component.json', 'w') as fp:
        json.dump(final_json, fp)

    #decomposition("./CLI_examples/comp_analysis/final_component.json")

    


# #Create adjacency list
# def create_adjacency(file_name):
#     file = open(file_name)
#     data = json.load(file)
#     adj_list = {}
#     for i in range(len(data['mapper']['nodes'])):
#         adj_list[int(data['mapper']['nodes'][i]['id'])] = []

#     for i in data['mapper']['links']:
#         adj_list[i['source']].append(i['target'])
#         adj_list[i['target']].append(i['source'])

#     return adj_list

# def set_default(obj):
#     if isinstance(obj, set):
#         return list(obj)
    
# def decomposition(filename):

#     # Take input the graph component from the json file
#     dic = create_adjacency(filename)
#     obj = Graph.graph(dic)
#     file = open(filename)
#     data = json.load(file)
#     # Create id_list
#     ids = []
#     for i in data['mapper']['nodes']:
#         ids.append(i['id'])

#     obj.find_stars()
#     obj.find_cycles()
#     '''
#     # To create the csv files
#     if os.path.exists("./CLI_examples/comp_analysis/CSV"):
#         shutil.rmtree("./CLI_examples/comp_analysis/CSV")

#     os.mkdir('./CLI_examples/comp_analysis/CSV')
#     title = ['substructure','node_number','smiles']
#     final_csv = [title]
#     for cycle in obj.cycles:
#         for i in range(len(cycle)-1):
#             node = cycle[i]
#             for vertex in data['mapper']['nodes'][ids.index(str(node))]['vertices']:
#                 line = linecache.getline("./CLI_examples/processed_data.csv", vertex+2)
#                 struc = line.split(',')[-1]
#                 struc = struc.replace('"','')
#                 print(struc)
#                 final_csv.append(['cycle_'+str(i),node,struc])

#     with open('./CLI_examples/comp_analysis/CSV/cycles.csv', 'w') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(final_csv)
    
#     obj.find_stars()
#     final_csv = [title]
#     for star in obj.stars:
#         for i in range(len(star)-1):
#             node = star[i]
#             for vertex in data['mapper']['nodes'][ids.index(str(node))]['vertices']:
#                 line = linecache.getline("./CLI_examples/processed_data.csv", vertex+2)
#                 struc = line.split(',')[-1]
#                 struc = struc.replace('"','')
#                 final_csv.append(['star_'+str(i),node,struc])

#     with open('./CLI_examples/comp_analysis/CSV/stars.csv', 'w') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(final_csv)
#     '''
#     print("CSV SKIPPED")
#     print("CYCLES: ", obj.cycles)

#     '''
#     for i in obj.cycles:
#         for j in i:
#             obj.del_node(j)
    
#     for i in obj.stars:
#         for j in i:
#             obj.del_node(j)
#     obj.branch_decomposition()
#     '''
#     # Now coming to writing it into seperate .json files
#     file = open(filename)
#     data = json.load(file)
#     # Let us start with stars
#     if os.path.exists("./CLI_examples/comp_analysis/stars"):
#         shutil.rmtree("./CLI_examples/comp_analysis/stars")
#     os.mkdir("./CLI_examples/comp_analysis/stars")
#     count = 0 

#     for star in obj.stars:


#         final_json = {'mapper':{'nodes':[],'links':[]},'connected_components':[],'col_keys':[],'categorical_cols':[]}

#         ids = []
#         for i in data['mapper']['nodes']:
#             ids.append(int(i['id']))

#         for i in star:
#             final_json['mapper']['nodes'].append(data['mapper']['nodes'][ids.index(i)])
        
#         ar = []
#         for i in range(len(final_json['mapper']['nodes'])):
#             ar.append(i)

#         final_json['connected_components'].append(ar)

#         final_json['col_keys'] = data['col_keys']
#         final_json['categorical_cols'] = data['categorical_cols']

#         ids = []
#         for i in final_json['mapper']['nodes']:
#             ids.append(int(i['id']))

#         for i in data['mapper']['links']:
#             if i['source'] in ids and i['target'] in ids:
#                 final_json['mapper']['links'].append(i)



#         with open('./CLI_examples/comp_analysis/stars/final_star' + str(count)+ '.json', 'w') as fp:
#             json.dump(final_json, fp,default=set_default)

#         count = count + 1

#     count = 0

#     # Let us start with cycles
#     if os.path.exists("./CLI_examples/comp_analysis/cycles"):
#         shutil.rmtree("./CLI_examples/comp_analysis/cycles")
#     os.mkdir("./CLI_examples/comp_analysis/cycles")

#     for cycle in obj.cycles:

#         cycle = cycle[:-1]

#         final_json = {'mapper':{'nodes':[],'links':[]},'connected_components':[],'col_keys':[],'categorical_cols':[]}

#         ids = []
#         for i in data['mapper']['nodes']:
#             ids.append(int(i['id']))

#         for i in cycle:
#             final_json['mapper']['nodes'].append(data['mapper']['nodes'][ids.index(i)])
        
#         ar = []
#         for i in range(len(final_json['mapper']['nodes'])):
#             ar.append(i)

#         final_json['connected_components'].append(ar)

#         final_json['col_keys'] = data['col_keys']
#         final_json['categorical_cols'] = data['categorical_cols']

#         ids = []
#         for i in final_json['mapper']['nodes']:
#             ids.append(int(i['id']))

#         for i in data['mapper']['links']:
#             if i['source'] in ids and i['target'] in ids:
#                 final_json['mapper']['links'].append(i)



#         with open('./CLI_examples/comp_analysis/cycles/final_cycle' + str(count)+ '.json', 'w') as fp:
#             json.dump(final_json, fp,default=set_default)

#         count = count + 1

# '''
#     count = 0

#     # Let us start with paths
#     if os.path.exists("./CLI_examples/comp_analysis/paths"):
#         shutil.rmtree("./CLI_examples/comp_analysis/paths")
#     os.mkdir("./CLI_examples/comp_analysis/paths")

#     for path in obj.paths:

#         final_json = {'mapper':{'nodes':[],'links':[]},'connected_components':[],'col_keys':[],'categorical_cols':[]}

#         ids = []
#         for i in data['mapper']['nodes']:
#             ids.append(int(i['id']))

#         for i in path:
#             final_json['mapper']['nodes'].append(data['mapper']['nodes'][ids.index(i)])
        
#         ar = []
#         for i in range(len(final_json['mapper']['nodes'])):
#             ar.append(i)

#         final_json['connected_components'].append(ar)

#         final_json['col_keys'] = data['col_keys']
#         final_json['categorical_cols'] = data['categorical_cols']

#         ids = []
#         for i in final_json['mapper']['nodes']:
#             ids.append(int(i['id']))

#         for i in data['mapper']['links']:
#             if i['source'] in ids and i['target'] in ids:
#                 final_json['mapper']['links'].append(i)



#         with open('./CLI_examples/comp_analysis/paths/final_path' + str(count)+ '.json', 'w') as fp:
#             json.dump(final_json, fp,default=set_default)

#         count = count + 1

# '''





