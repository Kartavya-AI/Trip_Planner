from langgraph.graph import StateGraph, END
from nodes import intent_mapper_node, finder_node, itinerary_node

graph = StateGraph(dict)

# Nodes
graph.add_node("intent_mapper", intent_mapper_node)
graph.add_node("finder", finder_node)
graph.add_node("itinerary", itinerary_node)

#Edges
graph.set_entry_point("intent_mapper")
graph.add_edge("intent_mapper", "finder")
graph.add_edge("finder", "itinerary")
graph.add_edge("itinerary", END)

app = graph.compile()
