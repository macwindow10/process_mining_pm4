import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from PIL import Image

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('high_performers.csv')

# Rename the column names according to XES format
df = df.rename(columns={
    'Case_id': 'case:concept:name',
    'Case': 'concept:name',
    'timestamp': 'time:timestamp',
    'Activity': 'concept:name',
    'Grades': 'Grade'
})

# Convert the DataFrame to an event log object in XES format
log = log_converter.apply(df)

# Apply the Heuristic Miner algorithm to obtain the Heuristics net
heu_net = heuristics_miner.apply_heu(log)

# Visualize the Heuristics net
gviz = hn_visualizer.apply(heu_net)

# Save the Heuristics net visualization as a PNG file
hn_visualizer.save(gviz, "heuristics_net.png")

# Display the Heuristics net visualization
Image.open("heuristics_net.png").show()
