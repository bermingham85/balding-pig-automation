# Add this new endpoint to your server.py file

@app.route('/generate-enhanced', methods=['POST'])
def generate_enhanced():
    """Generate trend-aware product ideas using Perplexity research."""
    try:
        data = request.json
        user_prompt = data.get('prompt', '')
        
        if not user_prompt:
            return jsonify({'success': False, 'message': 'Prompt is required.'}), 400
        
        # Log the incoming request
        logger.info(f"Received enhanced generation request: {user_prompt}")
        
        # Create a new UserPrompt record
        new_user_prompt = UserPrompt(prompt_text=user_prompt)
        db.session.add(new_user_prompt)
        db.session.commit()
        logger.info(f"Saved user prompt to database with ID: {new_user_prompt.id}")
        
        # Step 1: Generate enhanced product ideas with trend research
        logger.info("Generating enhanced product ideas with trend research...")
        product_ideas = EnhancedGoAPIService.generate_enhanced_product_ideas(user_prompt)
        
        # Create a response with all product details
        response_data = []
        
        for product_data in product_ideas:
            # Save the product to the database with enhanced fields
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                tagline=product_data['tagline'],
                design_style=product_data['design_style'],
                colours=product_data['colours'],
                keywords=product_data['keywords'],
                ai_prompt=product_data['ai_prompt'],
                printify_status="Pending"
            )
            
            db.session.add(product)
            new_user_prompt.products.append(product)
            db.session.commit()
            
            logger.info(f"Saved enhanced product to database with ID: {product.id}")
            
            # Create product data with additional trend information
            enhanced_product = product_data.copy()
            enhanced_product['db_id'] = product.id
            
            response_data.append(enhanced_product)
        
        return jsonify({
            'success': True,
            'message': 'Successfully generated trend-aware product ideas!',
            'products': response_data,
            'enhancement': 'trend-research'
        })
        
    except Exception as e:
        logger.error(f"Error in enhanced generate endpoint: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/products/<int:product_id>/analyze', methods=['POST'])
def analyze_product_potential(product_id):
    """Analyze market potential of a specific product using Perplexity."""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        logger.info(f"Analyzing market potential for product: {product.name}")
        
        # Prepare product data for analysis
        product_data = {
            'name': product.name,
            'description': product.description,
            'design_style': product.design_style,
            'keywords': product.keywords
        }
        
        # Analyze with Perplexity
        analysis_result = EnhancedGoAPIService.analyze_product_potential(product_data)
        
        if analysis_result.get('success'):
            return jsonify({
                'success': True,
                'product_id': product_id,
                'analysis': analysis_result['analysis'],
                'citations': analysis_result.get('citations', [])
            })
        else:
            return jsonify({
                'success': False,
                'message': f"Analysis failed: {analysis_result.get('message')}"
            }), 500
        
    except Exception as e:
        logger.error(f"Error analyzing product potential: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/trends/research', methods=['POST'])
def research_trends():
    """Research current trends for a given topic using Perplexity."""
    try:
        data = request.json
        topic = data.get('topic', '')
        
        if not topic:
            return jsonify({'success': False, 'message': 'Topic is required.'}), 400
        
        logger.info(f"Researching trends for topic: {topic}")
        
        # Research trends with Perplexity
        trend_result = EnhancedGoAPIService.research_trends_with_perplexity(topic)
        
        if trend_result.get('success'):
            return jsonify({
                'success': True,
                'topic': topic,
                'research': trend_result['research'],
                'citations': trend_result.get('citations', [])
            })
        else:
            return jsonify({
                'success': False,
                'message': f"Trend research failed: {trend_result.get('message')}"
            }), 500
        
    except Exception as e:
        logger.error(f"Error researching trends: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500