import pandas as pd
import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.conformance.tokenreplay import algorithm as token_based_replay
from pm4py.algo.conformance.tokenreplay.diagnostics import duration_diagnostics

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

# Convert the DataFrame to an event log object in XES format
log = log_converter.apply(df_selected)

# Generating model using only a part of the log
net, initial_marking, final_marking = alpha_miner.apply(log)

#
# token base conformance
#
parameters_tbr = {
    token_based_replay.Variants.TOKEN_REPLAY.value.Parameters.DISABLE_VARIANTS: True,
    token_based_replay.Variants.TOKEN_REPLAY.value.Parameters.ENABLE_PLTR_FITNESS: True
}
replayed_traces, place_fitness, trans_fitness, unwanted_activities = \
    token_based_replay.apply(log, net, initial_marking,
                             final_marking,
                             parameters=parameters_tbr)
print('replayed_traces: ', replayed_traces)
print('place_fitness: ', place_fitness)
print('trans_fitness: ', trans_fitness)
print('unwanted_activities: ', unwanted_activities)

# Displaying Diagnostics Information
act_diagnostics = duration_diagnostics.diagnose_from_notexisting_activities(
    log, unwanted_activities)
for act in act_diagnostics:
    print(act, act_diagnostics[act])

trans_diagnostics = duration_diagnostics.diagnose_from_trans_fitness(
    log, trans_fitness)
for act in trans_diagnostics:
    print(act, trans_diagnostics[act])


#
# alignment base conformance
#
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, initial_marking, final_marking)
print(aligned_traces)

