import os
from spmf import Spmf
from gsppy.gsp import GSP
import pandas as pd
import pickle
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)


def create_sequences_file_for_spmf(df_u):
    sequences = []
    sequence = ''
    if os.path.exists('contextGSP_2.txt'):
        append_write = 'a'
    else:
        append_write = 'w'
    f = open('contextGSP_2.txt', append_write)

    if os.path.exists('contextGSP_2_user_mapping.txt'):
        append_write = 'a'
    else:
        append_write = 'w'
    file_context_gsp_user_mapping = open('contextGSP_2_user_mapping.txt', append_write)

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
            sequence = sequence + '2 -1 '
        elif r['Activity'] == 'c':
            sequence = sequence + '3 '
        elif r['Activity'] == 'd':
            if previous_activity == 'c':
                sequence = sequence + '4 '
            else:
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
            file_context_gsp_user_mapping.write(str(r['Case_id']) + ': ' + sequence + '\n')
            sequence = ''

        previous_activity = r['Activity']

    f.close()
    file_context_gsp_user_mapping.close()


def generate_sequences_for_gsppy(df_u, sequences):
    sequence = []
    for index, r in df_u.iterrows():
        if r['Activity'] == 'a':
            sequence.append('user_login')
        elif r['Activity'] == 'b':
            sequence.append('view_lectures')
        elif r['Activity'] == 'c':
            sequence.append('watch_video_lecture')
        elif r['Activity'] == 'd':
            sequence.append('download_handouts')
        elif r['Activity'] == 'e':
            sequence.append('attempt_Quiz')
        elif r['Activity'] == 'f':
            sequence.append('view_Quiz_List')
        elif r['Activity'] == 'g':
            sequence.append('view_progress')
        elif r['Activity'] == 'h':
            sequence.append('view_assignment')
        elif r['Activity'] == 'i':
            sequence.append('view_announcements')
        elif r['Activity'] == 'j':
            sequence.append('user_logout')
            sequences.append(sequence)
            # print(sequence)
            sequence = []
    # print(sequences)


def main():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('total_students.csv')
    selected_columns = ['Case_id', 'Activity', 'timestamp', 'Grades']
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

    if os.path.exists('contextGSP_2.txt'):
        os.remove('contextGSP_2.txt')
    if os.path.exists('contextGSP_2_user_mapping.txt'):
        os.remove('contextGSP_2_user_mapping.txt')
    if os.path.exists('userIDs.txt'):
        os.remove('userIDs.txt')

    file_user_ids = open('userIDs.txt', "w")
    file_user_ids.write('Id' + ', ' + 'Grades' + '\n')
    records_processes = 1
    sequences_for_gsppy = []
    for u in userids:
        list = [u]
        # print(u)
        # print('user id: ', list)

        mask = df['Case_id'].isin(list)
        df_u = df.loc[mask]
        df_u = df_u.sort_values(by=['timestamp'])
        # print('records count: ', len(df_u))
        records_processes = records_processes + len(df_u)
        # print(df_u)

        create_sequences_file_for_spmf(df_u)
        generate_sequences_for_gsppy(df_u, sequences_for_gsppy)

        file_user_ids.write(
            str(df_u.iloc[0]['Case_id']) + ', ' +
            str(df_u.iloc[0]['Grades']) + '\n')

    file_user_ids.close()
    print('records_processes: ', records_processes)
    # print(len(sequences_for_gsppy))

    """
    # Spmf GSP algorithms:
    spmf = Spmf("GSP", input_filename="contextPrefixSpan.txt",
                output_filename="output.txt",
                spmf_bin_location_dir="venv/Lib/site-packages/spmf/",
                arguments=[0.7, 1])
    spmf.run()
    # print(spmf.parse_output())
    # print(spmf.to_pandas_dataframe(pickle=True))
    spmf.to_csv("output.csv")
    """

    """
    spmf = Spmf("GSP", input_filename="contextGSP_2.txt",
                output_filename="output_spmfgsp.txt",
                spmf_bin_location_dir="venv/Lib/site-packages/spmf/",
                arguments=[0.5, 1])
    spmf.run()
    """

    # process SPMF GSP output file
    file_output_spmfgsp = open("output_spmfgsp.txt", "r")
    lines = file_output_spmfgsp.readlines()
    count = 0
    support = ""
    sids = []
    for line in lines:
        count += 1
        if line.__contains__("watch_video_lecture download_handout attemp_quiz"):
            line_items = line.split()
            for i in range(len(line_items)):
                if line_items[i] == '#SUP:':
                    support = line_items[i + 1]
                elif line_items[i] == '#SID:':
                    sids = line_items[(i + 1):]
                    # print('sids: ', sids)
                    # print('sids len: ', len(sids))
            break
    file_output_spmfgsp.close()

    file_context_gsp_user_mapping = open('contextGSP_2_user_mapping.txt', "r")
    user_mapping_lines = file_context_gsp_user_mapping.readlines()
    userids_c_d_e = []
    for sid in sids:
        # print('sid: ', sid)
        sid_index = int(sid)
        user_id = user_mapping_lines[sid_index].split(':')[0]
        # print('user_id: ', user_id)
        userids_c_d_e.append(int(user_id))

    file_context_gsp_user_mapping.close()

    print('userids_c_d_e count: ', len(userids_c_d_e))
    print('userids_c_d_e: ', userids_c_d_e)

    df_final_grades = pd.read_csv('final_grades.csv')
    mask = df_final_grades['User_id'].isin(userids_c_d_e)

    df_final_grades_cde = df_final_grades.loc[mask]
    df_final_grades_cde['cluster'] = 1  # 'Students who followed desired activities'
    # print('df_final_grades_cde count: ', len(df_final_grades_cde))

    df_final_grades_rest = df_final_grades.loc[~mask]
    df_final_grades_rest['cluster'] = 2  # 'Students who performed random activities'
    # print('df_final_grades_rest count: ', len(df_final_grades_rest))

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    df_final_grades_cde.plot(x="User_id", y=["Grades"],
                             kind="bar",
                             color='blue',
                             ax=ax[0])
    ax[0].set_xlabel("Student Id")
    ax[0].set_ylabel("Student Grades")
    df_final_grades_rest.plot(x="User_id", y=["Grades"],
                              kind="bar",
                              color='black',
                              ax=ax[1])
    ax[1].set_xlabel("Student Id")
    ax[1].set_ylabel("Student Grades")
    plt.show()

    frames = [df_final_grades_cde, df_final_grades_rest]
    result = pd.concat(frames)
    # result.groupby('cluster')['Grades'].plot(kind='hist')
    fig, ax = plt.subplots()
    ax.bar(result.cluster, result["Grades"])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(
        "Cluster 1: Student who performed desired activities \nCluster 2: Student who performed random activities")
    ax.set_ylabel("Student Grades")
    fig.tight_layout()
    plt.show()

    # gsp-py
    # gsp_py = GSP(sequences_for_gsppy)
    # result = gsp_py.search(0.5)
    # print(result)
    print('program ends')


if __name__ == "__main__":
    main()
