#!/usr/bin/env python3
"""
The Balding Pig - Automatic Printify Configuration
This script automatically updates your .env file with Printify settings
"""

import requests
import os
from dotenv import load_dotenv, set_key

# Load current environment
load_dotenv()

def auto_configure_printify():
    """Automatically configure Printify settings in .env"""
    
    print("🐷 The Balding Pig - Automatic Printify Configuration")
    print("="*50)
    
    # Check for API key
    api_key = os.getenv('PRINTIFY_API_KEY')
    if not api_key:
        print("❌ PRINTIFY_API_KEY not found in .env")
        print("Please add it first, then run this script again")
        return
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Fetching your Printify shops...")
    
    try:
        # Get shops
        response = requests.get('https://api.printify.com/v1/shops.json', headers=headers)
        
        if response.status_code == 200:
            shops = response.json()
            
            if shops:
                # Use the first shop
                shop_id = shops[0]['id']
                shop_name = shops[0]['title']
                
                print(f"✅ Found shop: {shop_name} (ID: {shop_id})")
                
                # Update .env file
                env_file = '.env'
                
                # Update PRINTIFY_SHOP_ID
                set_key(env_file, 'PRINTIFY_SHOP_ID', str(shop_id))
                print(f"✅ Updated PRINTIFY_SHOP_ID={shop_id}")
                
                # Set default blueprint (Unisex Softstyle T-Shirt)
                set_key(env_file, 'PRINTIFY_BLUEPRINT_ID', '3')
                print(f"✅ Updated PRINTIFY_BLUEPRINT_ID=3 (Unisex Softstyle T-Shirt)")
                
                # Add provider ID
                set_key(env_file, 'PRINTIFY_PROVIDER_ID', '99')
                print(f"✅ Added PRINTIFY_PROVIDER_ID=99 (PrintifyChoice)")
                
                print("\n🎉 Configuration complete!")
                print("\n📋 Popular blueprint IDs for reference:")
                print("   3 - Unisex Softstyle T-Shirt (RECOMMENDED)")
                print("   5 - Unisex Heavy Cotton Tee")
                print("   6 - Unisex Jersey Short Sleeve Tee")
                print("   145 - Bella + Canvas 3001")
                print("   265 - Next Level 3600")
                
                print("\n✅ Your .env file has been automatically updated!")
                print("Press Enter to continue...")
                input()
                
            else:
                print("❌ No shops found. Please create a shop on Printify first.")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    auto_configure_printify()
