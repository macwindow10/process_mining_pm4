import pandas as pd
from sklearn.cluster import KMeans

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# students_activity = pd.read_csv('students_activity.csv')
students_activity = pd.read_csv('students_activity2023-02-20.csv')
print(students_activity.head(10))

final_grades = pd.read_csv('final_grades.csv')
print(final_grades.head(10))

# Step 2: Replace log events
students_activity['Actions'] = students_activity['Actions'].replace({
    '.viewed lecture link https://www.youtube.com/watch?v=vO7QXLTSE4I.': 'watch video lecture',
    '.viewed lecture link https://www.youtube.com/watch?v=3kL1Cof-WAs.': 'watch video lecture',
    '.viewed lecture link https://www.youtube.com/watch?v=OMuTdETbsDw.': 'watch video lecture',
    '.viewed lecture link https://www.youtube.com/watch?v=A1JMbBDfhYU.': 'watch video lecture',
    '.viewed lecture link https://www.youtube.com/watch?v=rFeMWWFFkfs.': 'watch video lecture',
    '.viewed lecture link https://www.youtube.com/watch?v=jg933uLFTCM.': 'watch video lecture',
    '.downloaded lecture file Lecture 1.': 'download handouts',
    '.downloaded lecture file Lecture 2.': 'download handouts',
    '.downloaded lecture file Lecture 3.': 'download handouts',
    '.downloaded lecture file Lecture 4.': 'download handouts',
    '.downloaded lecture file Lecture 5.': 'download handouts',
    '.downloaded lecture file Lecture 6.': 'download handouts'
})
print(students_activity.head(10))

# Step 3: Rename attribute names
students_activity = students_activity.rename(
    columns={'User_id': 'Case_id', 'Username': 'Case', 'Actions': 'Activity', 'Date': 'timestamp'})
final_grades = final_grades.rename(columns={'User_id': 'Case_id'})

# Step 4: Replace log events
students_activity['Activity'] = students_activity['Activity'].replace({
    'user Loged in': 'a',
    'view lectures': 'b',
    'watch video lecture': 'c',
    'download handouts': 'd',
    'attempt Quiz': 'e',
    'view Quiz List': 'f',
    'view progress': 'g',
    'view assignment': 'h',
    'view announcements': 'i',
    'user logged out': 'j',
})

# Step 5: Filter out specified events
students_activity = students_activity[~students_activity['Activity'].isin(
    ['view notifications', 'view CLOs', 'view messages', 'view events', 'view students list',
     '.viewed lecture link https://www.youtube.com/watch?v=8cABrN3Dqcg.',
     '.viewed lecture link https://www.youtube.com/watch?v=O5Mh1e4xq0Y.'])]

# Step 6: Merge with final_grades on Case_id
merged_data = pd.merge(students_activity, final_grades, on='Case_id', how='left')

# Step 7: Drop rows with missing grades
merged_data = merged_data.dropna(subset=['Grades'])

# Step 8: Perform k-means clustering on grades
Grades = merged_data['Grades'].values.reshape(-1, 1)
kmeans = KMeans(n_clusters=2, random_state=0).fit(Grades)
cluster_labels = kmeans.labels_

# Step 9: Add cluster labels to merged data
merged_data['Cluster'] = cluster_labels

# Step 10: Create separate dataframes for high performers and low performers
high_performers = merged_data[merged_data['Grades'] > 60]
low_performers = merged_data[merged_data['Grades'] <= 60]

# Step 11: Export data to CSV files
high_performers.to_csv('high_performers.csv', index=False)
low_performers.to_csv('low_performers.csv', index=False)
merged_data.to_csv('total_students.csv', index=False)
print('high_performers, low_performers, and total_students generated')