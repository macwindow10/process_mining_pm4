import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the XES event log
log = pd.read_csv('high_performers.csv')  # Replace with the path to your event log file

# Preprocess the event log (if necessary)
# Filter, transform, or enrich the log as per your requirements

# Extract the relevant information from the event log (e.g., activities, timestamps)
activities = log[
    'Activity'].unique()  # Replace 'activity_column_name' with the actual column name in your log that represents activities
timestamps = log[
    'timestamp'].values  # Replace 'timestamp_column_name' with the actual column name in your log that represents timestamps

# Calculate the fuzzy relations between activities based on timestamps
fuzzy_relation_matrix = np.zeros((len(activities), len(activities)))

for i in range(len(activities)):
    for j in range(len(activities)):
        if i != j:
            fuzzy_relation_matrix[i, j] = len(
                log[(log['Activity'] == activities[i]) & (log['Activity'].shift(-1) == activities[j])]) / len(
                log[log['Activity'] == activities[i]])

# Visualize the Directly-Follows Graph
fig, ax = plt.subplots()
ax.imshow(fuzzy_relation_matrix, cmap='Blues')

# Add labels to the activities
ax.set_xticks(np.arange(len(activities)))
ax.set_yticks(np.arange(len(activities)))
ax.set_xticklabels(activities)
ax.set_yticklabels(activities)

# Rotate the tick labels and set their alignment
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations
for i in range(len(activities)):
    for j in range(len(activities)):
        text = ax.text(j, i, fuzzy_relation_matrix[i, j],
                       ha="center", va="center", color="w")

plt.show()
