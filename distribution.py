# importing the required libraries
from sklearn import datasets
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setting up the Data Frame
iris = datasets.load_iris()

iris_df = pd.DataFrame(iris.data, columns=['Sepal_Length',
                                           'Sepal_Width', 'Patal_Length', 'Petal_Width'])

iris_df['Target'] = iris.target

iris_df['Target'].replace([0], 'Iris_Setosa', inplace=True)
iris_df['Target'].replace([1], 'Iris_Vercicolor', inplace=True)
iris_df['Target'].replace([2], 'Iris_Virginica', inplace=True)

# print(iris_df)
iris_df_target = iris_df.loc[(iris_df['Target'] == 'Iris_Virginica'),
                             'Sepal_Length']
print(iris_df_target)
# Plotting the KDE Plot
sns.kdeplot(iris_df_target,
            color='b',
            fill=True)

# Setting the X and Y Label
plt.xlabel('Sepal Length')
plt.ylabel('Probability Density')
plt.show()
