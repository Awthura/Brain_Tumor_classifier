import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv(r'data\Brain Tumor.csv')
var_list = ['Mean','Variance','Standard Deviation','Entropy','Skewness','Kurtosis','Contrast','Energy','ASM',
'Homogeneity','Dissimilarity','Correlation','Coarseness']
#dfT= df.T
#print(dfT)
drop_list = ['Image','Class','Coarseness']
dfv = df.drop(drop_list,axis=1)
#dfv = dfv.astype({"Class": str})
print(dfv.dtypes)
#print(dfv.head())
#plt.hist(df[''])
#plt.scatter(df['Mean'], df['Variance'], alpha=0.2,
#            c=df['Class'], cmap='viridis') 

"""
corr = dfv.corr()
sns.heatmap(corr, square=True, annot=True)
plt.show() 
"""
print(df.describe())
print(df["Class"].unique())
g = sns.PairGrid(df, hue="Class", vars = ['Mean','Standard Deviation','Entropy','Skewness','Homogeneity','Dissimilarity'])
g.map_diag(sns.histplot)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.add_legend()
plt.show()