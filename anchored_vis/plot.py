import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

print("LOADING DATASET")
df = pd.read_csv("./processed_data.csv")
df = np.array(df)
color_col = df[:,-2]

for i in range(len(color_col)):

    if color_col[i]=='C1CCCCC1':
        color_col[i] = 'red'
    if color_col[i] == "O=C(Nc1ccccc1)c1ccccc1":
        color_col[i] = 'blue'
    if color_col[i]=="c1ccc(-c2ccccc2)cc1":
        color_col[i] = 'grey'
    if color_col[i]=="c1ccc(COc2ccccc2)cc1":
        color_col[i] = 'brown'
    if color_col[i]=="c1ccc(Cc2ccccc2)cc1":
        color_col[i] = 'green'
    if color_col[i] == "c1ccc2[nH]ccc2c1":
        color_col[i] = 'pink'
    if color_col[i] == "c1ccc2ccccc2c1":
        color_col[i] = 'gold'
    if color_col[i] == "c1ccc2ncccc2c1":
        color_col[i] = 'yellow'
    if color_col[i] == "c1ccccc1":
        color_col[i] = "darkblue"
    if color_col[i] == "c1ccncc1":
        color_col[i] = 'black'

        print("DEBUG: ",color_col)

df = df[:,:-3]
print(df.shape)
print("LOADING AND PROCESSING DATASET COMPLETED")

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2,n_jobs=16,random_state=0)
#pca = PCA(n_components=2)
print("DOING TSNE")
red = tsne.fit_transform(df)
print("TSNE DONE")
plt.scatter(red[:,0],red[:,1],c=color_col)
plt.savefig("./GEM_10K_sub_50_50_1.5_2_TSNE.png")
plt.show()

# Now to generate the vtk file
file1 = open("./graph_points_TSNE.vtk","w")
file1.write("# vtk DataFile Version 2.0\nvtk output\nASCII\nDATASET POLYDATA\n")
file1.write("POINTS "+str(len(red)) + " float" + "\n")
for i in red:
    file1.write(str(i[0]) + " " + str(i[1]) + " 0\n" )

file1.write("POINT_DATA "+str(len(red))+"\n")
file1.write("FIELD FieldData 1\n")
file1.write("Category 1 " + str(len(red)) + " string\n")
for i in color_col:
        file1.write(str(i) + "\n")