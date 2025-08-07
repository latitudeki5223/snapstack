"""
SnapStack Backend API
Flask application with admin interface
"""
from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Register admin blueprint
from admin import admin_bp
app.register_blueprint(admin_bp)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    from flask import jsonify
    return jsonify({'status': 'healthy', 'service': 'snapstack-backend'})


# Old endpoints kept for compatibility
@app.route('/api/admin/parser/test', methods=['POST'])
def test_parser():
    """
    Test the generic parser with input text
    
    Request body:
    {
        "text": "iPhone 15 Pro 256GB"
    }
    
    Returns:
    {
        "success": true,
        "result": {
            "products": [...],
            "tokens": [...],
            "confidence": 0.95,
            "parser_used": "generic"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "text" field in request body'
            }), 400
        
        text = data['text']
        
        # Parse the text
        result = parser.parse(text)
        
        # Convert dataclass to dict
        response = {
            'success': True,
            'result': {
                'products': result.products,
                'tokens': [asdict(token) for token in result.tokens],
                'confidence': result.confidence,
                'parser_used': result.parser_used,
                'raw_text': result.raw_text
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/parser/examples', methods=['GET'])
def get_examples():
    """Get example inputs for testing"""
    examples = [
        {
            'category': 'Electronics',
            'inputs': [
                'iPhone 15 Pro 256GB',
                'Samsung 65 inch OLED TV',
                'Sony WH-1000XM5 headphones',
                'MacBook Pro 16" M3 Max'
            ]
        },
        {
            'category': 'Home & Kitchen',
            'inputs': [
                'instant pot 6 quart',
                'ninja blender 1000 watts',
                'dyson V15 vacuum',
                'nespresso vertuo coffee maker'
            ]
        },
        {
            'category': 'Fashion',
            'inputs': [
                'red dress size 8',
                'Nike Air Max 90 size 10',
                'levi 501 jeans 32x30',
                'canada goose parka medium'
            ]
        },
        {
            'category': 'Toys & Games',
            'inputs': [
                'lego star wars millennium falcon',
                'monopoly board game',
                'barbie dreamhouse',
                'nintendo switch oled'
            ]
        },
        {
            'category': 'Grocery & Food',
            'inputs': [
                'organic honey 32oz',
                'KIND bars variety pack 12 count',
                'starbucks pike place coffee k-cups',
                'sriracha hot sauce 17oz'
            ]
        },
        {
            'category': 'Random/Ambiguous',
            'inputs': [
                'that thing from tiktok',
                'the pink stuff cleaner',
                'as seen on tv gadget',
                'unicorn onesie adult medium'
            ]
        },
        {
            'category': 'Books & Media',
            'inputs': [
                '"Atomic Habits" by James Clear',
                'harry potter complete collection',
                'taylor swift vinyl',
                'the office complete series dvd'
            ]
        },
        {
            'category': 'Tools & Hardware',
            'inputs': [
                'dewalt 20v drill',
                'craftsman 200 piece tool set',
                'gorilla glue 4oz',
                '3M command strips large'
            ]
        }
    ]
    
    return jsonify(examples)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)