import json
from Improve_vis import pie

def find_index(id,list):
    index=0
    for i in list:
        if(i['id']==str(id+1)):
            return index
        index = index + 1

def improve_vis(mapper,filename):
    
    # with open('./CLI_examples/pos.json', 'r') as f:
    #     # Load the JSON data into a Python dictionary
    #     mapper = json.load(f)
    file1 = open("./shots/graph_points.vtk","w")
    file1.write("# vtk DataFile Version 2.0\nvtk output\nASCII\nDATASET POLYDATA\n")
    file1.write("POINTS "+str(len(mapper)) + " float" + "\n")
    for i in mapper:
        file1.write(str(i["x"]) + " 0 " + str(i["y"]) + "\n" )

    file2 = open("./shots/graph_edges.vtk","w")
    file2.write("# vtk DataFile Version 2.0\nvtk output\nASCII\nDATASET POLYDATA\n")
    file2.write("POINTS "+str(len(mapper)) + " float" + "\n")
    for i in mapper:
        file2.write(str(i["x"]) + " 0 " + str(i["y"]) + "\n" )

    with open(filename, 'r') as f:
        # Load the JSON data into a Python dictionary
        mapper = json.load(f)

    file1.write("POINT_DATA "+str(len(mapper["mapper"]["nodes"]))+"\n")
    file1.write("FIELD FieldData 1\n")
    file1.write("Category 1 " + str(len(mapper["mapper"]["nodes"])) + " string\n")
    print(len(mapper["mapper"]["nodes"]))
    for i in mapper["mapper"]["nodes"]:
            max_key = max(i["categorical_cols_summary"]["scaffold"], key=i["categorical_cols_summary"]["scaffold"].get)
            file1.write(str(max_key) + "\n")
    
    if 'toxicity' in mapper['col_keys']:
        file1.write("SCALARS toxicity float 1\n")
        file1.write("LOOKUP_TABLE default\n")
        count = 1
        for i in mapper["mapper"]["nodes"]:
                file1.write(str(i["avgs"]["toxicity"]) + "\n")
                count = count +1
        
    if 'solubility' in mapper['col_keys']:
        file1.write("SCALARS solubility float 1\n")
        file1.write("LOOKUP_TABLE default\n")
        count = 1
        for i in mapper["mapper"]["nodes"]:
                file1.write(str(i["avgs"]["solubility"]) + "\n")
                count = count +1
    

    file2.write("LINES " + str(len(mapper["mapper"]["links"])) + " " + str(3*len(mapper["mapper"]["links"])) + "\n")
    for i in mapper["mapper"]["links"]:
        file2.write("2 " + str(find_index(i["source"]-1,mapper["mapper"]["nodes"])) + " " + str(find_index(i["target"]-1,mapper["mapper"]["nodes"])) + "\n")

    file1.close()
    file2.close()
    pie.pie(filename)