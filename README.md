# 🔍 Dehashed Data Extractor

Fetch and process leaked credentials and personal information from the [Dehashed API](https://www.dehashed.com/) for a specific domain.
This tool is fully compatible with the latest DeHashed V2 API, ensuring accurate and up-to-date breach data retrieval.

---

## 📦 Features

- 🧠 Fetches data using Dehashed API with pagination
- 📁 Generates:
  - `emails.txt`: List of unique email addresses
  - `Email-Password.txt`: Combos of email:password
  - `Email-Hash.txt`: Combos of email:hash
  - `outData.csv`: Structured CSV of all combinations
  - `summary.json`: Count summary of extracted fields
  - `rawData.json`: Raw response from Dehashed
- 📢 Verbose output with:
  - API balance shown after execution
  - Entry summary printed in terminal
- 🛡️ Error-handling and status reporting

---

## 🚀 Usage

```bash
python main.py -d <domain.com> -k <DEHASHED_API_KEY>
```

![DeHashed Tool Demo](https://i.imgur.com/5vkkp9c.png)
