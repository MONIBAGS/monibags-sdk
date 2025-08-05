"""
CLI interface for MoniBags SDK
"""

import sys
import argparse
import json
from datetime import datetime
from .sdk import MoniBagsSDK
from .version import __version__


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='MoniBags - Twitter Username History Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  monibags check elonmusk
  monibags check user1 user2 user3
  monibags check username --save
  monibags check username --save --output results.json
  monibags analyze vitalikbuterin
  monibags batch usernames.txt --delay 3
        """
    )
    
    parser.add_argument('--version', action='version', version=f'MoniBags SDK v{__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check username history')
    check_parser.add_argument('usernames', nargs='+', help='Twitter username(s) to check')
    check_parser.add_argument('--save', action='store_true', help='Save results to file')
    check_parser.add_argument('--output', default=None, help='Output filename')
    check_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Full profile analysis')
    analyze_parser.add_argument('username', help='Twitter username to analyze')
    analyze_parser.add_argument('--save', action='store_true', help='Save results to file')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch check from file')
    batch_parser.add_argument('file', help='File containing usernames (one per line)')
    batch_parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests')
    batch_parser.add_argument('--output', default=None, help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    sdk = MoniBagsSDK()
    
    if args.command == 'check':
        if len(args.usernames) == 1:
            # Single username
            username = args.usernames[0]
            print(f"Checking @{username}...")
            
            try:
                result = sdk.check_username_history(username)
                print(sdk.format_result(result))
                
                if args.save:
                    output_file = args.output or f"monibags_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
                    sdk.export_results([result], output_file, args.format)
                    
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            # Multiple usernames
            results = sdk.batch_check(args.usernames)
            
            for result in results:
                print(sdk.format_result(result))
            
            if args.save:
                output_file = args.output or f"monibags_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
                sdk.export_results(results, output_file, args.format)
    
    elif args.command == 'analyze':
        print(f"Analyzing @{args.username}...")
        
        try:
            result = sdk.analyze_profile(args.username)
            
            if result.get('success'):
                print(f"\nProfile Analysis for @{args.username}")
                print("="*50)
                print(f"Followers: {result.get('profile', {}).get('followers_count', 'N/A')}")
                print(f"Following: {result.get('profile', {}).get('following_count', 'N/A')}")
                print(f"Network size: {len(result.get('network', []))}")
                
                if args.save:
                    output_file = f"monibags_analysis_{args.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"\nAnalysis saved to {output_file}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.command == 'batch':
        # Read usernames from file
        try:
            with open(args.file, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
            
            print(f"Loaded {len(usernames)} usernames from {args.file}")
            results = sdk.batch_check(usernames, delay=args.delay)
            
            # Print summary
            clean_count = sum(1 for r in results if r.get('success') and r.get('data', {}).get('is_clean'))
            suspicious_count = sum(1 for r in results if r.get('success') and not r.get('data', {}).get('is_clean'))
            error_count = sum(1 for r in results if not r.get('success'))
            
            print("\n" + "="*50)
            print("Batch Check Summary")
            print("="*50)
            print(f"Total checked: {len(results)}")
            print(f"Clean accounts: {clean_count}")
            print(f"Suspicious accounts: {suspicious_count}")
            print(f"Errors: {error_count}")
            
            # Save results
            output_file = args.output or f"monibags_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nDetailed results saved to {output_file}")
            
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()