# src/console/plugins/deck_validator.py
from src.console.plugins.base import ConsolePlugin

class DeckValidatorPlugin(ConsolePlugin):
    @property
    def name(self) -> str:
        return "Deck Synergy & Meta Validator"

    @property
    def description(self) -> str:
        return "Analyzes a Leader deck composition against Knowledge Graph synergy nodes."

    def execute(self, session, normalizer, graph) -> None:
        print("\n=== DECK SYNERGY VALIDATOR ===")
        leader_code = normalizer.normalize_card_code(
            input("Enter Leader Card Code (e.g., OP09-001): ")
        )
        
        # Pull Leader Synergies from Knowledge Graph
        synergies = graph.find_deck_engine(leader_code)
        
        if not synergies:
            print(f"[-] No registered synergy engines found for Leader [{leader_code}].")
            return

        print(f"\n[+] Recommended Core Engine Cards for Leader [{leader_code}]:")
        for card_id in synergies:
            node_data = graph.graph.nodes.get(card_id, {})
            name = node_data.get("name", "Unknown")
            print(f"  • [{card_id}] {name}")
            
        print("\n[✔] Synergy analysis complete.")