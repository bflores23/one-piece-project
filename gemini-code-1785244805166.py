# src/console/plugins/financial_report.py
from src.console.plugins.base import ConsolePlugin
from src.database.models import InventoryItem
from sqlalchemy.sql import func

class FinancialReportPlugin(ConsolePlugin):
    @property
    def name(self) -> str:
        return "Executive Collection Financial Report"

    @property
    def description(self) -> str:
        return "Generates total collection valuation and location breakdown."

    def execute(self, session, normalizer, graph) -> None:
        print("\n=== EXECUTIVE FINANCIAL REPORT ===")
        
        total_val = session.query(func.sum(InventoryItem.acquisition_price)).scalar() or 0.0
        total_count = session.query(func.count(InventoryItem.id)).scalar() or 0
        
        print(f"• Total Collection Estimated Value: ${total_val:,.2f}")
        print(f"• Total Tracked Items: {total_count}")
        
        print("\n--- Breakdown by Storage Location ---")
        location_breakdown = session.query(
            InventoryItem.location, 
            func.count(InventoryItem.id),
            func.sum(InventoryItem.acquisition_price)
        ).group_by(InventoryItem.location).all()
        
        for loc, count, val in location_breakdown:
            print(f"  • {loc}: {count} cards | Total Value: ${val:,.2f}")
            
        print("\n[✔] Financial audit generated.")