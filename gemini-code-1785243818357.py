# src/engine/graph_engine.py
import networkx as nx

class MetaKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_card_node(self, card_id: str, name: str, node_type: str):
        """Node types: 'Leader', 'Character', 'Event', 'Stage'"""
        self.graph.add_node(card_id, name=name, type=node_type)

    def add_synergy(self, source_id: str, target_id: str, synergy_type: str, weight: float = 1.0):
        """
        Synergy Types: 
        - 'SYNERGIZES_WITH' (e.g., Engine cards in a Leader deck)
        - 'COUNTERS' (e.g., Removal options vs specific leaders)
        - 'PRICE_CORRELATED' (e.g., Tier 1 Staples)
        """
        self.graph.add_edge(source_id, target_id, relation=synergy_type, weight=weight)

    def get_card_synergies(self, card_id: str):
        """Retrieves all outgoing and incoming relationships for a given card."""
        if card_id not in self.graph:
            return []
        
        results = []
        # Outgoing edges
        for target in self.graph.successors(card_id):
            edge_data = self.graph.get_edge_data(card_id, target)
            target_name = self.graph.nodes[target].get("name", target)
            results.append((card_id, edge_data["relation"], f"{target_name} ({target})"))
            
        # Incoming edges
        for source in self.graph.predecessors(card_id):
            edge_data = self.graph.get_edge_data(source, card_id)
            source_name = self.graph.nodes[source].get("name", source)
            results.append((f"{source_name} ({source})", edge_data["relation"], card_id))

        return results

    def find_deck_engine(self, leader_id: str):
        """Extracts core engine components linked directly to a Leader."""
        synergies = []
        for target in self.graph.successors(leader_id):
            relation = self.graph.get_edge_data(leader_id, target)["relation"]
            if relation == "SYNERGIZES_WITH":
                synergies.append(target)
        return synergies