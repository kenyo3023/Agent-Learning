from dataclasses import dataclass, field
from typing import TypedDict
from langgraph.graph import StateGraph, END


# **State**
@dataclass
class StateForRetrieval():#TypedDict):
    content:str
    _dict:dict = field(default_factory=lambda:{})

# **State**
@dataclass
class StateForCompletion():#TypedDict):
    prompt:str
    sampling_params:dict = field(default_factory=lambda:{})

# **State**
class State(TypedDict):
    state:list

# **Node**
class Retrieval():
    name = 'retrieval'

    def __init__(self, _dict:dict={}, name:str=None):
        self._dict = _dict
        self.name = name or self.name

    def __call__(self, state: State):
        print(f"Execute node for retrieval")
        curr_state = StateForRetrieval(**state['state'][-1])
        print(f'curr_state: {curr_state}')

        latest_state = {'prompt':'how dare you?'}
        state['state'].append(latest_state)
        return state

# **Node**
class Completion():
    name = 'completion'

    def __init__(self, sampling_params:dict={}, name:str=None):
        self.sampling_params = sampling_params
        self.name = name or self.name

    def __call__(self, state: State):
        print(f"Execute node for completion")
        curr_state = StateForCompletion(**state['state'][-1])
        print(f'curr_state: {curr_state}')

        latest_state = {'completion':'fuck you'}
        state['state'].append(latest_state)
        return state

# **Edge**
def is_valid_response(state: State):
    curr_state = StateForCompletion(**state['state'][-1])

    if 'stop' in curr_state.prompt:
        return END
    else:
        return 'completion'


# The Graph!  The "Program" !!
workflow = StateGraph(State)

node_for__retrieval = Retrieval()
workflow.add_node(node_for__retrieval.name, node_for__retrieval)

node_for_completion = Completion()
workflow.add_node(node_for_completion.name, node_for_completion)

workflow.set_entry_point(node_for__retrieval.name)
workflow.add_edge(node_for__retrieval.name, node_for_completion.name)
# workflow.add_conditional_edges(
#     source=node_for_completion.name, path=is_valid_response
# )

# Compile, and then run
graph = workflow.compile()
r = graph.invoke({'state':[{'content':'HI'},]})
print(r)