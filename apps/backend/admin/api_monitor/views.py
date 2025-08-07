"""
API Monitor - Real-time vendor API monitoring and cost tracking
Critical for maintaining service reliability and managing costs
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import time
import asyncio


@dataclass
class VendorStatus:
    """Status of a vendor API"""
    name: str
    status: str  # 'healthy', 'degraded', 'down'
    response_time_ms: float
    success_rate: float
    rate_limit_remaining: int
    rate_limit_reset: str
    last_error: Optional[str]
    cost_today: float
    calls_today: int


class APIMonitor:
    """
    Real-time vendor API monitoring
    Tracks health, performance, costs, and rate limits
    """
    
    def __init__(self, vendor_adapters, db, cache, alert_service):
        self.adapters = vendor_adapters
        self.db = db
        self.cache = cache
        self.alerts = alert_service
    
    async def get_api_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive API monitoring dashboard
        """
        vendor_statuses = await self._get_all_vendor_statuses()
        
        return {
            'vendor_status': vendor_statuses,
            'aggregate_metrics': await self._get_aggregate_metrics(),
            'alerts': await self._get_active_alerts(),
            'cost_breakdown': await self._get_cost_breakdown(),
            'performance_history': await self._get_performance_history(),
            'rate_limit_warnings': await self._get_rate_limit_warnings()
        }
    
    async def _get_all_vendor_statuses(self) -> Dict[str, VendorStatus]:
        """Get status for all configured vendors"""
        statuses = {}
        
        for vendor_name, adapter in self.adapters.items():
            statuses[vendor_name] = await self._get_vendor_status(
                vendor_name, adapter
            )
        
        return statuses
    
    async def _get_vendor_status(self, name: str, adapter) -> VendorStatus:
        """Get detailed status for a single vendor"""
        # Get metrics from cache or database
        metrics = await self.cache.get(f"vendor_metrics:{name}") or {}
        
        # Calculate current status
        status = self._calculate_health_status(metrics)
        
        return VendorStatus(
            name=name,
            status=status,
            response_time_ms=metrics.get('avg_response_time', 0),
            success_rate=metrics.get('success_rate', 1.0),
            rate_limit_remaining=metrics.get('rate_limit_remaining', 1000),
            rate_limit_reset=metrics.get('rate_limit_reset', ''),
            last_error=metrics.get('last_error'),
            cost_today=metrics.get('cost_today', 0),
            calls_today=metrics.get('calls_today', 0)
        )
    
    def _calculate_health_status(self, metrics: Dict) -> str:
        """Calculate health status based on metrics"""
        success_rate = metrics.get('success_rate', 1.0)
        response_time = metrics.get('avg_response_time', 0)
        
        if success_rate < 0.9 or response_time > 2000:
            return 'down'
        elif success_rate < 0.95 or response_time > 1000:
            return 'degraded'
        else:
            return 'healthy'
    
    async def _get_aggregate_metrics(self) -> Dict[str, Any]:
        """Get aggregate metrics across all vendors"""
        total_calls = 0
        total_cost = 0
        total_errors = 0
        total_response_time = 0
        
        for vendor_name in self.adapters:
            metrics = await self.cache.get(f"vendor_metrics:{vendor_name}") or {}
            total_calls += metrics.get('calls_today', 0)
            total_cost += metrics.get('cost_today', 0)
            total_errors += metrics.get('errors_today', 0)
            total_response_time += metrics.get('avg_response_time', 0)
        
        return {
            'total_api_calls_today': total_calls,
            'total_cost_today': total_cost,
            'total_errors_today': total_errors,
            'average_response_time': total_response_time / len(self.adapters) if self.adapters else 0,
            'error_rate': total_errors / total_calls if total_calls > 0 else 0,
            'fallback_triggered_count': await self._get_fallback_count()
        }
    
    async def _get_fallback_count(self) -> int:
        """Count how many times fallback was triggered today"""
        # Placeholder implementation
        return 45
    
    async def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active API-related alerts"""
        alerts = []
        
        for vendor_name in self.adapters:
            metrics = await self.cache.get(f"vendor_metrics:{vendor_name}") or {}
            
            # Check for rate limit warnings
            if metrics.get('rate_limit_remaining', 1000) < 100:
                alerts.append({
                    'vendor': vendor_name,
                    'type': 'rate_limit',
                    'severity': 'warning',
                    'message': f"{vendor_name} approaching rate limit ({metrics.get('rate_limit_remaining')} remaining)",
                    'action': 'Consider reducing request frequency'
                })
            
            # Check for high error rates
            if metrics.get('success_rate', 1.0) < 0.95:
                alerts.append({
                    'vendor': vendor_name,
                    'type': 'error_rate',
                    'severity': 'error',
                    'message': f"{vendor_name} high error rate ({(1 - metrics.get('success_rate', 1.0)) * 100:.1f}%)",
                    'action': 'Check vendor status page'
                })
            
            # Check for slow response times
            if metrics.get('avg_response_time', 0) > 1500:
                alerts.append({
                    'vendor': vendor_name,
                    'type': 'performance',
                    'severity': 'warning',
                    'message': f"{vendor_name} slow response time ({metrics.get('avg_response_time')}ms)",
                    'action': 'Monitor for degradation'
                })
        
        return alerts
    
    async def _get_cost_breakdown(self) -> Dict[str, Any]:
        """Get detailed cost breakdown by vendor"""
        costs = {}
        
        for vendor_name in self.adapters:
            metrics = await self.cache.get(f"vendor_metrics:{vendor_name}") or {}
            costs[vendor_name] = {
                'today': metrics.get('cost_today', 0),
                'week': metrics.get('cost_week', 0),
                'month': metrics.get('cost_month', 0),
                'per_call': metrics.get('cost_per_call', 0)
            }
        
        return {
            'by_vendor': costs,
            'total_today': sum(v['today'] for v in costs.values()),
            'total_week': sum(v['week'] for v in costs.values()),
            'total_month': sum(v['month'] for v in costs.values()),
            'projection_month': sum(v['month'] for v in costs.values()) * 1.1  # Simple projection
        }
    
    async def _get_performance_history(self, hours: int = 24) -> List[Dict]:
        """Get performance history for charts"""
        history = []
        
        for i in range(hours):
            timestamp = datetime.now() - timedelta(hours=i)
            
            # Get metrics for this hour (placeholder data)
            history.append({
                'timestamp': timestamp.isoformat(),
                'sovrn_response_time': 145 + (i * 5),
                'amazon_response_time': 523 + (i * 10),
                'ebay_response_time': 234 + (i * 7),
                'total_calls': 523 - (i * 10),
                'error_count': 2 if i % 5 == 0 else 0
            })
        
        return history
    
    async def _get_rate_limit_warnings(self) -> List[Dict]:
        """Get vendors approaching rate limits"""
        warnings = []
        
        for vendor_name in self.adapters:
            metrics = await self.cache.get(f"vendor_metrics:{vendor_name}") or {}
            remaining = metrics.get('rate_limit_remaining', 1000)
            reset_time = metrics.get('rate_limit_reset', '')
            
            if remaining < 500:  # Warning threshold
                warnings.append({
                    'vendor': vendor_name,
                    'remaining': remaining,
                    'reset_time': reset_time,
                    'usage_percentage': (1000 - remaining) / 10,  # Assuming 1000 limit
                    'severity': 'critical' if remaining < 100 else 'warning'
                })
        
        return sorted(warnings, key=lambda x: x['remaining'])
    
    async def test_vendor_api(
        self, 
        vendor: str, 
        test_query: str = "iPhone 15"
    ) -> Dict[str, Any]:
        """
        Manually test a vendor API
        Useful for debugging issues
        """
        if vendor not in self.adapters:
            raise ValueError(f"Unknown vendor: {vendor}")
        
        adapter = self.adapters[vendor]
        
        start_time = time.time()
        try:
            # Perform test search
            response = await adapter.search(test_query)
            response_time = (time.time() - start_time) * 1000
            
            return {
                'success': True,
                'vendor': vendor,
                'query': test_query,
                'response_time_ms': response_time,
                'result_count': len(response.get('products', [])),
                'sample_results': response.get('products', [])[:3],
                'headers': response.get('headers', {}),
                'rate_limit_info': self._extract_rate_limit_info(response.get('headers', {}))
            }
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            return {
                'success': False,
                'vendor': vendor,
                'query': test_query,
                'response_time_ms': response_time,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def _extract_rate_limit_info(self, headers: Dict) -> Dict:
        """Extract rate limit information from response headers"""
        return {
            'limit': headers.get('X-RateLimit-Limit'),
            'remaining': headers.get('X-RateLimit-Remaining'),
            'reset': headers.get('X-RateLimit-Reset')
        }
    
    async def trigger_vendor_fallback(self, primary_vendor: str) -> Dict:
        """Manually trigger fallback from one vendor to another"""
        # This would trigger the fallback mechanism
        return {
            'primary_vendor': primary_vendor,
            'fallback_vendor': 'sovrn',  # Default fallback
            'reason': 'Manual trigger',
            'timestamp': datetime.now().isoformat()
        }
    
    async def reset_vendor_metrics(self, vendor: str) -> Dict:
        """Reset metrics for a vendor (useful after fixing issues)"""
        await self.cache.delete(f"vendor_metrics:{vendor}")
        
        return {
            'vendor': vendor,
            'status': 'metrics_reset',
            'timestamp': datetime.now().isoformat()
        }