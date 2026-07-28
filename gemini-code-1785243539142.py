# main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Card, InventoryItem, PriceSnapshot
from src.engine.normalizer import DataNormalizer

def bootstrap_system():
    print("==================================================")
    print("  ETERNAL ANCHOR CORE BOOTSTRAP v0.1 ALPHA       ")
    print("==================================================")

    # 1. Initialize SQLite Core Storage
    engine = create_engine("sqlite:///eternal_anchor.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("[✔] Database schema initialized.")

    # 2. Initialize Normalizer
    normalizer = DataNormalizer()

    # 3. Seed Founders Baseline Data
    seed_data = [
        {"raw_code": "op05-119", "name": "Monkey.D.Luffy", "rarity": "Manga Rare", "price": 3850.00, "location": "Binder 1 (Vault Page 1)"},
        {"raw_code": "op06-118", "name": "Roronoa Zoro", "rarity": "Manga Art", "price": 1200.00, "location": "Binder 1 (Vault Page 1)"},
        {"raw_code": "st13-001", "name": "Sabo (Flagship)", "rarity": "Promo", "price": 850.00, "location": "Display Case / Tier 1"},
    ]

    for item in seed_data:
        code = normalizer.normalize_card_code(item["raw_code"])
        rarity = normalizer.categorize_rarity(item["rarity"])

        # Add Card entity if missing
        card = session.query(Card).filter_by(card_id=code).first()
        if not card:
            card = Card(card_id=code, name=item["name"], set_code=code.split("-")[0], rarity=rarity, category="Character")
            session.add(card)

        # Add Inventory record
        inv = InventoryItem(card_id=code, location=item["location"], condition="NM", acquisition_price=item["price"])
        session.add(inv)

        # Add Price Snapshot
        price = PriceSnapshot(card_id=code, market_price=item["price"])
        session.add(price)

    session.commit()
    print(f"[✔] Seeded {len(seed_data)} canonical cards into Entity Registry.")

    # 4. Captain's Console Output
    print("\n--- CAPTAIN'S CONSOLE: ACTIVE INVENTORY SNAPSHOT ---")
    inventory = session.query(InventoryItem).all()
    for item in inventory:
        print(f"• [{item.card_id}] {item.card.name} | Location: {item.location} | Value: ${item.acquisition_price:,.2f}")

if __name__ == "__main__":
    bootstrap_system()