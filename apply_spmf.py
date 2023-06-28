import os
from spmf import Spmf
import pandas as pd
import pickle
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)


def create_sequence_file(df_u):
    sequences = []
    sequence = ''
    if os.path.exists('contextGSP_2.txt'):
        append_write = 'a'
    else:
        append_write = 'w'
    f = open('contextGSP_2.txt', append_write)
    if append_write == 'w':
        f.write("""@CONVERTED_FROM_TEXT
@ITEM=1=user_login
@ITEM=2=view_lecture
@ITEM=3=watch_video_lecture
@ITEM=4=download_handout
@ITEM=5=attemp_quiz
@ITEM=6=view_quiz_list
@ITEM=7=view_progress
@ITEM=8=view_assignment
@ITEM=9=view_announcement
@ITEM=10=user_logout
@ITEM=-1=|
""")
    previous_activity = ''
    for index, r in df_u.iterrows():
        if r['Activity'] == 'a':
            sequence = '1 -1 '
        elif r['Activity'] == 'b':
            sequence = sequence + '2 '
        elif r['Activity'] == 'c':
            if previous_activity == 'b':
                sequence = sequence + '3 '
            else:
                sequence = sequence + '3 -1 '
        elif r['Activity'] == 'd':
            sequence = sequence + '4 -1 '
        elif r['Activity'] == 'e':
            sequence = sequence + '5 -1 '
        elif r['Activity'] == 'f':
            sequence = sequence + '6 -1 '
        elif r['Activity'] == 'g':
            sequence = sequence + '7 -1 '
        elif r['Activity'] == 'h':
            sequence = sequence + '8 -1 '
        elif r['Activity'] == 'i':
            sequence = sequence + '9 -1 '
        elif r['Activity'] == 'j':
            sequence = sequence + '10 -1 -2'
            sequences.append(sequence)
            f.write(sequence + '\n')
            sequence = ''

        previous_activity = r['Activity']

    f.close()


# Load the CSV file into a pandas DataFrame
df = pd.read_csv('total_students.csv')
selected_columns = ['Case_id', 'Activity', 'timestamp']
df = df[selected_columns]
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
for u in userids:
    list = [u]
    print(u)
    print(list)
    mask = df['Case_id'].isin(list)
    df_u = df.loc[mask]
    df_u = df_u.sort_values(by=['timestamp'])
    print(len(df_u))
    print(df_u)
    create_sequence_file(df_u)

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

spmf = Spmf("GSP", input_filename="contextGSP_2.txt",
            output_filename="output_gsp.txt",
            spmf_bin_location_dir="venv/Lib/site-packages/spmf/",
            arguments=[0.5, 1])
spmf.run()
