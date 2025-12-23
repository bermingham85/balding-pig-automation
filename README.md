# The Balding Pig Automation

Complete automation system for The Balding Pig product generation and management.

## Overview
Comprehensive automation platform integrating Printify, Notion, Perplexity, and n8n workflows for automated product design, listing, and management. Built for "The Balding Pig" print-on-demand business.

## Features
- **Product Generation**: Automated design and product creation
- **Printify Integration**: Direct product listing and management
- **Notion Database**: Product tracking and inventory management
- **Perplexity AI**: Enhanced content generation and research
- **n8n Workflows**: Complete workflow automation
- **Web Interface**: HTML control panel for system management
- **Database Management**: Schema management and updates

## Tech Stack
- Python 3.x
- JavaScript/Node.js
- n8n workflow automation
- Notion API
- Printify API
- Perplexity API
- PowerShell deployment scripts

## Getting Started

### Prerequisites
- Python 3.7+
- Node.js (for n8n)
- Notion workspace and API key
- Printify account and API key
- Perplexity API access
- n8n instance (configured at http://192.168.50.246:5678)

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Deploy the system (Windows)
.\scripts\deploy_balding_pig_system.ps1

# Or use simplified deployment
.\scripts\deploy_simple.ps1
```

### Configuration
1. Set up environment variables in `.env`:
   - Notion API key and database IDs
   - Printify API credentials
   - Perplexity API key
   - n8n endpoint

2. Configure business settings in `configs/business_config.json`

3. Load Notion schema: `python setup/update-database.py`

## Project Structure
```
balding-pig-automation/
├── configs/              # Configuration files
│   └── business_config.json
├── docs/                 # Documentation
│   ├── PROJECT_OVERVIEW.md
│   └── IMPORT_GUIDE.md
├── scripts/              # Automation scripts
│   ├── deploy_balding_pig_system.ps1
│   ├── deploy_simple.ps1
│   └── claude_work_logger.ps1
├── workflows/            # n8n workflow definitions
│   ├── balding_pig_*.json
│   └── various automation workflows
├── setup/                # Setup and configuration scripts
│   ├── printify_setup.py
│   ├── notion_db_check.py
│   ├── update-database.py
│   ├── enhanced_server_endpoint.py
│   ├── perplexity_enhanced_service.py
│   └── env-loader.py
└── README.md             # This file
```

## Key Components

### Printify Setup (`setup/printify_setup.py`)
Initialize and configure Printify product templates and listings.

### Notion Integration (`setup/notion_db_check.py`)
Verify and manage Notion database connections and schemas.

### Perplexity Service (`setup/perplexity_enhanced_service.py`)
Enhanced AI-powered content generation and research.

### n8n Workflows (`workflows/`)
Complete automation workflows for:
- Product generation
- Design automation
- Inventory management
- Listing updates
- Order processing

### Web Interface (`setup/html_interface.html`)
Browser-based control panel for system management.

## Workflows
Import n8n workflows from the `workflows/` directory:
- `balding_pig_product_generator.json` - Main product pipeline
- `balding_pig_design_automation.json` - Design generation
- Additional supporting workflows

## Documentation
- `docs/PROJECT_OVERVIEW.md` - Complete project documentation
- `docs/IMPORT_GUIDE.md` - Workflow import instructions
- `setup/Priority Setup Plan.pdf` - Setup priority guide

## Deployment
The system is designed for deployment to:
- Local development environment
- QNAP NAS (network storage integration)
- n8n instance at http://192.168.50.246:5678

## Environment Variables
Required environment variables (see `setup/*.env` files):
- `NOTION_API_KEY` - Notion integration token
- `NOTION_DATABASE_ID` - Product database ID
- `PRINTIFY_API_KEY` - Printify API token
- `PERPLEXITY_API_KEY` - Perplexity API key
- `N8N_ENDPOINT` - n8n webhook endpoint

## License
MIT
