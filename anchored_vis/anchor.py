import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from openTSNE import TSNE
import json
import os

def anchor(filename):
    with open(filename, 'r') as f:
        # Load the JSON data into a Python dictionary
        mapper = json.load(f)
    sub_mapper = []
    for i in mapper["mapper"]["nodes"]:
        temp_sample = list(i["vertices"])
        sub_mapper.append(temp_sample)
    df = pd.read_csv("./CLI_examples/wrangled_data.csv")
    df = df.values.astype(np.float32)
    tsne = TSNE(n_components=2,n_jobs=32,negative_gradient_method='fft')
    red = tsne.fit(df)



    node_anchors = []
    for i in range(len(mapper["mapper"]["nodes"])):
        anchor_x = 0
        anchor_y = 0
        for j in sub_mapper[i]:
            anchor_x = red[j][0] + anchor_x
            anchor_y = red[j][1] + anchor_y
        
        mapper["mapper"]["nodes"][i]['avgs']['anchor_x'] = float(anchor_x/len(sub_mapper[i]))
        mapper["mapper"]["nodes"][i]['avgs']['anchor_y'] = float(anchor_y/len(sub_mapper[i]))
        node_anchors.append([anchor_x/len(sub_mapper[i]),anchor_y/len(sub_mapper[i])])


    from sklearn.cluster import KMeans
    node_anchors = np.array(node_anchors)
    kmeans = KMeans(n_clusters=15, random_state=0, n_init="auto").fit(node_anchors)

    for i in range(len(mapper["mapper"]["nodes"])):

        mapper["mapper"]["nodes"][i]['avgs']['cluster'] = int(kmeans.labels_[i]) 


    k_clusters = []
    for i in kmeans.cluster_centers_:
        k_clusters.append({"x":float(i[0]),"y":float(i[1])})

    mapper["mapper"]["k_clusters"] = k_clusters

    with open(filename, "w") as f:
        json.dump(mapper, f)


# color_col = df[sub_sample,-2]

# for i in range(len(color_col)):

#     if color_col[i]=='C1CCCCC1':
#         color_col[i] = 'red'
#     if color_col[i] == "O=C(Nc1ccccc1)c1ccccc1":
#         color_col[i] = 'blue'
#     if color_col[i]=="c1ccc(-c2ccccc2)cc1":
#         color_col[i] = 'grey'
#     if color_col[i]=="c1ccc(COc2ccccc2)cc1":
#         color_col[i] = 'brown'
#     if color_col[i]=="c1ccc(Cc2ccccc2)cc1":
#         color_col[i] = 'green'
#     if color_col[i] == "c1ccc2[nH]ccc2c1":
#         color_col[i] = 'pink'
#     if color_col[i] == "c1ccc2ccccc2c1":
#         color_col[i] = 'gold'
#     if color_col[i] == "c1ccc2ncccc2c1":
#         color_col[i] = 'yellow'
#     if color_col[i] == "c1ccccc1":
#         color_col[i] = "darkblue"
#     if color_col[i] == "c1ccncc1":
#         color_col[i] = 'black'


# df = df[sub_sample,:-3]
# print(df.shape)
# print("LOADING AND PROCESSING DATASET COMPLETED")


# plt.scatter(red[:,0],red[:,1],c=color_col)
# plt.savefig("./GraphMAE_finetuned_500_40_5_5_TSNE.png")
# plt.show()

# # Now to generate the vtk file
# file1 = open("./graph_points_TSNE.vtk","w")
# file1.write("# vtk DataFile Version 2.0\nvtk output\nASCII\nDATASET POLYDATA\n")
# file1.write("POINTS "+str(len(red)) + " float" + "\n")
# for i in red:
#     file1.write(str(i[0]) + " " + str(i[1]) + " 0\n" )

# file1.write("POINT_DATA "+str(len(red))+"\n")
# file1.write("FIELD FieldData 1\n")
# file1.write("Category 1 " + str(len(red)) + " string\n")
# for i in color_col:
#         file1.write(str(i) + "\n")