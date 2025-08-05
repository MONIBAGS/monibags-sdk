# MoniBags SDK

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![API](https://img.shields.io/badge/API-monibags.xyz-orange)](https://monibags.xyz)

Official Python SDK for MoniBags - The Truth Detector for Crypto Twitter. Expose fake builders and larpers by checking Twitter username history.

## 🚀 Features

- ✅ Check Twitter username history
- 🔍 Detect account rebranding attempts
- 🚫 Identify potential scammers and larpers
- 📊 Batch processing for multiple accounts
- 🔄 Rate limit handling
- 📁 Export results to JSON

## 📦 Installation

### Install from source
```bash
git clone https://github.com/monibags/monibags-sdk.git
cd monibags-sdk
pip install -e .
```

## 🔧 Quick Start

### Basic Usage

```python
from monibags import MoniBagsSDK

# Initialize SDK
sdk = MoniBagsSDK()

# Check single username
result = sdk.check_username_history("elonmusk")

if result['success']:
    data = result['data']
    if data['is_clean']:
        print(f"✅ @{data['current_username']} is CLEAN")
    else:
        print(f"⚠️ Found {data['total_changes']} username changes")
        print(f"Previous names: {data['history']}")
```

### CLI Usage

```bash
# Check single account
monibags check elonmusk

# Check multiple accounts
monibags check user1 user2 user3

# Save results to file
monibags check elonmusk --save --output results.json
```

## 📚 Documentation

### SDK Methods

#### `check_username_history(username: str) -> dict`
Check username history for a single Twitter account.

**Parameters:**
- `username` (str): Twitter username (with or without @)

**Returns:**
- `dict`: Response containing history data

**Example:**
```python
result = sdk.check_username_history("vitalikbuterin")
```

#### `batch_check(usernames: List[str], delay: float = 2.0) -> List[dict]`
Check multiple usernames with automatic rate limiting.

**Parameters:**
- `usernames` (List[str]): List of Twitter usernames
- `delay` (float): Delay between requests in seconds

**Returns:**
- `List[dict]`: Results for each username

**Example:**
```python
usernames = ["jack", "cz_binance", "SBF_FTX"]
results = sdk.batch_check(usernames, delay=3)
```

#### `analyze_profile(username: str) -> dict`
Perform full profile analysis including network connections.

**Parameters:**
- `username` (str): Twitter username

**Returns:**
- `dict`: Complete analysis with profile, network, and interaction data

**Example:**
```python
analysis = sdk.analyze_profile("balajis")
```

### Response Format

#### Success Response
```json
{
    "success": true,
    "data": {
        "current_username": "example",
        "total_changes": 2,
        "is_clean": false,
        "history": ["oldname1", "oldname2"],
        "insights": ["Username changed 2 times"],
        "warnings": ["Potential rebrand detected"],
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Rate limit exceeded",
    "message": "Please wait before making another request"
}
```

## 🎯 Use Cases

### 1. Verify Crypto Influencers
```python
from monibags import MoniBagsSDK

sdk = MoniBagsSDK()

influencers = [
    "cryptopunk6529",
    "cobie",
    "inversebrah"
]

for username in influencers:
    result = sdk.check_username_history(username)
    if result['success']:
        data = result['data']
        print(f"@{username}: {'✅ CLEAN' if data['is_clean'] else '⚠️ SUSPICIOUS'}")
```

### 2. Due Diligence for Projects
```python
# Check team members of a crypto project
team_members = ["founder_username", "cto_username", "community_manager"]
results = sdk.batch_check(team_members)

# Generate report
suspicious_count = sum(1 for r in results if r['success'] and not r['data']['is_clean'])
if suspicious_count > 0:
    print(f"⚠️ Warning: {suspicious_count} team members have changed usernames")
```

### 3. Export Results for Analysis
```python
import json
from datetime import datetime

# Check multiple accounts
accounts = ["account1", "account2", "account3"]
results = sdk.batch_check(accounts)

# Save with timestamp
filename = f"monibags_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Results saved to {filename}")
```

## 🔒 Rate Limiting

The SDK automatically handles rate limiting. Default limits:
- 100 requests per minute
- 1000 requests per hour

For batch operations, use the `delay` parameter to avoid hitting limits:
```python
results = sdk.batch_check(large_list, delay=5)  # 5 seconds between requests
```

## 🛠️ Advanced Configuration

### Custom Base URL
```python
# Use a custom API endpoint
sdk = MoniBagsSDK(base_url="https://api.monibags.xyz")
```

### Custom Headers
```python
sdk = MoniBagsSDK()
sdk.session.headers.update({
    'X-API-Key': 'your-api-key',
    'X-Custom-Header': 'value'
})
```

## 📊 Examples

More examples available in the [examples/](examples/) directory:
- [basic_usage.py](examples/basic_usage.py) - Simple username checking
- [batch_processing.py](examples/batch_processing.py) - Process multiple accounts
- [export_results.py](examples/export_results.py) - Export to various formats
- [influencer_check.py](examples/influencer_check.py) - Check crypto influencers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Website**: [https://monibags.xyz](https://monibags.xyz)
- **Twitter**: [@monibagsxyz](https://x.com/monibagsxyz)
- **API Documentation**: [https://monibags.xyz/docs](https://monibags.xyz/docs)
- **GitHub**: [https://github.com/monibags/monibags-sdk](https://github.com/monibags/monibags-sdk)

## 💡 Support

For support, please open an issue on [GitHub](https://github.com/monibags/monibags-sdk/issues) or contact us on Twitter [@monibagsxyz](https://x.com/monibagsxyz).

---

**MoniBags** - End the Larping. Expose the Truth. 🎯
