#!/usr/bin/env python3
"""
Batch processing example for MoniBags SDK
"""

from monibags import MoniBagsSDK
import json
from datetime import datetime


def progress_callback(current, total, username):
    """Custom progress callback"""
    percentage = (current / total) * 100
    print(f"[{current}/{total}] ({percentage:.1f}%) Checking @{username}...")


def main():
    # Initialize SDK
    sdk = MoniBagsSDK()
    
    # List of crypto influencers to check
    crypto_influencers = [
        "aantonop",
        "APompliano", 
        "cz_binance",
        "VitalikButerin",
        "SatoshiLite",
        "balajis",
        "naval"
    ]
    
    print("=" * 60)
    print("MoniBags Batch Processing - Crypto Influencer Check")
    print("=" * 60)
    print(f"\nChecking {len(crypto_influencers)} accounts...")
    print("-" * 60)
    
    # Batch check with custom progress callback
    results = sdk.batch_check(
        crypto_influencers, 
        delay=3,  # 3 seconds between requests
        progress_callback=progress_callback
    )
    
    # Analyze results
    clean_accounts = []
    suspicious_accounts = []
    failed_checks = []
    
    for result in results:
        username = result.get('username', 'unknown')
        
        if result.get('success'):
            data = result['data']
            if data.get('is_clean'):
                clean_accounts.append(username)
            else:
                suspicious_accounts.append({
                    'username': username,
                    'changes': data.get('total_changes', 0),
                    'history': data.get('history', [])
                })
        else:
            failed_checks.append({
                'username': username,
                'error': result.get('error', 'Unknown error')
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING RESULTS")
    print("=" * 60)
    
    print(f"\n✅ Clean Accounts ({len(clean_accounts)}):")
    if clean_accounts:
        for acc in clean_accounts:
            print(f"   • @{acc}")
    else:
        print("   None")
    
    print(f"\n⚠️  Accounts with Username Changes ({len(suspicious_accounts)}):")
    if suspicious_accounts:
        for acc in suspicious_accounts:
            print(f"   • @{acc['username']} - {acc['changes']} changes")
            if acc['history']:
                print(f"     Previous names: {', '.join(acc['history'][:3])}")
    else:
        print("   None")
    
    print(f"\n❌ Failed Checks ({len(failed_checks)}):")
    if failed_checks:
        for acc in failed_checks:
            print(f"   • @{acc['username']}: {acc['error']}")
    else:
        print("   None")
    
    # Calculate statistics
    total_checked = len(results)
    success_rate = ((len(clean_accounts) + len(suspicious_accounts)) / total_checked * 100) if total_checked > 0 else 0
    
    print("\n" + "-" * 60)
    print("STATISTICS")
    print("-" * 60)
    print(f"Total accounts checked: {total_checked}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Clean rate: {(len(clean_accounts) / total_checked * 100):.1f}%")
    
    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"batch_results_{timestamp}.json"
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_checked': total_checked,
            'clean': len(clean_accounts),
            'suspicious': len(suspicious_accounts),
            'failed': len(failed_checks)
        },
        'clean_accounts': clean_accounts,
        'suspicious_accounts': suspicious_accounts,
        'failed_checks': failed_checks,
        'detailed_results': results
    }
    
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")


if __name__ == "__main__":
    main()