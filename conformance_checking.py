import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.evaluation.replay_fitness.algorithm import token_replay as token_replay_evaluator
from pm4py.algo.evaluation.precision import algorithm as token_replay_precision
from pm4py.algo.evaluation.generalization import algorithm as token_replay_generalization
from pm4py.algo.evaluation.simplicity import algorithm as token_replay_simplicity

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('total_students.csv')
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
log = log_converter.apply(df_selected)
# print(log)

#
# Conformance Checking for Alpha
#
net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)
fitness_alpha = token_replay_evaluator.apply(log, net, initial_marking, final_marking)
precision_alpha = token_replay_precision.apply(log, net, initial_marking, final_marking)
f1score_alpha = 2 * (precision_alpha * fitness_alpha['log_fitness']) / (precision_alpha + fitness_alpha['log_fitness'])
generalization_alpha = token_replay_generalization.apply(log, net, initial_marking, final_marking)
simplicity_alpha = token_replay_simplicity.apply(net)
print('alpha miner accuracy: ', fitness_alpha['log_fitness'])
print('alpha miner precision: ', precision_alpha)
print('alpha miner f1score: ', f1score_alpha)
print('alpha miner generalization: ', generalization_alpha)
print('alpha miner simplicity: ', simplicity_alpha)
# fitness_alpha = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
# print(fitness_alpha)

#
# Conformance Checking for Inductive
#
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
# fitness_inductive = token_replay_evaluator.apply(log, net, initial_marking, final_marking)
# precision_inductive = token_replay_precision.apply(log, net, initial_marking, final_marking)
# f1score_inductive = 2 * (precision_inductive * fitness_inductive['log_fitness']) / (
#        precision_inductive + fitness_inductive['log_fitness'])
# generalization_inductive = token_replay_generalization.apply(log, net, initial_marking, final_marking)
# simplicity_inductive = token_replay_simplicity.apply(net)
# print('inductive miner accuracy: ', fitness_inductive['log_fitness'])
# print('inductive miner precision: ', precision_inductive)
# print('inductive miner f1score: ', f1score_inductive)
# print('inductive miner generalization: ', generalization_inductive)
# print('inductive miner simplicity: ', simplicity_inductive)
replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
print(replayed_traces)
print(replayed_traces.__len__())
for t in replayed_traces:
    print(t['trace_is_fit'])
# fitness_inductive = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
# print(fitness_inductive)
exit(1)

#
# Conformance Checking for Heuristic
#
net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log)
fitness_heuristics = token_replay_evaluator.apply(log, net, initial_marking, final_marking)
precision_heuristics = token_replay_precision.apply(log, net, initial_marking, final_marking)
f1score_heuristics = 2 * (precision_heuristics * fitness_heuristics['log_fitness']) / (
        precision_heuristics + fitness_heuristics['log_fitness'])
generalization_heuristics = token_replay_generalization.apply(log, net, initial_marking, final_marking)
simplicity_heuristics = token_replay_simplicity.apply(net)
print('heuristics miner accuracy: ', fitness_heuristics['log_fitness'])
print('heuristics miner precision: ', precision_heuristics)
print('heuristics miner f1score: ', f1score_heuristics)
print('heuristics miner generalization: ', generalization_heuristics)
print('heuristics miner simplicity: ', simplicity_heuristics)
# replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
# fitness_heuristics = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
# print(fitness_heuristics)

#
# Conformance Checking for ILP...
#
net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(log)
fitness_ilp = token_replay_evaluator.apply(log, net, initial_marking, final_marking)
precision_ilp = token_replay_precision.apply(log, net, initial_marking, final_marking)
f1score_ilp = 2 * (precision_ilp * fitness_ilp['log_fitness']) / (precision_ilp + fitness_ilp['log_fitness'])
generalization_ilp = token_replay_generalization.apply(log, net, initial_marking, final_marking)
simplicity_ilp = token_replay_simplicity.apply(net)
print('ilp miner accuracy: ', fitness_ilp['log_fitness'])
print('ilp miner precision: ', precision_ilp)
print('ilp miner f1score: ', f1score_ilp)
print('ilp miner generalization: ', generalization_ilp)
print('ilp miner simplicity: ', simplicity_ilp)
# replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
# fitness_ilp = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
# print(fitness_ilp)

#
# Conformance Checking for Directly Follows Graph...
#
'''
dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
print('dfg: ', dfg)
net, initial_marking, final_marking = pt_converter.apply(df)
fitness_dfg = token_replay_evaluator.apply(log, net, initial_marking, final_marking)
print('fitness_dfg: ', fitness_dfg)
'''

#
# plot accuracy
#
y1 = [
    fitness_alpha['log_fitness'],
    fitness_inductive['log_fitness'],
    fitness_heuristics['log_fitness'],
    fitness_ilp['log_fitness']
]
barWidth = 0.30
br1 = np.arange(len(y1))
fig = plt.subplots(figsize=(12, 8))
# keys_fitness_inductive = list(fitness_inductive.keys())
# values_fitness_inductive = list(fitness_inductive.values())
plt.bar(br1, y1, color='maroon', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("Accuracy", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
plt.savefig("Conformance Checking Accuracy.PNG", dpi=200, bbox_inches='tight')
plt.show()

#
# plot precision
#
y1 = [
    precision_alpha,
    precision_inductive,
    precision_heuristics,
    precision_ilp
]
barWidth = 0.30
br1 = np.arange(len(y1))
fig = plt.subplots(figsize=(12, 8))
plt.bar(br1, y1, color='blue', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("Precision", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
plt.savefig("Conformance Checking Precision.PNG", dpi=200, bbox_inches='tight')
plt.show()

#
# plot f1score
#
y1 = [
    f1score_alpha,
    f1score_inductive,
    f1score_heuristics,
    f1score_ilp
]
barWidth = 0.30
br1 = np.arange(len(y1))
fig = plt.subplots(figsize=(12, 8))
plt.bar(br1, y1, color='green', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("F1 Score", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
plt.savefig("Conformance Checking F1Score.PNG", dpi=200, bbox_inches='tight')
plt.show()

#
# plot generalization
#
y1 = [
    generalization_alpha,
    generalization_inductive,
    generalization_heuristics,
    generalization_ilp
]
barWidth = 0.30
br1 = np.arange(len(y1))
fig = plt.subplots(figsize=(12, 8))
plt.bar(br1, y1, color='red', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("Generalization", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
plt.savefig("Conformance Checking Generalization.PNG", dpi=200, bbox_inches='tight')
plt.show()

#
# plot simplicity
#
y1 = [
    simplicity_alpha,
    simplicity_inductive,
    simplicity_heuristics,
    simplicity_ilp
]
barWidth = 0.30
br1 = np.arange(len(y1))
fig = plt.subplots(figsize=(12, 8))
plt.bar(br1, y1, color='black', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("Simplicity", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
plt.savefig("Conformance Checking Simplicity.PNG", dpi=200, bbox_inches='tight')
plt.show()

#
# plot summary table
#
row_headers = ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner']
column_headers = ['Accuracy', 'Precision', 'F1 Score', 'Generalization', 'Simplicity']
cell_values = [
    [fitness_alpha['log_fitness'], precision_alpha, f1score_alpha, generalization_alpha, simplicity_alpha],
    [fitness_inductive['log_fitness'], precision_inductive, f1score_inductive, generalization_inductive,
     simplicity_inductive],
    [fitness_heuristics['log_fitness'], precision_heuristics, f1score_heuristics, generalization_heuristics,
     simplicity_heuristics],
    [fitness_ilp['log_fitness'], precision_ilp, f1score_ilp, generalization_ilp, simplicity_ilp]
]
# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(10, 2 + 6 / 2.5))
ax.set_axis_off()
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
table = ax.table(
    cellText=cell_values,
    rowLabels=row_headers,
    colLabels=column_headers,
    rowColours=rcolors,
    colColours=ccolors,
    cellLoc='center',
    rowLoc='right',
    loc='center')
table.scale(1, 2)
table.set_fontsize(16)
ax.set_title('Conformance Checking \n Comparison of Process Discovery Models',
             fontsize=18,
             fontweight="bold")
plt.tight_layout()
plt.savefig("Summary Table.png", dpi=200, bbox_inches='tight')
plt.show()
