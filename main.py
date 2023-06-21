import pandas as pd
from sklearn.cluster import KMeans
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization
from PIL import Image

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('high_performers.csv')
selected_columns = ['Case_id', 'Activity', 'timestamp', 'Grades']
df_selected = df[selected_columns]
df_selected = df_selected.rename(columns={
    'Case_id': 'case:concept:name',
    'Activity': 'concept:name',
    'timestamp': 'time:timestamp',
    'Grades': 'org:resource'
})
df_selected['time:timestamp'] = pd.to_datetime(df_selected['time:timestamp'])
print(df_selected.dtypes)
print(df_selected)
# df_selected = df_selected.sort_values(by=['case:concept:name', 'time:timestamp'])
# print(df_selected)

log = log_converter.apply(df_selected)
print(log)

# ALPHA
alpha_net, initial_marking, final_marking = alpha_miner.apply(log)
gviz = pn_visualizer.apply(alpha_net, initial_marking, final_marking)
pn_visualizer.view(gviz)
# save
pn_visualizer.save(gviz, "alpha_miner.png")

parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
gviz = pn_visualizer.apply(alpha_net, initial_marking, final_marking,
                           parameters=parameters,
                           variant=pn_visualizer.Variants.FREQUENCY, log=log)
pn_visualizer.view(gviz)
# save the Petri net
pn_visualizer.save(gviz, "alpha_miner_petri_net.png")

# Create graph from log
dfg = dfg_discovery.apply(log)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
dfg_visualization.view(gviz)
# dfg_visualization.save(gviz, "alpha_miner_dfg.png", parameters=parameters)

# creatig the graph from log
dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
dfg_visualization.view(gviz)
