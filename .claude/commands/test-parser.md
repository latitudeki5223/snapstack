Test the parser with: $ARGUMENTS

Execute comprehensive parser testing:

1. **Parse the input**
   - Show regex layer results
   - Show NLP layer results (if used)
   - Show LLM layer results (if used)
   - Display confidence scores

2. **Show parsed output**
   ```json
   {
     "products": [...],
     "confidence": 0.95,
     "parser_used": "regex|nlp|llm",
     "parsing_time_ms": 15
   }
   ```

3. **Validate results**
   - Check product name extraction
   - Verify attributes (size, color, quantity)
   - Validate category assignment

4. **Performance metrics**
   - Parsing time
   - Memory usage
   - Cache hit/miss

5. **Suggestions**
   - How to improve parsing for this input
   - Similar patterns to add to regex
   - Training data recommendations

Save test case to packages/parser/test_cases.json