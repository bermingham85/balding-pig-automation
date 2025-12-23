#!/usr/bin/env python3
"""
The Balding Pig - Environment Loader
Loads and validates environment variables for Python scripts
"""

import os
import sys
from dotenv import load_dotenv
from typing import Dict, Optional

class EnvLoader:
    """Handles loading and validation of environment variables"""
    
    def __init__(self, env_path: str = ".env"):
        self.env_path = env_path
        self.required_vars = [
            "SHOPIFY_STORE_URL",
            "SHOPIFY_ACCESS_TOKEN",
            "PRINTIFY_API_KEY",
            "OPENAI_API_KEY"
        ]
        self.config = {}
        
    def load(self) -> Dict[str, str]:
        """Load environment variables from .env file"""
        if not os.path.exists(self.env_path):
            print(f"❌ Error: {self.env_path} not found!")
            print("Run 'cp .env.example .env' and add your credentials")
            sys.exit(1)
            
        load_dotenv(self.env_path)
        
        # Load all environment variables
        self.config = {
            # eCommerce
            "SHOPIFY_STORE_URL": os.getenv("SHOPIFY_STORE_URL"),
            "SHOPIFY_ACCESS_TOKEN": os.getenv("SHOPIFY_ACCESS_TOKEN"),
            "SHOPIFY_API_VERSION": os.getenv("SHOPIFY_API_VERSION", "2024-01"),
            
            # Print on Demand
            "PRINTIFY_API_KEY": os.getenv("PRINTIFY_API_KEY"),
            "PRINTIFY_SHOP_ID": os.getenv("PRINTIFY_SHOP_ID"),
            
            # AI Services
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
            
            # Storage
            "STORAGE_PROVIDER": os.getenv("STORAGE_PROVIDER", "aws"),
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
            "S3_BUCKET_NAME": os.getenv("S3_BUCKET_NAME"),
            
            # Database
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            
            # Webhooks
            "WEBHOOK_SECRET": os.getenv("WEBHOOK_SECRET"),
            "WEBHOOK_ENDPOINT": os.getenv("WEBHOOK_ENDPOINT"),
            "N8N_WEBHOOK_URL": os.getenv("N8N_WEBHOOK_URL"),
            "MAKE_WEBHOOK_URL": os.getenv("MAKE_WEBHOOK_URL"),
            
            # General
            "NODE_ENV": os.getenv("NODE_ENV", "development"),
            "PORT": os.getenv("PORT", "3000"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "info")
        }
        
        return self.config
    
    def validate(self) -> bool:
        """Validate that required environment variables are set"""
        missing = []
        
        for var in self.required_vars:
            if not self.config.get(var):
                missing.append(var)
        
        if missing:
            print("❌ Missing required environment variables:")
            for var in missing:
                print(f"   - {var}")
            return False
            
        print("✅ All required environment variables loaded")
        return True
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a specific environment variable"""
        return self.config.get(key, default)

# Usage example
if __name__ == "__main__":
    loader = EnvLoader()
    config = loader.load()
    
    if loader.validate():
        print("\n🐷 The Balding Pig environment loaded successfully!")
        print(f"   Shopify Store: {config['SHOPIFY_STORE_URL']}")
        print(f"   Storage Provider: {config['STORAGE_PROVIDER']}")
        print(f"   Environment: {config['NODE_ENV']}")