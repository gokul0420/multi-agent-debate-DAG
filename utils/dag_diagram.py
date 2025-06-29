from graphviz import Digraph

def create_dag_diagram():
    dot = Digraph(comment='LangGraph Debate DAG')
    nodes = ["UserInput", "AgentA", "AgentB", "Memory", "Judge"]
    for node in nodes:
        dot.node(node)
    dot.edges([("UserInput", "AgentA"), ("AgentA", "Memory"), ("Memory", "AgentB"),
               ("AgentB", "Memory"), ("Memory", "Judge")])
    dot.render('dag_diagram', format='png', cleanup=True)
