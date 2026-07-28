# src/console/plugins/data_importer.py
import csv
import json
import os
from src.console.plugins.base import ConsolePlugin
from src.database.models import Card, InventoryItem, PriceSnapshot

class DataImporterPlugin(ConsolePlugin):
    @property
    def name(self) -> str:
        return "Batch Inventory Importer (CSV / JSON)"

    @property
    def description(self) -> str:
        return "Ingests card collection sheets or API exports into the database."

    def execute(self, session, normalizer, graph) -> None:
        print("\n=== BATCH DATA IMPORTER ===")
        file_path = input("Enter path to file (.csv or .json): ").strip()

        if not os.path.exists(file_path):
            print(f"[-] Error: File not found at '{file_path}'")
            return

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".csv":
            self._import_csv(file_path, session, normalizer)
        elif ext == ".json":
            self._import_json(file_path, session, normalizer)
        else:
            print("[-] Unsupported file format. Please provide a .csv or .json file.")

    def _process_record(self, record: dict, session, normalizer) -> bool:
        """Processes and normalizes a single card record entry."""
        # Field mapping flexibility (handles different column names)
        raw_code = str(record.get("card_id") or record.get("id") or record.get("code") or "").strip()
        name = str(record.get("name") or "Unknown Card").strip()
        raw_rarity = str(record.get("rarity") or "C").strip()
        category = str(record.get("category") or "Character").strip()
        location = str(record.get("location") or "Unsorted Inventory").strip()
        condition = str(record.get("condition") or "NM").strip()

        # Parse price
        try:
            price = float(record.get("acquisition_price") or record.get("price") or 0.0)
        except ValueError:
            price = 0.0

        if not raw_code:
            return False

        # Apply Normalization Rules
        canonical_code = normalizer.normalize_card_code(raw_code)
        rarity = normalizer.categorize_rarity(raw_rarity)
        set_code = canonical_code.split("-")[0] if "-" in canonical_code else "PROMO"

        # 1. Upsert Card definition
        card = session.query(Card).filter_by(card_id=canonical_code).first()
        if not card:
            card = Card(
                card_id=canonical_code,
                name=name,
                set_code=set_code,
                rarity=rarity,
                category=category
            )
            session.add(card)

        # 2. Append Inventory Item record
        inv = InventoryItem(
            card_id=canonical_code,
            location=location,
            condition=condition,
            acquisition_price=price
        )
        session.add(inv)

        # 3. Append Price Snapshot
        if price > 0:
            snapshot = PriceSnapshot(card_id=canonical_code, market_price=price)
            session.add(snapshot)

        return True

    def _import_csv(self, file_path: str, session, normalizer):
        count = 0
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if self._process_record(row, session, normalizer):
                    count += 1

        session.commit()
        print(f"[✔] Import complete! Processed {count} CSV records into inventory.")

    def _import_json(self, file_path: str, session, normalizer):
        count = 0
        with open(file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            # Handle either a list of items or an object containing a 'cards' array
            records = data if isinstance(data, list) else data.get("cards", [])

            for record in records:
                if self._process_record(record, session, normalizer):
                    count += 1

        session.commit()
        print(f"[✔] Import complete! Processed {count} JSON records into inventory.")