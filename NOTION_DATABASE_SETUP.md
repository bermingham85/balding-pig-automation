# 📊 Balding Pig V2 - Notion Database Setup

**Date:** January 2, 2026  
**Status:** Complete Setup Instructions  

---

## Overview

The Balding Pig V2 system requires **3 Notion databases** (2 required, 1 optional):

1. ✅ **Trends Database** (REQUIRED) - Stores trending topics for product generation
2. ✅ **Products Database** (REQUIRED) - Tracks all generated products
3. ⚠️ **Errors Database** (OPTIONAL) - Logs workflow errors

---

## Setup Instructions

### Step 1: Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Name: `Balding Pig V2`
4. Associated workspace: Select your workspace
5. Type: **Internal**
6. Capabilities: 
   - ✅ Read content
   - ✅ Update content
   - ✅ Insert content
7. Click **"Submit"**
8. Copy the **Integration Token** (starts with `secret_...`)
9. Save this token - you'll need it for n8n

### Step 2: Create Databases

Create 3 new databases in Notion (one for each below). After creating each database, **share it with your integration**:

1. Open the database
2. Click **"..."** in top right
3. Click **"Add connections"**
4. Select **"Balding Pig V2"** integration

---

## 1. Trends Database

**Database Name:** `Balding Pig - Trends`

### Properties (8 total)

| Property Name | Type | Configuration | Description |
|--------------|------|---------------|-------------|
| **Topic** | Title | - | The trend topic (e.g., "Retro Futurism") |
| **Colors** | Text | - | Color palette (e.g., "neon pink, electric blue") |
| **Status** | Select | Options: `active`, `used`, `exhausted` | Current status of trend |
| **Relevance Score** | Number | Format: Number | Score from 0-100 |
| **Discovery Date** | Date | - | When trend was discovered |
| **Source** | Text | - | Where trend came from (e.g., "AI Research") |
| **Times Used** | Number | Format: Number | How many products used this trend |
| **Last Used** | Date | - | Last time trend was used |

### Select Options (Status property)

- 🟢 **active** - Ready to use
- 🟡 **used** - Has been used, still available
- 🔴 **exhausted** - Too old, should not be used

### Sample Data

Add these test trends to verify setup:

| Topic | Colors | Status | Relevance Score | Discovery Date | Source |
|-------|--------|--------|-----------------|----------------|--------|
| Retro Futurism | neon pink, electric blue | active | 95 | Today | Manual |
| Minimalist Zen | charcoal, cream, sage | active | 88 | Today | Manual |
| Pop Art Revival | red, yellow, black | active | 92 | Today | Manual |
| Cyberpunk Aesthetics | purple, cyan, silver | active | 90 | Today | Manual |
| Vintage 80s | coral, teal, gold | active | 85 | Today | Manual |

### Getting Database ID

1. Open the database in Notion
2. Look at URL: `https://www.notion.so/[DATABASE_ID]?v=...`
3. Copy the DATABASE_ID (32 characters)
4. Add to n8n environment: `NOTION_TRENDS_DB=<database-id>`

---

## 2. Products Database

**Database Name:** `Balding Pig - Products`

### Properties (14 total)

| Property Name | Type | Configuration | Description |
|--------------|------|---------------|-------------|
| **Name** | Title | - | Product name (e.g., "Chrome Dome Retro Edition") |
| **Category** | Select | Options: `t-shirt`, `hoodie`, `mug`, `tote-bag`, `poster` | Product type |
| **Trend Topic** | Text | - | Source trend used |
| **Shopify URL** | URL | - | Link to product on Shopify |
| **Status** | Select | Options: `draft`, `published`, `paused` | Current status |
| **Generated Date** | Date | Include time: Yes | When product was created |
| **Quality Score** | Number | Format: Number | Image quality score (0-100) |
| **Sales Count** | Number | Format: Number | Total units sold |
| **Revenue** | Number | Format: Dollar ($) | Total revenue earned |
| **Performance Score** | Number | Format: Number | Overall performance (0-100) |
| **Last Updated** | Date | Include time: Yes | Last metrics update |
| **Image URL** | URL | - | DALL-E generated image |
| **Printful Product ID** | Text | - | Printful product ID |
| **Shopify Product ID** | Text | - | Shopify product ID |

### Select Options

**Category:**
- 👕 t-shirt
- 🧥 hoodie
- ☕ mug
- 🛍️ tote-bag
- 🖼️ poster

**Status:**
- 📝 draft - Created, not published
- ✅ published - Live on store
- ⏸️ paused - Temporarily hidden

### Sample Data

Add one test product to verify setup:

| Name | Category | Trend Topic | Status | Generated Date | Quality Score |
|------|----------|-------------|--------|----------------|---------------|
| Test Product - Chrome Dome | t-shirt | Retro Futurism | draft | Today | 85 |

### Getting Database ID

1. Open the database in Notion
2. Look at URL: `https://www.notion.so/[DATABASE_ID]?v=...`
3. Copy the DATABASE_ID (32 characters)
4. Add to n8n environment: `NOTION_PRODUCTS_DB=<database-id>`

---

## 3. Errors Database (Optional)

**Database Name:** `Balding Pig - Errors`

### Properties (7 total)

| Property Name | Type | Configuration | Description |
|--------------|------|---------------|-------------|
| **Error Message** | Title | - | Brief error description |
| **Workflow** | Select | Options: `Product Generator`, `Trend Research`, `Performance Monitor` | Which workflow failed |
| **Node** | Text | - | Which node in workflow failed |
| **Timestamp** | Date | Include time: Yes | When error occurred |
| **Severity** | Select | Options: `low`, `medium`, `high`, `critical` | Error severity |
| **Stack Trace** | Text | - | Full error details |
| **Resolved** | Checkbox | - | Has error been fixed |

### Select Options

**Workflow:**
- 🏭 Product Generator
- 🔍 Trend Research
- 📊 Performance Monitor
- ⚙️ Other

**Severity:**
- 🟢 low - Minor issue
- 🟡 medium - Needs attention
- 🟠 high - Important
- 🔴 critical - System down

### Getting Database ID

1. Open the database in Notion
2. Look at URL: `https://www.notion.so/[DATABASE_ID]?v=...`
3. Copy the DATABASE_ID (32 characters)
4. Add to n8n environment: `NOTION_ERRORS_DB=<database-id>`

---

## Database Views (Recommended)

### Trends Database Views

**View 1: Active Trends** (Default)
- Filter: `Status = active`
- Sort: `Relevance Score` (descending)
- Shows only trends ready to use

**View 2: All Trends**
- No filters
- Sort: `Discovery Date` (descending)
- Shows complete history

**View 3: Exhausted**
- Filter: `Status = exhausted`
- Sort: `Last Used` (descending)
- Shows old trends

### Products Database Views

**View 1: Published** (Default)
- Filter: `Status = published`
- Sort: `Generated Date` (descending)
- Shows live products

**View 2: Performance**
- Filter: `Status = published`
- Sort: `Performance Score` (descending)
- Shows best/worst performers

**View 3: Revenue**
- Filter: `Status = published`
- Sort: `Revenue` (descending)
- Shows top earners

**View 4: All Products**
- No filters
- Sort: `Generated Date` (descending)
- Complete product catalog

### Errors Database Views

**View 1: Unresolved** (Default)
- Filter: `Resolved = unchecked`
- Sort: `Timestamp` (descending)
- Shows active issues

**View 2: Critical**
- Filter: `Severity = critical` AND `Resolved = unchecked`
- Sort: `Timestamp` (descending)
- Shows urgent issues

---

## Environment Variables Summary

After creating all databases, add these to your n8n instance:

```env
# Notion API
NOTION_API_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Database IDs
NOTION_TRENDS_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_PRODUCTS_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_ERRORS_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Where to add in n8n:

1. Open n8n: http://192.168.50.246:5678
2. Go to **Settings** → **Credentials**
3. Click **"Add Credential"**
4. Choose **"Notion API"**
5. Paste your **Integration Token**
6. Save as **"Balding Pig Notion"**

For environment variables:

1. If using Docker: Add to `docker-compose.yml` or `.env` file
2. If using npm: Add to `.env` file in n8n directory
3. If using cloud: Add in environment settings

---

## Testing Database Setup

### Test 1: Notion API Connection

1. Open n8n workflow editor
2. Add a **Notion** node
3. Choose **"Get Database"** operation
4. Select credential **"Balding Pig Notion"**
5. Paste Trends Database ID
6. Execute node
7. ✅ Should return database schema

### Test 2: Create Trend

1. Add **Notion** node
2. Choose **"Create Page"** operation
3. Database: Trends Database ID
4. Set properties:
   - Topic: "Test Trend"
   - Colors: "red, blue"
   - Status: "active"
   - Relevance Score: 75
5. Execute node
6. ✅ Check Notion - new trend should appear

### Test 3: Query Trends

1. Add **Notion** node
2. Choose **"Query Database"** operation
3. Database: Trends Database ID
4. Filter: `Status = active`
5. Execute node
6. ✅ Should return all active trends

---

## Database Maintenance

### Daily
- Trend Research workflow adds new trends
- Product Generator workflow creates products
- Performance Monitor updates sales data

### Weekly
- Review exhausted trends (delete if >30 days old)
- Check for duplicate trends
- Verify all products have Shopify URLs

### Monthly
- Archive paused products (no sales >60 days)
- Analyze trend performance (which trends sold best?)
- Clean up error logs

---

## Formulas (Advanced)

If you want to add calculated properties:

### Products Database

**Days Active** (Number formula):
```
dateBetween(now(), prop("Generated Date"), "days")
```

**Revenue Per Day** (Number formula):
```
if(prop("Days Active") > 0, prop("Revenue") / prop("Days Active"), 0)
```

**Conversion Rate** (Number formula):
```
if(prop("Sales Count") > 0, prop("Sales Count") / prop("Days Active") * 100, 0)
```

### Trends Database

**Days Since Discovery** (Number formula):
```
dateBetween(now(), prop("Discovery Date"), "days")
```

**Usage Rate** (Number formula):
```
if(prop("Times Used") > 0, prop("Times Used") / dateBetween(now(), prop("Discovery Date"), "days"), 0)
```

---

## Troubleshooting

### Error: "Database not found"

**Cause:** Integration not connected to database  
**Fix:** 
1. Open database in Notion
2. Click "..." → "Add connections"
3. Select "Balding Pig V2" integration

### Error: "Insufficient permissions"

**Cause:** Integration lacks required permissions  
**Fix:**
1. Go to https://www.notion.so/my-integrations
2. Edit "Balding Pig V2" integration
3. Enable all capabilities (Read, Update, Insert)
4. Update in workspace

### Error: "Property not found"

**Cause:** Property name mismatch  
**Fix:**
1. Check property names in Notion (case-sensitive)
2. Update workflow to match exact names
3. Ensure property types match (Text, Number, etc.)

### Workflow can't find trends

**Cause:** No active trends in database  
**Fix:**
1. Add sample trends from this document
2. Ensure Status = "active"
3. Set Relevance Score > 70

---

## Quick Setup Checklist

- [ ] Create Notion integration at https://www.notion.so/my-integrations
- [ ] Copy integration token
- [ ] Create "Balding Pig - Trends" database with 8 properties
- [ ] Create "Balding Pig - Products" database with 14 properties
- [ ] Create "Balding Pig - Errors" database with 7 properties (optional)
- [ ] Share all databases with integration
- [ ] Copy all 3 database IDs
- [ ] Add Notion credential to n8n
- [ ] Add environment variables to n8n
- [ ] Add 5 sample trends to Trends database
- [ ] Add 1 test product to Products database
- [ ] Test Notion API connection in n8n
- [ ] Run test query to fetch active trends
- [ ] Verify product generator workflow can access databases

---

## Database URLs for Reference

After setup, bookmark these URLs:

```
Trends Database:
https://www.notion.so/[YOUR_TRENDS_DB_ID]

Products Database:
https://www.notion.so/[YOUR_PRODUCTS_DB_ID]

Errors Database:
https://www.notion.so/[YOUR_ERRORS_DB_ID]
```

---

**Created by:** Warp Agent  
**Date:** January 2, 2026  
**For:** Emergent & Claude  
**Status:** Complete Setup Guide
