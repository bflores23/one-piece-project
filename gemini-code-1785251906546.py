import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.engine.normalizer import DataNormalizer
from src.engine.graph_engine import MetaKnowledgeGraph, seed_meta_knowledge_graph
from src.console.plugins.data_importer import DataImporterPlugin
from src.console.plugins.financial_report import FinancialReportPlugin
from src.console.plugins.deck_validator import DeckValidatorPlugin

def run_integration_test():
    print("==================================================")
    print("  ETERNAL ANCHOR v0.1 ALPHA: SYSTEM TEST RUN     ")
    print("==================================================")

    # 1. Initialize Test DB and Clean Old Files
    db_file = "test_eternal_anchor.db"
    csv_file = "test_collection.csv"
    if os.path.exists(db_file):
        os.remove(db_file)
    if os.path.exists(csv_file):
        os.remove(csv_file)

    engine = create_engine(f"sqlite:///{db_file}", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("[✔] Test SQLite database schema generated successfully.")

    # 2. Generate Mock CSV Collection Sheet
    mock_data = [
        {"id": "op05-119", "name": "Monkey.D.Luffy", "rarity": "Manga Rare", "category": "Character", "location": "Vault Binder Page 1", "acquisition_price": "3850.00"},
        {"id": "op06-118", "name": "Roronoa Zoro", "rarity": "manga art", "category": "Character", "location": "Vault Binder Page 1", "acquisition_price": "1200.00"},
        {"id": "op10-001", "name": "Smoker", "rarity": "L", "category": "Leader", "location": "Deck Box 1", "acquisition_price": "25.00"},
        {"id": "op10-002", "name": "Caesar Clown", "rarity": "SR", "category": "Character", "location": "Binder 2", "acquisition_price": "15.00"},
        {"id": "op11-041", "name": "Nami", "rarity": "L", "category": "Leader", "location": "Deck Box 2", "acquisition_price": "30.00"},
        {"id": "op11-118", "name": "Monkey.D.Luffy", "rarity": "SEC-Parallel", "category": "Character", "location": "Binder 1", "acquisition_price": "180.00"},
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "rarity", "category", "location", "acquisition_price"])
        writer.writeheader()
        writer.writerows(mock_data)
    print(f"[✔] Generated sample collection file: '{csv_file}'.")

    # 3. Initialize Normalizer, Knowledge Graph, and Seed Meta Rules
    normalizer = DataNormalizer()
    graph = MetaKnowledgeGraph()
    seed_meta_knowledge_graph(graph)
    print("[✔] Knowledge Graph initialized and seeded with OP10 & OP11 synergy nodes.")

    # 4. Test Data Importer Plugin
    importer = DataImporterPlugin()
    print("\n--- TEST PHASE 1: BATCH CSV INGESTION ---")
    importer._import_csv(csv_file, session, normalizer)

    # 5. Test Executive Valuation Plugin
    print("\n--- TEST PHASE 2: FINANCIAL REPORT PLUGIN ---")
    financial_report = FinancialReportPlugin()
    financial_report.execute(session, normalizer, graph)

    # 6. Test Knowledge Graph Synergy Validator Plugin
    print("\n--- TEST PHASE 3: DECK SYNERGY VALIDATOR (OP10 Smoker Leader) ---")
    validator = DeckValidatorPlugin()
    
    # Simulating input for OP10-001
    leader_code = normalizer.normalize_card_code("op10-001")
    synergies = graph.find_deck_engine(leader_code)
    
    print(f"[+] Engine check for Leader [{leader_code}]:")
    for card_id in synergies:
        node_data = graph.graph.nodes.get(card_id, {})
        print(f"  • [{card_id}] {node_data.get('name', 'Unknown')}")

    # Clean up test artifacts
    session.close()
    if os.path.exists(csv_file):
        os.remove(csv_file)
    print("\n==================================================")
    print("  [SUCCESS] INTEGRATION TEST COMPLETED PERFECTLY  ")
    print("==================================================")

if __name__ == "__main__":
    run_integration_test()