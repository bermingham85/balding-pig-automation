#!/usr/bin/env python3
"""
Printify Configuration Helper Script
This script will help you get your Shop ID, Blueprint IDs, and Provider IDs
"""

import requests
import json

# Your Printify API key
PRINTIFY_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjcwMjQyYTlkZDczNGY5ZGU0NDlkNWZjYjU0ZjVhYzdkYzNmNjM4ODA0NGZhMjY1YzJjMDJmNmUzMjFlNTM1Y2UwYzE1OTdhNmE2NWI5ZDIxIiwiaWF0IjoxNzQ5ODY0NjI1LjY2ODUxOCwibmJmIjoxNzQ5ODY0NjI1LjY2ODUyMSwiZXhwIjoxNzgxNDAwNjI1LjY1NDQ1NSwic3ViIjoiMTc0NzM2MDEiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIiwidXNlci5pbmZvIl19.J6tm0WTKzY1NyuFjkTfs_K-v1FAsisVGRqhGHo7BcVv5uMjc8vcDDHA-KAtOE0PGE8_Kme-XtZOnuDIvPs41wWb3xMKtr2jb_GdGVy7UAKGjskErCdHKhkoVgm5MkApUc52R9GzF9PSUe7tCAYlxzSYFCAQjEKICF4UJF1c5-wKEnjX2ucYTBDBTKNP3yKF117zAD49cj-PWqSXXzEv8qCuV4MIIjat3mMO09JdYF9NFq0tpVLmgasWIVQFOnMOoqpQybw5lI7LKu0nnHgfG3KQkmnHByK3UQy-tg-av-IwRm-TwkpCFtdQFB_4g47cCAsBONPcoufAiSRymf1LndJgpEs5Zo1o0ASMUrzfnel0ge8uV-OxoquDOgeVFuvoz6DqRTJJ1HcWHI5bD9-zKAkLM67tbu_VH0DEvsLkHjVeEnKSDN5ui8EhyYB6qhfBPWVHFzgbS2HI3JoqipV2crzrnGPSrFSxpn-Y3mK6NY3i2xw1Pxp0XRRSqcfxL04q9MJ5sqKV_hjatTiNQ7Uq2EFTo3YkhVumXIngMzi16RdW3TCmKU-kSZReTHtP5uz9096KE_7Sk7OVbAQdg9mZkSWRPXWROJUeKIroEpKOqXAVksOHBCYxtZGxV9EVcvA_aatCxv1bOd8EaKWpY-B5IchrLq96tYyD6alQnQSD2h-I"

BASE_URL = "https://api.printify.com/v1"

headers = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

def get_shops():
    """Get all shops associated with your account"""
    print("🏪 Getting your shops...")
    response = requests.get(f"{BASE_URL}/shops.json", headers=headers)
    
    if response.status_code == 200:
        shops = response.json()
        print(f"✅ Found {len(shops)} shop(s):")
        for shop in shops:
            print(f"   - Shop ID: {shop['id']} | Name: {shop['title']} | Platform: {shop.get('sales_channel', 'Unknown')}")
        return shops
    else:
        print(f"❌ Error getting shops: {response.status_code} - {response.text}")
        return []

def get_catalog():
    """Get available blueprints (product types)"""
    print("\n📚 Getting product catalog...")
    response = requests.get(f"{BASE_URL}/catalog/blueprints.json", headers=headers)
    
    if response.status_code == 200:
        blueprints = response.json()
        print(f"✅ Found {len(blueprints)} blueprint(s):")
        
        # Show popular product types
        popular_types = ["t-shirt", "hoodie", "mug", "poster", "canvas", "phone case", "sticker"]
        
        for blueprint in blueprints[:20]:  # Show first 20
            title = blueprint.get('title', '').lower()
            if any(product_type in title for product_type in popular_types):
                print(f"   ⭐ Blueprint ID: {blueprint['id']} | Name: {blueprint['title']}")
            else:
                print(f"   - Blueprint ID: {blueprint['id']} | Name: {blueprint['title']}")
        
        if len(blueprints) > 20:
            print(f"   ... and {len(blueprints) - 20} more blueprints")
        
        return blueprints
    else:
        print(f"❌ Error getting catalog: {response.status_code} - {response.text}")
        return []

def get_blueprint_providers(blueprint_id):
    """Get providers for a specific blueprint"""
    print(f"\n🏭 Getting providers for blueprint {blueprint_id}...")
    response = requests.get(f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers.json", headers=headers)
    
    if response.status_code == 200:
        providers = response.json()
        print(f"✅ Found {len(providers)} provider(s):")
        for provider in providers:
            print(f"   - Provider ID: {provider['id']} | Name: {provider['title']}")
        return providers
    else:
        print(f"❌ Error getting providers: {response.status_code} - {response.text}")
        return []

def recommend_configuration():
    """Recommend the best configuration for TheBaldingPig"""
    print("\n🎯 RECOMMENDED CONFIGURATION FOR THEBALDINGPIG:")
    print("=" * 60)
    
    # Get shops
    shops = get_shops()
    if shops:
        # Use the first shop (or let user choose)
        recommended_shop = shops[0]
        print(f"📍 SHOP_ID: {recommended_shop['id']}")
    
    # Get blueprints and find t-shirt
    blueprints = get_catalog()
    
    # Look for t-shirt blueprint (most popular for print-on-demand)
    tshirt_blueprint = None
    for blueprint in blueprints:
        if "t-shirt" in blueprint.get('title', '').lower() and "unisex" in blueprint.get('title', '').lower():
            tshirt_blueprint = blueprint
            break
    
    if not tshirt_blueprint:
        # Fallback to any t-shirt
        for blueprint in blueprints:
            if "t-shirt" in blueprint.get('title', '').lower():
                tshirt_blueprint = blueprint
                break
    
    if tshirt_blueprint:
        print(f"👕 BLUEPRINT_ID: {tshirt_blueprint['id']} ({tshirt_blueprint['title']})")
        
        # Get providers for this blueprint
        providers = get_blueprint_providers(tshirt_blueprint['id'])
        
        if providers:
            # Recommend first provider (usually the most popular)
            recommended_provider = providers[0]
            print(f"🏭 PROVIDER_ID: {recommended_provider['id']} ({recommended_provider['title']})")
    
    print("\n📋 ADD THESE TO YOUR .env FILE:")
    print(f"PRINTIFY_API_KEY={PRINTIFY_API_KEY}")
    if shops:
        print(f"PRINTIFY_SHOP_ID={shops[0]['id']}")
    if tshirt_blueprint:
        print(f"PRINTIFY_BLUEPRINT_ID={tshirt_blueprint['id']}")
        if providers:
            print(f"PRINTIFY_PROVIDER_ID={providers[0]['id']}")

if __name__ == "__main__":
    print("🚀 PRINTIFY CONFIGURATION HELPER")
    print("=" * 50)
    
    try:
        recommend_configuration()
        
        print("\n✅ Configuration complete!")
        print("💡 Copy the values above to your .env file to enable Printify integration.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your API key and internet connection.")