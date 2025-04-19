import argparse
from src.dehashed_processor import DehashedProcessor
from config.config import Config
import json
import os

def main():
    parser = argparse.ArgumentParser(description="📡 Fetch and process Dehashed data.")
    parser.add_argument("-d", "--domain", required=True, help="🔍 Domain name to query")
    parser.add_argument("-k", "--apikey", required=True, help="🔑 Dehashed API key")
    args = parser.parse_args()

    config = Config(domain=args.domain, api_key=args.apikey)
    processor = DehashedProcessor(config)
    
    try:
        data = processor.fetch_data()
        entries = data.get("entries", [])
        processor.process_entries(entries)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # ✅ Read API balance from rawData.json
    try:
        if os.path.exists("rawData.json"):
            with open("rawData.json", "r") as f:
                raw_data = json.load(f)
                balance = raw_data[0].get("balance", "Unknown")
                print(f"\n💳 API Balance Remaining: {balance}")
        else:
            print("⚠️ rawData.json not found to read API balance.")
    except Exception as e:
        print(f"⚠️ Could not read API balance: {e}")

if __name__ == "__main__":
    main()
