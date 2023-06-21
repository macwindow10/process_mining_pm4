import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from PIL import Image

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('high_performers.csv')

selected_columns = ['Case_id', 'Activity', 'timestamp']
df_selected = df[selected_columns]
df_selected = df_selected.rename(columns={
    'Case_id': 'case:concept:name',
    'Activity': 'concept:name',
    'timestamp': 'time:timestamp'

})
df = df.rename(columns={
    'Case_id': 'case:concept:name',
    'Case': 'concept:name_1',
    'timestamp': 'time:timestamp',
    'Activity': 'concept:name',
    'Grades': 'Grade'
})
# Sort the DataFrame by case ID and timestamp
# df_selected = df_selected.sort_values(by=['case:concept:name', 'time:timestamp'])


# Rename the column names according to XES format


# Convert the DataFrame to an event log object in XES format
log = log_converter.apply(df_selected)

# log = log_converter.apply(df)

# Apply the Alpha Miner algorithm to obtain the Petri net
net, initial_marking, final_marking = alpha_miner.apply(log)

# add information about frequency to the viz
parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}

# Visualize the Petri net
gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters,
                           variant=pn_visualizer.Variants.FREQUENCY,
                           log=log)

# Save the Petri net visualization as a PNG file
pn_visualizer.save(gviz, "petri_net.png")
pn_visualizer.view(gviz)

# Display the Petri net visualization
Image.open("petri_net.png").show()
