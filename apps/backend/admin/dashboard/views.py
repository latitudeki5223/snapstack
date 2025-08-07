"""
Admin Dashboard Views - Main business metrics and overview
"""
from flask import jsonify
from datetime import datetime, timedelta
from . import dashboard_bp
import random  # For demo data


@dashboard_bp.route('/metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get main dashboard metrics"""
    
    # Generate demo metrics (replace with real data later)
    metrics = {
        'gmv': round(random.uniform(10000, 50000), 2),
        'revenue': round(random.uniform(300, 1500), 2),
        'active_users': random.randint(100, 1000),
        'parse_accuracy': round(random.uniform(0.85, 0.99), 3),
        'api_health_score': round(random.uniform(0.9, 1.0), 3),
        'conversion_rate': round(random.uniform(0.01, 0.05), 3),
        'total_searches_today': random.randint(500, 5000),
        'total_products_parsed': random.randint(1000, 10000),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(metrics)


@dashboard_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get system alerts"""
    
    alerts = [
        {
            'id': 'alert_001',
            'type': 'warning',
            'message': 'Parser accuracy below 95% threshold',
            'timestamp': datetime.now().isoformat(),
            'severity': 'medium'
        },
        {
            'id': 'alert_002',
            'type': 'info',
            'message': 'New parser patterns added successfully',
            'timestamp': (datetime.now() - timedelta(hours=1)).isoformat(),
            'severity': 'low'
        }
    ]
    
    return jsonify(alerts)


@dashboard_bp.route('/trending', methods=['GET'])
def get_trending_products():
    """Get trending products"""
    
    products = [
        {'name': 'iPhone 15 Pro', 'searches': 342, 'conversion': 0.023},
        {'name': 'Stanley Tumbler', 'searches': 287, 'conversion': 0.031},
        {'name': 'Dyson V15', 'searches': 198, 'conversion': 0.018},
        {'name': 'Nike Air Max', 'searches': 156, 'conversion': 0.027},
        {'name': 'Instant Pot', 'searches': 134, 'conversion': 0.035}
    ]
    
    return jsonify(products)


@dashboard_bp.route('/chart-data', methods=['GET'])
def get_chart_data():
    """Get data for charts"""
    
    # Generate hourly data for last 24 hours
    chart_data = []
    now = datetime.now()
    
    for i in range(24):
        hour_time = now - timedelta(hours=23-i)
        chart_data.append({
            'hour': hour_time.strftime('%H:00'),
            'searches': random.randint(50, 500),
            'conversions': random.randint(1, 20),
            'revenue': round(random.uniform(10, 200), 2)
        })
    
    return jsonify(chart_data)