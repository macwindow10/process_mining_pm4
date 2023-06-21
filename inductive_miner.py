import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('high_performers.csv')

selected_columns = ['Case_id', 'Activity', 'timestamp']
df_selected = df[selected_columns]
df_selected = df_selected.rename(columns={
    'Case_id': 'case:concept:name',
    'Activity': 'concept:name',
    'timestamp': 'time:timestamp'
})

# Convert the DataFrame to an event log object in XES format
log = log_converter.apply(df_selected)

# untill here all we do is get data from csv ... will be same for all
# under that we will apply alogorithm we want to apply and visualize it according to algo
# Apply the Alpha Miner algorithm to obtain the process model (process tree)
process_tree = inductive_miner.apply(log)

# Visualize the process model
gviz = pt_visualizer.apply(process_tree)
pt_visualizer.view(gviz)
