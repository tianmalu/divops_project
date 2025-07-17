#!/usr/bin/env python3
"""
Log analysis tool for TarotAI logs.
Provides insights into application behavior and performance.
"""

import os
import re
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import argparse

def parse_log_line(line: str) -> Dict[str, str]:
    """
    Parse a log line into its components.
    
    Args:
        line: Log line string
        
    Returns:
        Dictionary with parsed components
    """
    # Pattern: 2025-01-16 10:30:45 - app.rag_engine - INFO - Starting new discussion...
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - ([\w\.]+) - (\w+) - (.+)'
    
    match = re.match(pattern, line.strip())
    if match:
        return {
            'timestamp': match.group(1),
            'module': match.group(2),
            'level': match.group(3),
            'message': match.group(4)
        }
    return {}

def analyze_log_file(log_file: str) -> Dict:
    """
    Analyze a log file and return statistics.
    
    Args:
        log_file: Path to log file
        
    Returns:
        Dictionary with analysis results
    """
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return {}
    
    print(f"Analyzing log file: {log_file}")
    
    stats = {
        'total_lines': 0,
        'parsed_lines': 0,
        'log_levels': Counter(),
        'modules': Counter(),
        'error_messages': [],
        'warning_messages': [],
        'timeline': defaultdict(int),
        'user_activities': defaultdict(int),
        'api_endpoints': defaultdict(int),
        'performance_metrics': []
    }
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            stats['total_lines'] += 1
            
            parsed = parse_log_line(line)
            if parsed:
                stats['parsed_lines'] += 1
                
                # Count log levels
                stats['log_levels'][parsed['level']] += 1
                
                # Count modules
                stats['modules'][parsed['module']] += 1
                
                # Collect error and warning messages
                if parsed['level'] == 'ERROR':
                    stats['error_messages'].append({
                        'timestamp': parsed['timestamp'],
                        'module': parsed['module'],
                        'message': parsed['message']
                    })
                elif parsed['level'] == 'WARNING':
                    stats['warning_messages'].append({
                        'timestamp': parsed['timestamp'],
                        'module': parsed['module'],
                        'message': parsed['message']
                    })
                
                # Timeline analysis (by hour)
                try:
                    dt = datetime.strptime(parsed['timestamp'], '%Y-%m-%d %H:%M:%S')
                    hour_key = dt.strftime('%Y-%m-%d %H:00')
                    stats['timeline'][hour_key] += 1
                except ValueError:
                    pass
                
                # Extract user activities
                message = parsed['message']
                if 'user' in message.lower():
                    # Extract user ID patterns
                    user_matches = re.findall(r'user[_\s]+([a-zA-Z0-9_]+)', message, re.IGNORECASE)
                    for user_id in user_matches:
                        stats['user_activities'][user_id] += 1
                
                # Extract API endpoint usage
                if 'endpoint' in message.lower() or 'request' in message.lower():
                    endpoint_matches = re.findall(r'(/[\w/]+)', message)
                    for endpoint in endpoint_matches:
                        if endpoint.startswith('/'):
                            stats['api_endpoints'][endpoint] += 1
                
                # Performance metrics
                if 'response length' in message.lower():
                    length_matches = re.findall(r'(\d+)\s+characters', message)
                    if length_matches:
                        stats['performance_metrics'].append({
                            'timestamp': parsed['timestamp'],
                            'metric': 'response_length',
                            'value': int(length_matches[0])
                        })
    
    return stats

def print_analysis_report(stats: Dict):
    """
    Print a formatted analysis report.
    
    Args:
        stats: Analysis statistics
    """
    print("\n" + "="*60)
    print("TAROTAI LOG ANALYSIS REPORT")
    print("="*60)
    
    # Basic statistics
    print(f"\n📊 BASIC STATISTICS")
    print(f"Total lines: {stats['total_lines']:,}")
    print(f"Parsed lines: {stats['parsed_lines']:,}")
    print(f"Parse rate: {(stats['parsed_lines']/stats['total_lines']*100):.1f}%")
    
    # Log levels
    print(f"\n📈 LOG LEVELS")
    for level, count in stats['log_levels'].most_common():
        percentage = (count / stats['parsed_lines'] * 100) if stats['parsed_lines'] > 0 else 0
        print(f"  {level}: {count:,} ({percentage:.1f}%)")
    
    # Modules
    print(f"\n🔧 MODULES")
    for module, count in stats['modules'].most_common(10):
        percentage = (count / stats['parsed_lines'] * 100) if stats['parsed_lines'] > 0 else 0
        print(f"  {module}: {count:,} ({percentage:.1f}%)")
    
    # Errors
    if stats['error_messages']:
        print(f"\n❌ RECENT ERRORS (last 5)")
        for error in stats['error_messages'][-5:]:
            print(f"  {error['timestamp']} - {error['module']}: {error['message'][:80]}...")
    
    # Warnings
    if stats['warning_messages']:
        print(f"\n⚠️  RECENT WARNINGS (last 5)")
        for warning in stats['warning_messages'][-5:]:
            print(f"  {warning['timestamp']} - {warning['module']}: {warning['message'][:80]}...")
    
    # User activities
    if stats['user_activities']:
        print(f"\n👥 TOP USERS")
        for user, count in Counter(stats['user_activities']).most_common(10):
            print(f"  {user}: {count:,} activities")
    
    # API endpoints
    if stats['api_endpoints']:
        print(f"\n🌐 API ENDPOINTS")
        for endpoint, count in Counter(stats['api_endpoints']).most_common(10):
            print(f"  {endpoint}: {count:,} requests")
    
    # Timeline
    if stats['timeline']:
        print(f"\n⏰ ACTIVITY TIMELINE (last 24 hours)")
        sorted_timeline = sorted(stats['timeline'].items())
        for hour, count in sorted_timeline[-24:]:
            print(f"  {hour}: {count:,} log entries")
    
    # Performance metrics
    if stats['performance_metrics']:
        response_lengths = [m['value'] for m in stats['performance_metrics'] if m['metric'] == 'response_length']
        if response_lengths:
            avg_length = sum(response_lengths) / len(response_lengths)
            print(f"\n⚡ PERFORMANCE METRICS")
            print(f"  Average response length: {avg_length:.0f} characters")
            print(f"  Max response length: {max(response_lengths):,} characters")
            print(f"  Min response length: {min(response_lengths):,} characters")

def main():
    parser = argparse.ArgumentParser(description='Analyze TarotAI log files')
    parser.add_argument('log_file', nargs='?', help='Path to log file')
    parser.add_argument('--auto', action='store_true', help='Auto-find latest log file')
    parser.add_argument('--errors-only', action='store_true', help='Show only errors')
    parser.add_argument('--warnings-only', action='store_true', help='Show only warnings')
    
    args = parser.parse_args()
    
    # Auto-find log file
    if args.auto or not args.log_file:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        today = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'tarot_ai_{today}.log')
        
        if not os.path.exists(log_file):
            # Try to find any log file
            if os.path.exists(log_dir):
                log_files = [f for f in os.listdir(log_dir) if f.startswith('tarot_ai_') and f.endswith('.log')]
                if log_files:
                    log_file = os.path.join(log_dir, sorted(log_files)[-1])
                else:
                    print("No log files found in logs directory")
                    return
            else:
                print("Logs directory not found")
                return
    else:
        log_file = args.log_file
    
    # Analyze log file
    stats = analyze_log_file(log_file)
    
    if not stats:
        return
    
    # Print filtered report
    if args.errors_only:
        print(f"\n❌ ERRORS IN {log_file}")
        for error in stats['error_messages']:
            print(f"{error['timestamp']} - {error['module']}: {error['message']}")
    elif args.warnings_only:
        print(f"\n⚠️  WARNINGS IN {log_file}")
        for warning in stats['warning_messages']:
            print(f"{warning['timestamp']} - {warning['module']}: {warning['message']}")
    else:
        print_analysis_report(stats)

if __name__ == "__main__":
    main()
