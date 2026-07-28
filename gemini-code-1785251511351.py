# src/engine/graph_engine.py (Excerpt - Archetype Seeding)

def seed_meta_knowledge_graph(graph: MetaKnowledgeGraph):
    # OP10 - Punk Hazard / Royal Blood Archetype
    graph.add_card_node("OP10-001", "Smoker", "Leader")
    graph.add_card_node("OP10-002", "Caesar Clown", "Character")
    graph.add_card_node("OP10-003", "Sugar", "Character")
    graph.add_card_node("OP10-004", "Vergo", "Character")
    
    # OP11 - Navy / Whole Cake Island Archetype
    graph.add_card_node("OP11-041", "Nami", "Leader")
    graph.add_card_node("OP11-118", "Monkey.D.Luffy", "Character")
    graph.add_card_node("OP11-119", "Koby", "Character")
    
    # Define Archetype Synergies
    graph.add_synergy("OP10-001", "OP10-002", "SYNERGIZES_WITH")
    graph.add_synergy("OP10-001", "OP10-003", "SYNERGIZES_WITH")
    graph.add_synergy("OP10-001", "OP10-004", "SYNERGIZES_WITH")
    
    graph.add_synergy("OP11-041", "OP11-118", "SYNERGIZES_WITH")
    graph.add_synergy("OP11-119", "OP10-001", "PRICE_CORRELATED") # Shared Navy archetype interest

    return graph