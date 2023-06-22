import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pm4py
from pm4py.objects.conversion.log import converter as log_converter

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


net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
fitness_inductive = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
print(fitness_inductive)

net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)
replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
fitness_alpha = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
print(fitness_alpha)

net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log)
replayed_traces = pm4py.conformance_diagnostics_token_based_replay(log, net, initial_marking, final_marking)
# print(replayed_traces)
fitness_heuristics = pm4py.fitness_token_based_replay(log, net, initial_marking, final_marking)
print(fitness_heuristics)

y1 = [
    fitness_inductive['average_trace_fitness'],
    fitness_inductive['log_fitness']]
y2 = [
    fitness_alpha['average_trace_fitness'],
    fitness_alpha['log_fitness']]
y3 = [
    fitness_heuristics['average_trace_fitness'],
    fitness_heuristics['log_fitness']]
barWidth = 0.30
br1 = np.arange(len(y1))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

fig = plt.subplots(figsize=(12, 8))

# keys_fitness_inductive = list(fitness_inductive.keys())
# values_fitness_inductive = list(fitness_inductive.values())
plt.bar(br1, y1, color='maroon', width=barWidth)
plt.bar(br2, y2, color='green', width=barWidth)
plt.bar(br3, y3, color='blue', width=barWidth)

plt.xlabel("Process Discovery Models")
plt.ylabel("Conformance Matrics")
plt.title("Comparison of Process Discovery Models")
plt.xticks([r + barWidth for r in range(len(y1))],
           ['Average Trace Fitness', 'Log Fitness'])
plt.legend()
plt.show()
