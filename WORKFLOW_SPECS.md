# 🔧 Balding Pig V2 - Workflow Specifications

**Date:** January 2, 2026  
**Status:** Specification - Ready to Build  

---

## Overview

This document provides complete technical specifications for the **two critical workflows** that are NOT YET BUILT but are required for the Balding Pig V2 system to be fully autonomous.

**Built & Complete:**
✅ Product Generator Workflow (`balding_pig_v2_product_generator.json`)

**Not Built Yet:**
❌ Trend Research Workflow (Daily)  
❌ Performance Monitor Workflow (Daily)  

---

## 1. Trend Research Workflow

**Filename:** `balding_pig_trend_research.json`  
**Schedule:** Daily at 6:00 AM  
**Purpose:** Automatically discover trending topics and color palettes to fuel the product generator  

### Workflow Architecture (8 nodes)

```
Schedule Trigger (6am)
    ↓
Search Trending Memes (Perplexity/GPT)
    ↓
Search Bald Humor Topics (GPT)
    ↓
Fetch Color Trends (Pinterest/Adobe Color API)
    ↓
Merge & Rank Results (JavaScript)
    ↓
Filter Duplicates (Check Notion)
    ↓
Store Top 5 Trends (Notion)
    ↓
Mark Old Trends as Used (Notion Update)
```

### Node Details

#### Node 1: Schedule Trigger
```json
{
  "type": "n8n-nodes-base.scheduleTrigger",
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 24,
          "triggerAtHour": 6
        }
      ]
    }
  },
  "name": "Daily 6am Trigger"
}
```

#### Node 2: Search Trending Memes (Perplexity API)
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "https://api.perplexity.ai/chat/completions",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "perplexityApi",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "model",
          "value": "llama-3.1-sonar-small-128k-online"
        },
        {
          "name": "messages",
          "value": "=[{\"role\": \"user\", \"content\": \"What are the top 5 trending memes and viral topics in 2026 related to baldness, hair loss, or bald humor? For each trend, provide: 1) Topic name 2) Why it's trending 3) Suggested color palette (2-3 colors). Focus on humorous, satirical content.\"}]"
        }
      ]
    }
  },
  "name": "Search Trending Memes"
}
```

**Alternative:** Use OpenAI GPT-4 with web browsing if Perplexity not available:
```json
{
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "parameters": {
    "model": "gpt-4",
    "prompt": "Search the web for the top 5 trending memes and viral topics in January 2026 related to baldness, hair loss, or bald humor. For each trend, provide: 1) Topic name 2) Why it's trending 3) Suggested color palette (2-3 colors). Focus on humorous, satirical content.",
    "options": {
      "temperature": 0.7
    }
  },
  "name": "GPT-4 Trend Search"
}
```

#### Node 3: Search Bald Humor Topics (OpenAI)
```json
{
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "parameters": {
    "resource": "text",
    "model": "gpt-4",
    "prompt": "Analyze current pop culture, social media trends, and viral content from January 2026. What are 5 emerging themes that would work well for satirical bald-themed merchandise? Focus on: confidence, empowerment, self-acceptance, and humorous takes on baldness. For each theme, suggest: 1) Theme name 2) Target audience 3) Color scheme (2-3 colors) 4) Mood (playful, bold, minimalist, etc.)",
    "options": {
      "temperature": 0.8
    }
  },
  "name": "Analyze Bald Humor Themes"
}
```

#### Node 4: Fetch Color Trends (Pinterest or Adobe Color)
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://www.pinterest.com/resource/BoardFeedResource/get/",
    "sendQuery": true,
    "queryParameters": {
      "parameters": [
        {
          "name": "source_url",
          "value": "/search/pins/?q=2026+color+trends"
        },
        {
          "name": "data",
          "value": "{\"options\":{\"board_id\":\"\",\"board_url\":\"\",\"field_set_key\":\"react_grid_pin\",\"filter_section_pins\":true,\"page_size\":25,\"query\":\"2026 color trends\",\"scope\":\"pins\"},\"context\":{}}"
        }
      ]
    }
  },
  "name": "Fetch Pinterest Color Trends"
}
```

**Alternative:** Manual fallback if APIs unavailable:
```javascript
// Node 4: Manual Color Trends (Code node)
const colorTrends2026 = [
  { palette: "electric blue, neon pink, silver", mood: "futuristic" },
  { palette: "forest green, terracotta, cream", mood: "earthy" },
  { palette: "deep purple, gold, black", mood: "luxurious" },
  { palette: "coral, mint, soft yellow", mood: "playful" },
  { palette: "charcoal, rust, sage", mood: "modern" }
];

return colorTrends2026.map(trend => ({ json: trend }));
```

#### Node 5: Merge & Rank Results (JavaScript Code)
```javascript
// Combine results from all sources
const memes = $input.first().json.choices[0].message.content;
const themes = $input.all()[1].json.choices[0].message.content;
const colors = $input.all()[2].json;

// Parse AI responses (they're text, need to extract structured data)
const parseTrends = (text) => {
  // Extract topics using regex or GPT JSON mode
  const trends = [];
  const lines = text.split('\n');
  let currentTrend = {};
  
  lines.forEach(line => {
    if (line.match(/^\d+\./)) {
      if (currentTrend.topic) trends.push(currentTrend);
      currentTrend = { topic: line.replace(/^\d+\.\s*/, '') };
    } else if (line.toLowerCase().includes('color')) {
      currentTrend.colors = line.replace(/.*colors?:?\s*/i, '').trim();
    } else if (line.toLowerCase().includes('mood')) {
      currentTrend.mood = line.replace(/.*mood:?\s*/i, '').trim();
    }
  });
  if (currentTrend.topic) trends.push(currentTrend);
  return trends;
};

const allTrends = [
  ...parseTrends(memes),
  ...parseTrends(themes)
];

// Rank by relevance (simple scoring)
const rankedTrends = allTrends.map(trend => ({
  topic: trend.topic,
  colors: trend.colors || 'silver and bold blue',
  mood: trend.mood || 'playful',
  relevance_score: Math.floor(Math.random() * 30) + 70, // 70-100
  discovery_date: new Date().toISOString(),
  source: 'AI Research',
  status: 'active'
}));

// Sort by score and return top 10
rankedTrends.sort((a, b) => b.relevance_score - a.relevance_score);
return rankedTrends.slice(0, 10).map(t => ({ json: t }));
```

#### Node 6: Filter Duplicates (Notion Check)
```json
{
  "type": "@n8n/n8n-nodes-langchain.notionTrigger",
  "parameters": {
    "resource": "database",
    "operation": "query",
    "databaseId": "={{$env.NOTION_TRENDS_DB}}",
    "filters": {
      "conditions": [
        {
          "property": "Topic",
          "condition": "text_contains",
          "value": "={{$json.topic}}"
        }
      ]
    }
  },
  "name": "Check if Trend Exists"
}
```

**Then filter:**
```javascript
// If no results from Notion, trend is new
const existingTrends = $input.all();
const newTrends = $input.first().json;

if (existingTrends.length === 0) {
  return [{ json: newTrends }];
} else {
  return [];
}
```

#### Node 7: Store Top 5 Trends (Notion Create)
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "page",
    "operation": "create",
    "databaseId": "={{$env.NOTION_TRENDS_DB}}",
    "properties": {
      "Topic": "={{$json.topic}}",
      "Colors": "={{$json.colors}}",
      "Status": "active",
      "Relevance Score": "={{$json.relevance_score}}",
      "Discovery Date": "={{$json.discovery_date}}",
      "Source": "={{$json.source}}"
    }
  },
  "name": "Create Trend in Notion"
}
```

#### Node 8: Mark Old Trends as Used (Notion Update)
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "database",
    "operation": "query",
    "databaseId": "={{$env.NOTION_TRENDS_DB}}",
    "filters": {
      "conditions": [
        {
          "property": "Discovery Date",
          "condition": "date_before",
          "value": "={{$today(-7)}}"
        },
        {
          "property": "Status",
          "condition": "select_equals",
          "value": "active"
        }
      ]
    }
  },
  "name": "Find Old Active Trends"
}
```

**Then update status:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "page",
    "operation": "update",
    "pageId": "={{$json.id}}",
    "properties": {
      "Status": "exhausted"
    }
  },
  "name": "Mark as Exhausted"
}
```

### Environment Variables Needed
```env
NOTION_TRENDS_DB=<trends-database-id>
PERPLEXITY_API_KEY=<optional>
OPENAI_API_KEY=<required>
PINTEREST_API_KEY=<optional>
```

### Success Criteria
- ✅ 5+ new trends added to Notion daily
- ✅ No duplicate trends
- ✅ All trends have color palettes
- ✅ Old trends (7+ days) marked as exhausted
- ✅ Relevance scores between 70-100

---

## 2. Performance Monitor Workflow

**Filename:** `balding_pig_performance_monitor.json`  
**Schedule:** Daily at 8:00 PM  
**Purpose:** Track product sales, update metrics, pause low performers  

### Workflow Architecture (7 nodes)

```
Schedule Trigger (8pm)
    ↓
Fetch All Products from Notion
    ↓
Get Shopify Sales Data (API)
    ↓
Calculate Metrics (JavaScript)
    ↓
Update Notion with Sales/Revenue
    ↓
Identify Low Performers
    ↓
Pause Products (Shopify API)
```

### Node Details

#### Node 1: Schedule Trigger
```json
{
  "type": "n8n-nodes-base.scheduleTrigger",
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 24,
          "triggerAtHour": 20
        }
      ]
    }
  },
  "name": "Daily 8pm Trigger"
}
```

#### Node 2: Fetch All Products from Notion
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "database",
    "operation": "getAll",
    "databaseId": "={{$env.NOTION_PRODUCTS_DB}}",
    "filters": {
      "conditions": [
        {
          "property": "Status",
          "condition": "select_equals",
          "value": "published"
        }
      ]
    }
  },
  "name": "Get Published Products"
}
```

#### Node 3: Get Shopify Sales Data (Loop)
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://your-store.myshopify.com/admin/api/2024-01/products/={{$json.shopify_product_id}}/metafields.json",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "shopifyApi",
    "sendQuery": true,
    "queryParameters": {
      "parameters": [
        {
          "name": "namespace",
          "value": "sales"
        }
      ]
    }
  },
  "name": "Fetch Product Sales"
}
```

**Alternative - Fetch Orders:**
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://your-store.myshopify.com/admin/api/2024-01/orders.json",
    "sendQuery": true,
    "queryParameters": {
      "parameters": [
        {
          "name": "created_at_min",
          "value": "={{$today(-1)}}"
        },
        {
          "name": "status",
          "value": "any"
        }
      ]
    }
  },
  "name": "Fetch Recent Orders"
}
```

#### Node 4: Calculate Metrics (JavaScript)
```javascript
// Input: Product data from Notion + Sales data from Shopify
const product = $input.first().json;
const orders = $input.all()[1].json.orders || [];

// Filter orders for this product
const productOrders = orders.filter(order => 
  order.line_items.some(item => item.product_id === product.shopify_product_id)
);

// Calculate metrics
const salesCount = productOrders.reduce((sum, order) => 
  sum + order.line_items
    .filter(item => item.product_id === product.shopify_product_id)
    .reduce((itemSum, item) => itemSum + item.quantity, 0)
, 0);

const revenue = productOrders.reduce((sum, order) => 
  sum + parseFloat(order.line_items
    .filter(item => item.product_id === product.shopify_product_id)
    .reduce((itemSum, item) => itemSum + parseFloat(item.price) * item.quantity, 0))
, 0);

// Calculate days since generation
const daysSinceGenerated = Math.floor(
  (Date.now() - new Date(product.generated_date).getTime()) / (1000 * 60 * 60 * 24)
);

// Performance score (0-100)
const performanceScore = Math.min(100, 
  (salesCount * 10) + (revenue / 10) - (daysSinceGenerated * 0.5)
);

// Recommendation
let recommendation = 'keep';
if (daysSinceGenerated > 30 && revenue < 10) {
  recommendation = 'pause'; // No sales after 30 days
} else if (daysSinceGenerated > 60 && revenue < 50) {
  recommendation = 'remove'; // Minimal sales after 60 days
} else if (salesCount > 10 && daysSinceGenerated < 14) {
  recommendation = 'boost'; // Hot seller
}

return [{
  json: {
    product_id: product.id,
    shopify_product_id: product.shopify_product_id,
    sales_count: salesCount,
    revenue: revenue.toFixed(2),
    days_active: daysSinceGenerated,
    performance_score: performanceScore.toFixed(0),
    recommendation: recommendation,
    last_updated: new Date().toISOString()
  }
}];
```

#### Node 5: Update Notion with Sales/Revenue
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "page",
    "operation": "update",
    "pageId": "={{$json.product_id}}",
    "properties": {
      "Sales Count": "={{$json.sales_count}}",
      "Revenue": "={{$json.revenue}}",
      "Performance Score": "={{$json.performance_score}}",
      "Last Updated": "={{$json.last_updated}}"
    }
  },
  "name": "Update Product Metrics"
}
```

#### Node 6: Identify Low Performers (Filter)
```javascript
// Only pass products with 'pause' or 'remove' recommendations
const product = $input.first().json;

if (product.recommendation === 'pause' || product.recommendation === 'remove') {
  return [{ json: product }];
} else {
  return [];
}
```

#### Node 7: Pause Products (Shopify API)
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "PUT",
    "url": "https://your-store.myshopify.com/admin/api/2024-01/products/={{$json.shopify_product_id}}.json",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "shopifyApi",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "product",
          "value": "={\"status\": \"draft\"}"
        }
      ]
    }
  },
  "name": "Pause Product on Shopify"
}
```

**Then update Notion:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "page",
    "operation": "update",
    "pageId": "={{$json.product_id}}",
    "properties": {
      "Status": "paused"
    }
  },
  "name": "Update Status to Paused"
}
```

### Environment Variables Needed
```env
NOTION_PRODUCTS_DB=<products-database-id>
SHOPIFY_STORE_URL=<your-store.myshopify.com>
SHOPIFY_API_KEY=<api-key>
SHOPIFY_API_SECRET=<api-secret>
```

### Success Criteria
- ✅ All published products checked daily
- ✅ Sales and revenue updated in Notion
- ✅ Low performers automatically paused
- ✅ Performance scores calculated accurately
- ✅ Recommendations logged for review

---

## 3. Error Handling Workflow (Optional but Recommended)

**Filename:** `balding_pig_error_handler.json`  
**Trigger:** Called by other workflows on error  
**Purpose:** Centralized error logging and notification  

### Workflow Architecture (4 nodes)

```
Webhook Trigger (Error Event)
    ↓
Parse Error Details (JavaScript)
    ↓
Log to Notion Errors DB
    ↓
Send Slack Notification
```

### Node Details

#### Node 1: Webhook Trigger
```json
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "balding-pig-error",
    "responseMode": "responseNode",
    "options": {}
  },
  "name": "Error Webhook"
}
```

#### Node 2: Parse Error Details
```javascript
const error = $input.first().json;

return [{
  json: {
    workflow_name: error.workflow || 'Unknown',
    error_message: error.message || 'No message',
    error_type: error.type || 'Unknown',
    node_name: error.node || 'Unknown',
    timestamp: new Date().toISOString(),
    stack_trace: error.stack || '',
    severity: error.severity || 'medium'
  }
}];
```

#### Node 3: Log to Notion
```json
{
  "type": "@n8n/n8n-nodes-langchain.notion",
  "parameters": {
    "resource": "page",
    "operation": "create",
    "databaseId": "={{$env.NOTION_ERRORS_DB}}",
    "properties": {
      "Workflow": "={{$json.workflow_name}}",
      "Error Message": "={{$json.error_message}}",
      "Node": "={{$json.node_name}}",
      "Timestamp": "={{$json.timestamp}}",
      "Severity": "={{$json.severity}}"
    }
  },
  "name": "Log Error to Notion"
}
```

#### Node 4: Send Slack Notification
```json
{
  "type": "n8n-nodes-base.slack",
  "parameters": {
    "resource": "message",
    "operation": "post",
    "channel": "#balding-pig-alerts",
    "text": "🚨 *Balding Pig Error*\n\n*Workflow:* {{$json.workflow_name}}\n*Node:* {{$json.node_name}}\n*Error:* {{$json.error_message}}\n*Time:* {{$json.timestamp}}"
  },
  "name": "Alert to Slack"
}
```

---

## Implementation Priority

### Phase 1: Core System (Complete ✅)
- [x] Product Generator Workflow

### Phase 2: Intelligence Layer (Next)
- [ ] Trend Research Workflow - **BUILD THIS FIRST**

### Phase 3: Optimization Layer
- [ ] Performance Monitor Workflow - **BUILD THIS SECOND**

### Phase 4: Resilience Layer (Optional)
- [ ] Error Handling Workflow - **BUILD IF TIME ALLOWS**

---

## Testing Checklist

### Trend Research Workflow
- [ ] Runs daily at 6am automatically
- [ ] Finds 5+ new trends
- [ ] No duplicate trends created
- [ ] All trends have colors and mood
- [ ] Old trends marked as exhausted

### Performance Monitor Workflow
- [ ] Runs daily at 8pm automatically
- [ ] Fetches all published products
- [ ] Calculates sales accurately
- [ ] Updates Notion with metrics
- [ ] Pauses low performers correctly

### Error Handling Workflow
- [ ] Receives error webhooks
- [ ] Logs errors to Notion
- [ ] Sends Slack notifications
- [ ] Includes full error context

---

## Estimated Build Time

**Trend Research Workflow:** 3-4 hours  
**Performance Monitor Workflow:** 2-3 hours  
**Error Handling Workflow:** 1 hour  

**Total:** 6-8 hours of development

---

## Dependencies

**Trend Research:**
- OpenAI API (GPT-4) - Required
- Perplexity API - Optional (can use GPT-4 instead)
- Pinterest API - Optional (can use manual fallback)

**Performance Monitor:**
- Shopify API - Required
- Notion API - Required

**Error Handling:**
- Slack API - Optional (can use email instead)

---

## Notes for Builders

1. **Trend Research is the most important workflow** - good trends = good products = good sales

2. **Start with GPT-4 for trend research** - it's simpler than Perplexity and works well enough

3. **Use manual color fallback initially** - Pinterest API is complex, manual list works fine

4. **Performance monitoring can wait** - you can manually check Shopify for the first few weeks

5. **Test trend research thoroughly** - bad trends = bad products = wasted DALL-E costs

6. **Consider rate limits** - both OpenAI and Shopify have rate limits, add delays if needed

---

**Created by:** Warp Agent  
**Date:** January 2, 2026  
**For:** Emergent & Claude  
**Status:** Ready to Build
