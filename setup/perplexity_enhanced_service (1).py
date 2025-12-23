import requests
import json
import logging
from typing import List, Dict, Any, Optional
from config import (GOAPI_KEY, OPENAI_API_KEY, NOTION_API_KEY, NOTION_DATABASE_ID, 
                   DISCORD_WEBHOOK_URL, PRINTIFY_API_KEY, PERPLEXITY_API_KEY)

logger = logging.getLogger(__name__)

class EnhancedGoAPIService:
    """Enhanced service class with Perplexity trend research for better product ideas"""
    
    BASE_URL = "https://api.goapi.ai/api"
    PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
    
    @staticmethod
    def _make_request(endpoint: str, method: str = "POST", data: Dict = None, headers: Dict = None) -> Dict:
        """Make a request to GoAPI.ai or handle direct API calls"""
        url = f"{EnhancedGoAPIService.BASE_URL}/{endpoint}"
        
        default_headers = {
            "Authorization": f"Bearer {GOAPI_KEY}",
            "Content-Type": "application/json"
        }
        
        if headers:
            default_headers.update(headers)
        
        try:
            if method == "POST":
                response = requests.post(url, json=data, headers=default_headers, timeout=30)
            else:
                response = requests.get(url, params=data, headers=default_headers, timeout=30)
            
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def research_trends_with_perplexity(topic: str) -> Dict:
        """Use Perplexity to research current trends related to the product topic"""
        if not PERPLEXITY_API_KEY:
            logger.warning("Perplexity API key not configured")
            return {"success": False, "message": "Perplexity API key not configured"}
        
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Research current market trends, popular styles, and consumer preferences for: {topic}

Please provide:
1. Current trending styles and aesthetics
2. Popular color schemes and design elements  
3. Target demographics and their preferences
4. Seasonal considerations and timing
5. Pricing insights and market positioning
6. Popular keywords and hashtags
7. Competitor analysis and market gaps

Focus on actionable insights for creating print-on-demand products."""
        
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert market researcher specializing in e-commerce and print-on-demand products. Provide current, actionable insights based on real market data."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(EnhancedGoAPIService.PERPLEXITY_URL, 
                                   json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            trend_research = result["choices"][0]["message"]["content"]
            
            logger.info(f"Successfully researched trends for: {topic}")
            return {
                "success": True, 
                "research": trend_research,
                "citations": result.get("citations", [])
            }
            
        except Exception as e:
            logger.error(f"Perplexity trend research failed: {e}")
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def generate_enhanced_product_ideas(user_prompt: str, count: int = 5) -> List[Dict]:
        """Generate product ideas enhanced with real-time trend research"""
        logger.info(f"Generating {count} enhanced product ideas for prompt: {user_prompt}")
        
        # Step 1: Research current trends
        trend_research = EnhancedGoAPIService.research_trends_with_perplexity(user_prompt)
        
        trend_context = ""
        if trend_research.get("success"):
            trend_context = f"\n\nCURRENT MARKET RESEARCH:\n{trend_research['research']}\n"
            logger.info("Incorporated trend research into product generation")
        
        # Step 2: Generate products with trend context
        enhanced_prompt = f"""
        Based on this user input: "{user_prompt}"
        {trend_context}
        
        Generate {count} unique, trend-aware e-commerce product ideas that incorporate current market insights. 
        For each product, provide:
        - name: A catchy, trendy product name that resonates with current market
        - description: A compelling product description (2-3 sentences) that highlights trending features
        - tagline: A memorable tagline that captures current consumer sentiment
        - design_style: Visual design style based on current trends (e.g., "Y2K minimalism", "cottagecore aesthetic", "dark academia")
        - colours: Trending color palette for 2025 (e.g., "sage green and cream", "digital purple and neon pink")
        - keywords: SEO keywords including trending terms and hashtags
        - ai_prompt: A detailed prompt for AI image generation incorporating current design trends
        - trend_score: Rate 1-10 how well this aligns with current trends
        - target_audience: Specific demographic this appeals to based on research
        
        Return the response as a JSON array of objects.
        """
        
        # Try multiple AI services for best results
        if OPENAI_API_KEY:
            return EnhancedGoAPIService._generate_via_openai(enhanced_prompt, count)
        elif GOAPI_KEY:
            return EnhancedGoAPIService._generate_via_goapi(enhanced_prompt, count)
        else:
            return EnhancedGoAPIService._generate_fallback_products(user_prompt, count)
    
    @staticmethod
    def _generate_via_openai(prompt: str, count: int) -> List[Dict]:
        """Generate products via OpenAI with enhanced prompting"""
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an expert e-commerce product designer with deep knowledge of current market trends. Always respond with valid JSON array."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                   json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            content = response.json()["choices"][0]["message"]["content"]
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            products = json.loads(content)
            logger.info(f"Generated {len(products)} enhanced products via OpenAI")
            return products if isinstance(products, list) else [products]
        
        except Exception as e:
            logger.error(f"OpenAI enhanced generation failed: {e}")
            return EnhancedGoAPIService._generate_fallback_products("fallback", count)
    
    @staticmethod
    def _generate_via_goapi(prompt: str, count: int) -> List[Dict]:
        """Generate products via GoAPI.ai with enhanced prompting"""
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an expert e-commerce product designer with deep knowledge of current market trends. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8
        }
        
        response = EnhancedGoAPIService._make_request("openai/chat/completions", data=data)
        
        if response["success"]:
            try:
                content = response["data"]["choices"][0]["message"]["content"]
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:-3]
                elif content.startswith("```"):
                    content = content[3:-3]
                
                products = json.loads(content)
                logger.info(f"Generated {len(products)} enhanced products via GoAPI")
                return products if isinstance(products, list) else [products]
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse enhanced GoAPI response: {e}")
                return EnhancedGoAPIService._generate_fallback_products("fallback", count)
        else:
            return EnhancedGoAPIService._generate_fallback_products("fallback", count)
    
    @staticmethod
    def _generate_fallback_products(user_prompt: str, count: int) -> List[Dict]:
        """Generate enhanced fallback products when AI APIs fail"""
        logger.warning("Using enhanced fallback product generation")
        
        # Enhanced fallback with trend-aware suggestions
        trending_styles = ["Y2K revival", "cottagecore", "dark academia", "minimalist brutalism", "maximalist dopamine"]
        trending_colors = ["sage green", "digital purple", "sunset orange", "ocean blue", "millennial pink"]
        
        products = []
        for i in range(count):
            style = trending_styles[i % len(trending_styles)]
            color = trending_colors[i % len(trending_colors)]
            
            product = {
                "name": f"Trending {user_prompt} - {style} Edition #{i+1}",
                "description": f"A {style.lower()} inspired product featuring {user_prompt.lower()} with contemporary design elements. Perfect for the modern consumer who values both style and authenticity.",
                "tagline": f"{style} meets {user_prompt} - trending now!",
                "design_style": style,
                "colours": f"{color} with complementary neutrals",
                "keywords": f"{user_prompt}, {style.replace(' ', '')}, trending, 2025, aesthetic, viral, {color.replace(' ', '')}",
                "ai_prompt": f"A beautiful {style.lower()} style design featuring {user_prompt}, {color} color palette, trending 2025 aesthetic, professional photography, clean background, high quality",
                "trend_score": 7 + (i % 3),  # Varying scores 7-9
                "target_audience": f"{style} enthusiasts, trend-conscious consumers aged 18-35"
            }
            products.append(product)
        
        return products
    
    @staticmethod
    def analyze_product_potential(product_data: Dict) -> Dict:
        """Use Perplexity to analyze the market potential of a specific product"""
        if not PERPLEXITY_API_KEY:
            return {"success": False, "message": "Perplexity API key not configured"}
        
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Analyze the market potential for this product:

Product Name: {product_data.get('name', 'Unknown')}
Description: {product_data.get('description', 'No description')}
Style: {product_data.get('design_style', 'Unknown')}
Target Keywords: {product_data.get('keywords', 'None')}

Please provide:
1. Market size and demand estimation
2. Competition level and key competitors
3. Pricing recommendations
4. Best marketing channels and strategies
5. Seasonal considerations
6. Risk factors and challenges
7. Success probability (1-10 scale)

Be specific and actionable."""
        
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a product market analyst specializing in e-commerce and print-on-demand. Provide data-driven insights."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 800
        }
        
        try:
            response = requests.post(EnhancedGoAPIService.PERPLEXITY_URL, 
                                   json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]
            
            return {
                "success": True, 
                "analysis": analysis,
                "citations": result.get("citations", [])
            }
            
        except Exception as e:
            logger.error(f"Product analysis failed: {e}")
            return {"success": False, "message": str(e)}
    
    # All other methods remain the same from the original service
    @staticmethod
    def add_products_to_notion(products: List[Dict]) -> List[str]:
        """Add products to Notion database (unchanged)"""
        if not NOTION_API_KEY or not NOTION_DATABASE_ID:
            logger.warning("Notion API key or Database ID not configured")
            return [""] * len(products)
        
        page_ids = []
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        for product in products:
            try:
                # Enhanced Notion data with trend information
                notion_data = {
                    "parent": {"database_id": NOTION_DATABASE_ID},
                    "properties": {
                        "Name": {"title": [{"text": {"content": product["name"]}}]},
                        "Description": {"rich_text": [{"text": {"content": product["description"]}}]},
                        "Tagline": {"rich_text": [{"text": {"content": product["tagline"]}}]},
                        "Design Style": {"rich_text": [{"text": {"content": product["design_style"]}}]},
                        "Colors": {"rich_text": [{"text": {"content": product["colours"]}}]},
                        "Keywords": {"rich_text": [{"text": {"content": product["keywords"]}}]},
                        "AI Prompt": {"rich_text": [{"text": {"content": product["ai_prompt"]}}]},
                        "Status": {"select": {"name": "Generated"}}
                    }
                }
                
                # Add trend-specific fields if available
                if "trend_score" in product:
                    notion_data["properties"]["Trend Score"] = {"number": product["trend_score"]}
                if "target_audience" in product:
                    notion_data["properties"]["Target Audience"] = {"rich_text": [{"text": {"content": product["target_audience"]}}]}
                
                response = requests.post("https://api.notion.com/v1/pages", 
                                       json=notion_data, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    page_id = response.json()["id"]
                    page_ids.append(page_id)
                    logger.info(f"Added enhanced product to Notion: {product['name']}")
                else:
                    logger.error(f"Failed to add product to Notion: {response.text}")
                    page_ids.append("")
                    
            except Exception as e:
                logger.error(f"Error adding product to Notion: {e}")
                page_ids.append("")
        
        return page_ids
    
    @staticmethod
    def send_midjourney_prompt(ai_prompt: str) -> Dict:
        """Send image generation prompt to Discord (unchanged)"""
        if not DISCORD_WEBHOOK_URL:
            logger.warning("Discord webhook URL not configured")
            return {"success": False, "message": "Discord webhook not configured"}
        
        formatted_prompt = f"/imagine prompt: {ai_prompt} --ar 1:1 --v 6"
        
        data = {
            "content": formatted_prompt,
            "username": "Enhanced Product Generator Bot"
        }
        
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
            
            if response.status_code == 204:
                logger.info("Successfully sent enhanced Midjourney prompt to Discord")
                return {"success": True, "message": "Enhanced prompt sent to Midjourney"}
            else:
                logger.error(f"Discord webhook failed: {response.status_code}")
                return {"success": False, "message": "Failed to send Discord message"}
                
        except Exception as e:
            logger.error(f"Error sending Discord message: {e}")
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def create_printify_product(title: str, description: str, image_url: str, 
                               tags: List[str], shop_id: str, blueprint_id: str, 
                               provider_id: str) -> Dict:
        """Create a product in Printify (unchanged from original)"""
        if not PRINTIFY_API_KEY:
            logger.warning("Printify API key not configured")
            return {"success": False, "message": "Printify API key not configured"}
        
        headers = {
            "Authorization": f"Bearer {PRINTIFY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        product_data = {
            "title": title,
            "description": description,
            "blueprint_id": int(blueprint_id),
            "print_provider_id": int(provider_id),
            "variants": [
                {
                    "id": 1,
                    "price": 2000,
                    "is_enabled": True
                }
            ],
            "print_areas": [
                {
                    "variant_ids": [1],
                    "placeholders": [
                        {
                            "position": "front",
                            "images": [
                                {
                                    "id": image_url,
                                    "x": 0.5,
                                    "y": 0.5,
                                    "scale": 1,
                                    "angle": 0
                                }
                            ]
                        }
                    ]
                }
            ],
            "tags": tags[:10]
        }
        
        try:
            url = f"https://api.printify.com/v1/shops/{shop_id}/products.json"
            response = requests.post(url, json=product_data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                product_id = response.json()["id"]
                logger.info(f"Created enhanced Printify product: {title}")
                return {"success": True, "product_id": product_id}
            else:
                logger.error(f"Printify API error: {response.text}")
                return {"success": False, "message": response.text}
                
        except Exception as e:
            logger.error(f"Error creating Printify product: {e}")
            return {"success": False, "message": str(e)}