from spmf import Spmf
import pandas as pd
import pickle
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('total_students.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
timestamp = df.timestamp.unique()
userids = df.Case_id.unique()
# print(timestamp)
# print(df.timestamp.min())
# print(df.timestamp.max())
# print(len(timestamp))
# print(userids)
# print(len(userids))
# df.groupby(df["timestamp"].dt.day).count().plot(kind="bar")
# df.groupby([df["timestamp"].dt.month, df["timestamp"].dt.day]).count().plot(kind="bar")
# plt.show()
# for u in userids:
list = [223]
# print(u)
print(list)
# df.loc[df['ID'].isin(list_ID)]
mask = df['Case_id'].isin(list)
df_u = df.loc[mask]
print(len(df_u))
print(df_u.sort_values(by=['timestamp']))

# Different input formats (apart from file):
input_example_list = [
    [[1], [1, 2, 3], [1, 3], [4], [3, 6]],
    [[1, 4], [3], [2, 3], [1, 5]],
    [[5, 6], [1, 2], [4, 6], [3], [2]],
    [[5], [7], [1, 6], [3], [2], [3]]
]

"""
# Different algorithms:
spmf = Spmf("GSP", input_filename="contextPrefixSpan.txt",
            output_filename="output.txt",
            spmf_bin_location_dir="venv/Lib/site-packages/spmf/",
            arguments=[0.7, 1])
spmf.run()
# print(spmf.parse_output())
# print(spmf.to_pandas_dataframe(pickle=True))
spmf.to_csv("output.csv")
"""

spmf = Spmf("GSP", input_filename="contextGSP.txt",
            output_filename="output_gsp.txt",
            spmf_bin_location_dir="venv/Lib/site-packages/spmf/",
            arguments=[0.7, 1])
spmf.run()
spmf.to_csv("output_gsp.csv")
