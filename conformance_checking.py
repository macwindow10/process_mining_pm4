import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.evaluation.replay_fitness.algorithm import token_replay as token_replay_evaluator
from pm4py.algo.evaluation.precision import algorithm as token_replay_precision
from pm4py.algo.evaluation.generalization import algorithm as token_replay_generalization
from pm4py.algo.evaluation.simplicity import algorithm as token_replay_simplicity

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
log = log_converter.apply(df_selected)
# print(log)

#
# plot summary table
#
row_headers = ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner']
column_headers = ['Accuracy', 'Precision', 'F1 Score', 'Generalization', 'Simplicity']
val3 = [
    [1, 0.7, 0.5, 0.75, 0.30],
    [0.9, 0.5, 0.8, 0.65, 1.0],
    [0.78, 0.8, 0.9, 0.8, 0.80],
    [0.6, 0.3, 0.9, 0.5, 0.90]
]
fig, ax = plt.subplots()
fig_background_color = 'skyblue'
fig_border = 'steelblue'
plt.figure(linewidth=2,
           edgecolor=fig_border,
           facecolor=fig_background_color)
ax.set_axis_off()
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
table = ax.table(
    cellText=val3,
    rowLabels=row_headers,
    colLabels=column_headers,
    rowColours=rcolors,
    colColours=ccolors,
    cellLoc='center',
    rowLoc='right',
    loc='center')
ax.set_title('matplotlib.axes.Axes.table() function Example',
             fontweight="bold")
'''
plt.savefig('pyplot-table-figure-style.png',
            bbox_inches='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150)
            '''
plt.show()

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
# replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
# fitness_alpha = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
# print(fitness_alpha)

#
# Conformance Checking for Inductive
#
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
fitness_inductive = token_replay_evaluator.apply(log, net, initial_marking, final_marking)
precision_inductive = token_replay_precision.apply(log, net, initial_marking, final_marking)
f1score_inductive = 2 * (precision_inductive * fitness_inductive['log_fitness']) / (
        precision_inductive + fitness_inductive['log_fitness'])
generalization_inductive = token_replay_generalization.apply(log, net, initial_marking, final_marking)
simplicity_inductive = token_replay_simplicity.apply(net)
print('inductive miner accuracy: ', fitness_inductive['log_fitness'])
print('inductive miner precision: ', precision_inductive)
print('inductive miner f1score: ', f1score_inductive)
print('inductive miner generalization: ', generalization_inductive)
print('inductive miner simplicity: ', simplicity_inductive)
# replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
# fitness_inductive = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
# print(fitness_inductive)

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
# Conformance Checking for Directly Follows Graph...
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
plt.bar(br1, y1, color='blue', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("F1 Score", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
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
plt.bar(br1, y1, color='green', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("Generalization", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
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
plt.bar(br1, y1, color='green', width=barWidth)
plt.xlabel("Process Discovery Models", fontsize=18)
plt.ylabel("Simplicity", fontsize=18)
plt.title("Conformance Checking of Process Discovery Models",
          fontdict={'fontsize': 18})
plt.xticks([r for r in range(len(y1))],
           ['Alpha Miner', 'Inductive Miner', 'Heuristic Miner', 'ILP Miner'])
xlocs, xlabs = plt.xticks()
for i, v in enumerate(y1):
    plt.text(xlocs[i] - 0.05, v + 0.01, str(round(v, 2)))
plt.show()
