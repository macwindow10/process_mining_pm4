import pandas as pd
import pm4py
from sklearn.cluster import KMeans
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.visualization.process_tree import visualizer as pt_visualizer

from pm4py.objects.conversion.process_tree import converter as pt_converter

from PIL import Image

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('high_performers.csv')
selected_columns = ['Case_id', 'Activity', 'timestamp', 'Case']
df_selected = df[selected_columns]
df_selected = df_selected.rename(columns={
    'Case_id': 'case:concept:name',
    'Activity': 'concept:name',
    'timestamp': 'time:timestamp',
    'Case': 'org:resource'
})
df_selected['time:timestamp'] = pd.to_datetime(df_selected['time:timestamp'])
print(df_selected.dtypes)
# print(df_selected)
# df_selected = df_selected.sort_values(by=['case:concept:name', 'time:timestamp'])
# print(df_selected)

log = log_converter.apply(df_selected)
# print(log)

#
# ALPHA Miner
#
alpha_net, initial_marking, final_marking = alpha_miner.apply(log)
gviz = pn_visualizer.apply(alpha_net, initial_marking, final_marking)
pn_visualizer.view(gviz)
# pn_visualizer.save(gviz, "alpha_miner.png")

parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
gviz = pn_visualizer.apply(alpha_net, initial_marking, final_marking,
                           parameters=parameters,
                           variant=pn_visualizer.Variants.FREQUENCY, log=log)
pn_visualizer.view(gviz)
# save the Petri net
# pn_visualizer.save(gviz, "alpha_miner_petri_net.png")

# Create graph from log
dfg = dfg_discovery.apply(log)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
dfg_visualization.view(gviz)
# dfg_visualization.save(gviz, "alpha_miner_dfg.png", parameters=parameters)

# creatig the graph from log
dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
dfg_visualization.view(gviz)

#
# HEURISTIC Miner
#
heu_net = heuristics_miner.apply_heu(log)
gviz = hn_visualizer.apply(heu_net)
hn_visualizer.view(gviz)
hn_visualizer.save(gviz, 'heuristic_miner.png')

# Petri-net of heuristic miner output
net, im, fm = heuristics_miner.apply(log)
gviz = pn_visualizer.apply(net, im, fm)
gviz = pn_visualizer.apply(net, im, fm,
                           parameters=parameters,
                           variant=pn_visualizer.Variants.FREQUENCY,
                           log=log)
pn_visualizer.view(gviz)
# pn_visualizer.save(gviz, 'heuristic_miner_petri_net.png')

#
# INDUCTIVE Miner
#
# create the process tree
tree = inductive_miner.apply(log)
gviz = pt_visualizer.apply(tree)
pt_visualizer.view(gviz)
# pt_visualizer.save(gviz, 'inductive_miner.png')
bpmn_model = pm4py.convert_to_bpmn(tree)
pm4py.view_bpmn(bpmn_model)

# convert the process tree to a petri net
net, initial_marking, final_marking = pt_converter.apply(tree)
# alternatively, use the inductive_miner to create a petri net from scratch
# net, initial_marking, final_marking = inductive_miner.apply(log)
parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
gviz = pn_visualizer.apply(net, initial_marking, final_marking,
                           parameters=parameters,
                           variant=pn_visualizer.Variants.FREQUENCY,
                           log=log)
pn_visualizer.view(gviz)
# pn_visualizer.save(gviz, "inductive_miner_petri_net.png")

from pm4py.objects.petri_net.utils import performance_map

traces = performance_map.get_transition_performance_with_token_replay(log, net, initial_marking, final_marking)
print(traces)
# traces_for_event_a = traces['a']['all_values']
# print(traces_for_event_a)

from pm4py.visualization.sna import visualizer as sna_vis
from pm4py.algo.organizational_mining.sna import algorithm as sna_factory
from pyvis import network as net

handover_nw = sna_factory.log_handover.apply(log)
# print(handover_nw)
gviz_hw_py = sna_vis.apply(handover_nw)
gnx = sna_vis.view(gviz_hw_py)
