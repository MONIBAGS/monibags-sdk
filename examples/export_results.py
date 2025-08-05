#!/usr/bin/env python3
"""
Export results example for MoniBags SDK
Shows how to export data in different formats
"""

from monibags import MoniBagsSDK
import json
import csv
from datetime import datetime


def export_to_markdown(results, filename):
    """Export results to Markdown format"""
    with open(filename, 'w') as f:
        f.write("# MoniBags Username History Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        
        total = len(results)
        clean = sum(1 for r in results if r.get('success') and r.get('data', {}).get('is_clean'))
        suspicious = sum(1 for r in results if r.get('success') and not r.get('data', {}).get('is_clean'))
        
        f.write(f"- Total accounts checked: {total}\n")
        f.write(f"- Clean accounts: {clean}\n")
        f.write(f"- Accounts with changes: {suspicious}\n\n")
        
        f.write("## Detailed Results\n\n")
        
        for result in results:
            if result.get('success'):
                data = result['data']
                username = data.get('current_username', 'unknown')
                
                f.write(f"### @{username}\n\n")
                
                if data.get('is_clean'):
                    f.write("✅ **Status:** CLEAN\n\n")
                else:
                    f.write(f"⚠️ **Status:** {data.get('total_changes', 0)} username changes detected\n\n")
                    
                    if data.get('history'):
                        f.write("**Previous usernames:**\n")
                        for name in data['history']:
                            f.write(f"- {name}\n")
                        f.write("\n")
                
                if data.get('insights'):
                    f.write("**Insights:**\n")
                    for insight in data['insights']:
                        f.write(f"- {insight}\n")
                    f.write("\n")
                
                f.write("---\n\n")


def export_to_html(results, filename):
    """Export results to HTML format"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>MoniBags Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #00ff41; }
        .clean { color: green; }
        .suspicious { color: orange; }
        .error { color: red; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>MoniBags Username History Report</h1>
    <p>Generated: {timestamp}</p>
    
    <h2>Summary</h2>
    <ul>
        <li>Total accounts: {total}</li>
        <li>Clean accounts: {clean}</li>
        <li>Suspicious accounts: {suspicious}</li>
    </ul>
    
    <h2>Results</h2>
    <table>
        <tr>
            <th>Username</th>
            <th>Status</th>
            <th>Changes</th>
            <th>Previous Names</th>
        </tr>
        {rows}
    </table>
</body>
</html>
    """
    
    rows = []
    total = len(results)
    clean = 0
    suspicious = 0
    
    for result in results:
        if result.get('success'):
            data = result['data']
            username = data.get('current_username', 'unknown')
            
            if data.get('is_clean'):
                clean += 1
                status = '<span class="clean">CLEAN ✅</span>'
                changes = '0'
                history = 'None'
            else:
                suspicious += 1
                status = '<span class="suspicious">CHANGES ⚠️</span>'
                changes = str(data.get('total_changes', 0))
                history = ', '.join(data.get('history', []))
            
            rows.append(f"""
        <tr>
            <td>@{username}</td>
            <td>{status}</td>
            <td>{changes}</td>
            <td>{history}</td>
        </tr>""")
    
    html_final = html_content.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total=total,
        clean=clean,
        suspicious=suspicious,
        rows=''.join(rows)
    )
    
    with open(filename, 'w') as f:
        f.write(html_final)


def main():
    # Initialize SDK
    sdk = MoniBagsSDK()
    
    # Check some accounts
    test_accounts = [
        "elonmusk",
        "jack",
        "vitalikbuterin"
    ]
    
    print("=" * 50)
    print("MoniBags Export Examples")
    print("=" * 50)
    print(f"\nChecking {len(test_accounts)} accounts...")
    
    results = sdk.batch_check(test_accounts, delay=2)
    
    # Export to different formats
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. JSON export (using SDK method)
    json_file = f"export_{timestamp}.json"
    sdk.export_results(results, json_file, format='json')
    print(f"✓ Exported to JSON: {json_file}")
    
    # 2. CSV export (using SDK method)
    csv_file = f"export_{timestamp}.csv"
    sdk.export_results(results, csv_file, format='csv')
    print(f"✓ Exported to CSV: {csv_file}")
    
    # 3. Markdown export (custom)
    md_file = f"export_{timestamp}.md"
    export_to_markdown(results, md_file)
    print(f"✓ Exported to Markdown: {md_file}")
    
    # 4. HTML export (custom)
    html_file = f"export_{timestamp}.html"
    export_to_html(results, html_file)
    print(f"✓ Exported to HTML: {html_file}")
    
    # 5. Custom JSON with additional metadata
    custom_json = {
        'report': {
            'title': 'MoniBags Username History Analysis',
            'generated_at': datetime.now().isoformat(),
            'sdk_version': '1.0.0',
            'total_accounts': len(results),
            'settings': {
                'delay_between_requests': 2,
                'api_endpoint': 'https://monibags.xyz'
            }
        },
        'results': results,
        'statistics': {
            'clean_accounts': sum(1 for r in results if r.get('success') and r.get('data', {}).get('is_clean')),
            'accounts_with_changes': sum(1 for r in results if r.get('success') and not r.get('data', {}).get('is_clean')),
            'failed_checks': sum(1 for r in results if not r.get('success'))
        }
    }
    
    custom_json_file = f"export_custom_{timestamp}.json"
    with open(custom_json_file, 'w') as f:
        json.dump(custom_json, f, indent=2)
    print(f"✓ Exported custom JSON: {custom_json_file}")
    
    print("\n" + "=" * 50)
    print("Export completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()