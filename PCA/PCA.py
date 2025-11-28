import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
data = pd.read_csv("./PCA/processed_data.csv")
features = []
for i in  range(32):
    features.append("Col"+str(i))

x = data.loc[:,features].values
print(x)
y = data.loc[:,['Scaffold']].values
print(y)

tsne = TSNE(n_components=2, random_state=42)
principalComponents = tsne.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['1', '2'])

print(principalDf)

# Encode the 'Scaffold' column if it is categorical
#label_encoder = LabelEncoder()
#data['Scaffold'] = label_encoder.fit_transform(data['Scaffold'])

data['Scaffold'] = data['Scaffold'].replace({"c1ccccc1": "#00008B", "O=C(Nc1ccccc1)c1ccccc1": "blue","c1ccncc1":"black","c1ccc2ccccc2c1":"gold","C1CCCCC1":"red","c1ccc(Cc2ccccc2)cc1":"green", "c1ccc2[nH]ccc2c1":"pink", "c1ccc(-c2ccccc2)cc1":"grey","c1ccc2ncccc2c1":"yellow","c1ccc(COc2ccccc2)cc1":"brown"})
finalDf = pd.concat([principalDf, data[['Scaffold']]], axis = 1)
print(finalDf)

# Create a scatter plot
finalDf.plot.scatter(x='1', y='2',c='Scaffold',cmap='viridis')

# Add title and labels
plt.title('Scatter Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')


# Show the plot
plt.show()