import json
import csv
from itertools import product
import requests
from config.config import Config


class DehashedProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.headers = {
            "Content-Type": "application/json",
            "Dehashed-Api-Key": config.api_key,
            "User-Agent": "Mozilla/5.0"
        }

    def fetch_data(self):
        all_entries = []
        page = 1
        raw_results = []

        print("📡 Fetching data from Dehashed API...")
        while True:
            payload = {"query": f'domain:{self.config.domain}', "page": page, "size": 10000}
            response = requests.post(self.config.base_url, headers=self.headers, json=payload)

            if response.status_code != 200:
                print(f"❌ Error fetching data on page {page}: {response.status_code} - {response.text}")
                break

            data = response.json()
            raw_results.append(data)

            entries = data.get("entries", [])
            print(f"✅ Page {page}: Retrieved {len(entries)} entries")

            if not entries:
                break

            all_entries.extend(entries)

            if len(entries) < 10000:
                break
            page += 1

        # Save raw JSON
        try:
            with open("rawData.json", "w") as f:
                json.dump(raw_results, f, indent=2)
            print("💾 Saved raw data to rawData.json")
        except Exception as e:
            print(f"❌ Error saving rawData.json: {e}")

        # Show API balance
        try:
            balance = raw_results[0].get("balance")
            print(f"💳 API Balance Remaining: {balance}")
        except Exception as e:
            print(f"⚠️ Could not read API balance from rawData.json: {e}")

        print(f"\n📊 Total entries fetched: {len(all_entries)}\n")
        return {"entries": all_entries}

    def normalize_field(self, value, field_name):
        if isinstance(value, list):
            return [v.strip() for v in value if v]
        return [value.strip()] if value else []

    def process_entries(self, entries):
        self.write_emails(entries)
        self.write_email_passwords(entries)
        self.write_email_hashes(entries)
        self.write_csv(entries)

        print("\n📄 Summary Report:")
        print(f"📧 Unique Emails: {self.count_unique(entries, 'email')}")
        print(f"🔐 Passwords: {self.count_unique(entries, 'password')}")
        print(f"🧬 Hashed Passwords: {self.count_unique(entries, 'hashed_password')}")

    def write_emails(self, entries):
        rows = []
        for entry in entries:
            rows.extend(self.normalize_field(entry.get("email", ""), "email"))
        self._write_file("emails.txt", sorted(set(rows)), "emails.txt")

    def write_email_passwords(self, entries):
        rows = []
        for entry in entries:
            emails = self.normalize_field(entry.get("email", ""), "email")
            passwords = self.normalize_field(entry.get("password", ""), "password")
            rows.extend(f"{e}:{p}" for e, p in product(emails, passwords))
        self._write_file("Email-Password.txt", sorted(set(rows)), "Email-Password.txt")

    def write_email_hashes(self, entries):
        rows = []
        for entry in entries:
            emails = self.normalize_field(entry.get("email", ""), "email")
            hashes = self.normalize_field(entry.get("hashed_password", ""), "hashed_password")
            rows.extend(f"{e}:{h}" for e, h in product(emails, hashes))
        self._write_file("Email-Hash.txt", sorted(set(rows)), "Email-Hash.txt")

    def write_csv(self, entries):
        fields = ["email", "ip_address", "username", "password", "hashed_password",
                  "name", "vin", "address", "phone", "database_name"]
        header = ["Email", "IP Address", "Username", "Password", "Hash", "Name", "VIN", "Address", "Phone", "Database"]
        rows = []

        for entry in entries:
            normalized = {f: self.normalize_field(entry.get(f, ""), f) for f in fields}
            combos = list(product(*[normalized[f] if normalized[f] else [""] for f in fields]))
            rows.extend(combos)

        try:
            with open("outData.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
            print("💾 outData.csv created with {} rows".format(len(rows)))
        except Exception as e:
            print(f"❌ Error writing outData.csv: {e}")

    def _write_file(self, filename, rows, label):
        try:
            with open(filename, "w") as f:
                f.write("\n".join(rows) + "\n")
            print(f"✅ {label} saved with {len(rows)} entries")
        except Exception as e:
            print(f"❌ Error writing {filename}: {e}")

    def count_unique(self, entries, field):
        values = set()
        for entry in entries:
            val = entry.get(field)
            if isinstance(val, list):
                values.update(v.strip() for v in val if v)
            elif val:
                values.add(val.strip())
        return len(values)
