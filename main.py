from nodes.user_input_node import get_debate_topic
from dag.debate_dag import run_debate
from utils.dag_diagram import create_dag_diagram

if __name__ == "__main__":
    topic = get_debate_topic()
    create_dag_diagram()
    run_debate(topic)
