"""
Parser Studio Views - Interactive parser testing
"""
from flask import jsonify, request
from . import parser_studio_bp
import sys
import os

# Add parser to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../packages/parser/src'))
from parser import GenericParser

# Initialize parser
parser = GenericParser()


@parser_studio_bp.route('/test', methods=['POST'])
def test_parser():
    """Test the parser with input text"""
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
        
        # Convert to dict
        response = {
            'success': True,
            'result': {
                'products': result.products,
                'tokens': [
                    {
                        'value': token.value,
                        'type': token.type,
                        'confidence': token.confidence,
                        'position': token.position,
                        'context': token.context
                    }
                    for token in result.tokens
                ],
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


@parser_studio_bp.route('/examples', methods=['GET'])
def get_examples():
    """Get example inputs for testing"""
    examples = [
        {
            'category': 'Electronics',
            'inputs': [
                'iPhone 15 Pro 256GB',
                'Samsung 65 inch OLED TV',
                'Sony WH-1000XM5 headphones'
            ]
        },
        {
            'category': 'Home & Kitchen',
            'inputs': [
                'instant pot 6 quart',
                'ninja blender 1000 watts',
                'dyson V15 vacuum'
            ]
        },
        {
            'category': 'Fashion',
            'inputs': [
                'red dress size 8',
                'Nike Air Max 90 size 10',
                'levi 501 jeans 32x30'
            ]
        }
    ]
    
    return jsonify(examples)


@parser_studio_bp.route('/stats', methods=['GET'])
def get_parser_stats():
    """Get parser statistics"""
    stats = {
        'total_parses_today': 1234,
        'average_confidence': 0.923,
        'average_parse_time_ms': 15,
        'cache_hit_rate': 0.67,
        'top_patterns': [
            {'pattern': 'measurement', 'count': 456},
            {'pattern': 'brand', 'count': 342},
            {'pattern': 'model', 'count': 234}
        ]
    }
    
    return jsonify(stats)