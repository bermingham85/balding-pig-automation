#!/usr/bin/env python3
"""
Quick script to update your server.py database configuration
"""

import fileinput
import sys

def update_database_config():
    """Update database configuration in server.py"""
    
    print("🐷 Updating database configuration...")
    
    # The old and new database configurations
    old_config = 'DATABASE_URL = os.environ.get("DATABASE_URL")'
    new_config = 'DATABASE_URL = "postgresql://postgres:YOUR_SUPABASE_PASSWORD@db.gzrvzdrmmupqkjosrfnd.supabase.co:5432/postgres"'
    
    try:
        # Read server.py and update the line
        updated = False
        with fileinput.FileInput('server.py', inplace=True) as file:
            for line in file:
                if old_config in line:
                    print(new_config)
                    updated = True
                else:
                    print(line, end='')
        
        if updated:
            print("✅ Database configuration updated!")
            print("⚠️  Remember to add your actual Supabase password!")
        else:
            print("⚠️  Could not find database configuration line")
            print("Please manually update this line in server.py:")
            print(f"   {new_config}")
            
    except FileNotFoundError:
        print("❌ server.py not found in current directory")
        print("Please run this script in your project directory")

if __name__ == "__main__":
    update_database_config()