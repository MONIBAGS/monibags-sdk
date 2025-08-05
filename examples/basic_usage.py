#!/usr/bin/env python3
"""
Basic usage example for MoniBags SDK
"""

from monibags import MoniBagsSDK

def main():
    # Initialize SDK
    sdk = MoniBagsSDK()
    
    # Example 1: Check single username
    print("=" * 50)
    print("Example 1: Check Single Username")
    print("=" * 50)
    
    username = "elonmusk"
    print(f"\nChecking @{username}...")
    
    try:
        result = sdk.check_username_history(username)
        
        if result['success']:
            data = result['data']
            
            print(f"\n✓ Username: @{data['current_username']}")
            
            if data['is_clean']:
                print("✓ Status: CLEAN - No username changes detected")
            else:
                print(f"⚠ Status: {data['total_changes']} username changes detected")
                print("\nPrevious usernames:")
                for name in data.get('history', []):
                    print(f"  • {name}")
            
            # Print insights if available
            if data.get('insights'):
                print("\nInsights:")
                for insight in data['insights']:
                    print(f"  {insight}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")
    
    # Example 2: Format and display result
    print("\n" + "=" * 50)
    print("Example 2: Formatted Output")
    print("=" * 50)
    
    username = "vitalikbuterin"
    print(f"\nChecking @{username}...")
    
    try:
        result = sdk.check_username_history(username)
        # Use built-in formatter
        print(sdk.format_result(result))
        
    except Exception as e:
        print(f"Exception occurred: {e}")


if __name__ == "__main__":
    main()