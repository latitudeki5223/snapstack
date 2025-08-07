"""
Generic Product Parser - Extracts meaningful tokens from ANY product text
No category assumptions - truly universal parsing
"""
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class Token:
    """Represents an extracted token from text"""
    value: str
    type: str  # 'measurement', 'number', 'brand', 'keyword', 'exact_phrase'
    confidence: float
    position: int = 0
    context: Optional[str] = None


@dataclass
class ParseResult:
    """Result from parsing operation"""
    products: List[Dict[str, Any]]
    tokens: List[Token]
    confidence: float
    parser_used: str = 'generic'
    raw_text: str = ''


class GenericParser:
    """
    Category-agnostic parser that extracts searchable tokens.
    Works for ANY product - from electronics to groceries to unicorn onesies.
    """
    
    def __init__(self):
        # Common words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
            'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about',
            'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'i', 'want', 'need', 'buy',
            'get', 'find', 'search', 'looking'
        }
        
    def parse(self, text: str) -> ParseResult:
        """
        Parse any product text into searchable tokens
        
        Args:
            text: Raw user input
            
        Returns:
            ParseResult with extracted tokens and search queries
        """
        if not text:
            return ParseResult(products=[], tokens=[], confidence=0.0, raw_text=text)
        
        # Normalize text but preserve original for context
        original_text = text
        text = self._normalize_text(text)
        
        # Extract all meaningful tokens
        tokens = self._extract_tokens(text)
        
        # Build search queries from tokens
        products = self._build_products(tokens, original_text)
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(tokens)
        
        return ParseResult(
            products=products,
            tokens=tokens,
            confidence=confidence,
            parser_used='generic',
            raw_text=original_text
        )
    
    def _normalize_text(self, text: str) -> str:
        """Basic text normalization"""
        # Preserve structure but clean up
        text = text.strip()
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _extract_tokens(self, text: str) -> List[Token]:
        """Extract all meaningful tokens without category assumptions"""
        tokens = []
        position = 0
        used_positions = set()
        
        # 1. Extract quoted phrases first (highest priority)
        quoted_pattern = r'"([^"]+)"'
        for match in re.finditer(quoted_pattern, text):
            tokens.append(Token(
                value=match.group(1),
                type='exact_phrase',
                confidence=1.0,
                position=match.start()
            ))
            used_positions.update(range(match.start(), match.end()))
        
        # 2. Extract measurements (universal for any product)
        measurement_pattern = r'(\d+(?:\.\d+)?)\s*(gb|tb|mb|kg|g|mg|lbs?|oz|ml|l|inch|"|cm|mm|pk|pack|count|ct|pc|quart|qt|gallon|gal|yard|yd|meter|m|foot|ft)'
        for match in re.finditer(measurement_pattern, text.lower()):
            if match.start() not in used_positions:
                value = f"{match.group(1)}{match.group(2)}"
                tokens.append(Token(
                    value=value,
                    type='measurement',
                    confidence=0.95,
                    position=match.start()
                ))
                used_positions.update(range(match.start(), match.end()))
        
        # 3. Extract model numbers (mix of letters and numbers)
        model_pattern = r'\b([A-Z]+[\d]+[A-Z\d]*|[\d]+[A-Z]+[\d\w]*)\b'
        for match in re.finditer(model_pattern, text):
            if match.start() not in used_positions:
                tokens.append(Token(
                    value=match.group(1),
                    type='model',
                    confidence=0.85,
                    position=match.start()
                ))
                used_positions.update(range(match.start(), match.end()))
        
        # 4. Extract standalone numbers
        number_pattern = r'\b(\d+)\b'
        for match in re.finditer(number_pattern, text):
            if match.start() not in used_positions:
                tokens.append(Token(
                    value=match.group(1),
                    type='number',
                    confidence=0.7,
                    position=match.start()
                ))
                used_positions.update(range(match.start(), match.end()))
        
        # 5. Extract brand-like words (capitalized)
        brand_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        for match in re.finditer(brand_pattern, text):
            if match.start() not in used_positions:
                tokens.append(Token(
                    value=match.group(1),
                    type='brand',
                    confidence=0.8,
                    position=match.start()
                ))
                used_positions.update(range(match.start(), match.end()))
        
        # 6. Extract remaining keywords
        words = text.split()
        word_position = 0
        for word in words:
            word_position = text.find(word, word_position)
            if word_position not in used_positions and word.lower() not in self.stop_words:
                # Check if this word wasn't already captured
                if not any(word in token.value for token in tokens):
                    tokens.append(Token(
                        value=word,
                        type='keyword',
                        confidence=0.6,
                        position=word_position
                    ))
            word_position += len(word)
        
        # Sort by position to maintain order
        tokens.sort(key=lambda x: x.position)
        
        return tokens
    
    def _build_products(self, tokens: List[Token], original_text: str) -> List[Dict[str, Any]]:
        """Build searchable products from tokens"""
        if not tokens:
            return []
        
        # Look for natural separators (comma, "and", newline)
        separator_pattern = r'[,\n]|\s+and\s+'
        parts = re.split(separator_pattern, original_text)
        
        if len(parts) > 1:
            # Multiple products detected
            products = []
            for part in parts:
                part_tokens = [t for t in tokens if t.value in part]
                if part_tokens:
                    products.append(self._tokens_to_product(part_tokens, part))
            return products
        else:
            # Single product
            return [self._tokens_to_product(tokens, original_text)]
    
    def _tokens_to_product(self, tokens: List[Token], raw_text: str) -> Dict[str, Any]:
        """Convert tokens to a searchable product"""
        # Prioritize tokens by type and confidence
        high_priority = []
        medium_priority = []
        low_priority = []
        
        for token in tokens:
            if token.type in ['exact_phrase', 'measurement', 'model']:
                high_priority.append(token)
            elif token.type in ['brand', 'number']:
                medium_priority.append(token)
            else:
                low_priority.append(token)
        
        # Build search query
        search_parts = []
        search_parts.extend([t.value for t in high_priority])
        search_parts.extend([t.value for t in medium_priority])
        search_parts.extend([t.value for t in low_priority[:3]])  # Limit keywords
        
        # Remove duplicates while preserving order
        seen = set()
        unique_parts = []
        for part in search_parts:
            if part.lower() not in seen:
                seen.add(part.lower())
                unique_parts.append(part)
        
        return {
            'search_query': ' '.join(unique_parts),
            'tokens': [asdict(t) for t in tokens],
            'raw_text': raw_text.strip(),
            'token_count': len(tokens),
            'priority_tokens': [t.value for t in high_priority]
        }
    
    def _calculate_confidence(self, tokens: List[Token]) -> float:
        """Calculate overall parsing confidence"""
        if not tokens:
            return 0.0
        
        # Weight by token type
        weights = {
            'exact_phrase': 1.0,
            'measurement': 0.95,
            'model': 0.85,
            'brand': 0.8,
            'number': 0.7,
            'keyword': 0.6
        }
        
        total_weight = 0
        weighted_confidence = 0
        
        for token in tokens:
            weight = weights.get(token.type, 0.5)
            total_weight += weight
            weighted_confidence += token.confidence * weight
        
        return weighted_confidence / total_weight if total_weight > 0 else 0.5


def test_parser():
    """Test the parser with various products"""
    parser = GenericParser()
    
    test_cases = [
        "iPhone 15 Pro 256GB",
        "instant pot 6 quart",
        "lego star wars millennium falcon",
        "organic honey 32oz",
        "red dress size 8",
        "dewalt 20v drill",
        "purple yoga mat 6mm thick",
        "dog bed large waterproof",
        "that thing from tiktok",
        '"Atomic Habits" by James Clear',
        "Nike Air Max 90 size 10",
        "Samsung 65 inch OLED TV",
    ]
    
    print("Generic Parser Test Results\n" + "="*50)
    
    for test_input in test_cases:
        result = parser.parse(test_input)
        print(f"\nInput: {test_input}")
        print(f"Confidence: {result.confidence:.2f}")
        
        for product in result.products:
            print(f"  Search Query: {product['search_query']}")
            print(f"  Priority Tokens: {product['priority_tokens']}")
            
        print(f"  All Tokens:")
        for token in result.tokens[:5]:  # Show first 5 tokens
            print(f"    - {token.value} ({token.type}, conf: {token.confidence:.2f})")
    
    return True


if __name__ == "__main__":
    test_parser()