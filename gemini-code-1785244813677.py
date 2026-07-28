# main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Card, InventoryItem
from src.engine.normalizer import DataNormalizer
from src.engine.graph_engine import MetaKnowledgeGraph

# Import Plugins
from src.console.plugins.deck_validator import DeckValidatorPlugin
from src.console.plugins.financial_report import FinancialReportPlugin

def initialize_system():
    engine = create_engine("sqlite:///eternal_anchor.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    normalizer = DataNormalizer()
    graph = MetaKnowledgeGraph()

    # Seed Graph Relationships
    graph.add_card_node("OP09-001", "Shanks", "Leader")
    graph.add_card_node("OP09-009", "Benn.Beckman", "Character")
    graph.add_card_node("OP08-118", "Silvers Rayleigh", "Character")
    
    graph.add_synergy("OP09-001", "OP09-009", "SYNERGIZES_WITH")
    graph.add_synergy("OP09-001", "OP08-118", "SYNERGIZES_WITH")

    return session, normalizer, graph

def main():
    session, normalizer, graph = initialize_system()

    # Register Active Plugins
    plugins = [
        DeckValidatorPlugin(),
        FinancialReportPlugin()
    ]

    while True:
        print("\n==================================================")
        print("  CAPTAIN'S CONSOLE v0.1 ALPHA (PLUGIN DRIVEN)  ")
        print("==================================================")
        
        for idx, plugin in enumerate(plugins, 1):
            print(f"{idx}. {plugin.name} - {plugin.description}")
        print(f"{len(plugins) + 1}. Exit")

        choice = input(f"\nSelect command (1-{len(plugins) + 1}): ").strip()

        if choice.isdigit():
            opt = int(choice)
            if 1 <= opt <= len(plugins):
                plugins[opt - 1].execute(session, normalizer, graph)
            elif opt == len(plugins) + 1:
                print("\nTerminating Captain's Console session. Anchor secured!")
                break
            else:
                print("Option out of range.")
        else:
            print("Invalid input. Enter a number.")

if __name__ == "__main__":
    main()