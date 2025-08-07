Implement a parser for: $ARGUMENTS

Follow the SnapStack hybrid parsing architecture:

1. **Analyze Input Format**
   - Identify patterns in the input
   - Determine structured vs unstructured elements
   - List edge cases to handle

2. **Implement Regex Layer**
   - Create patterns for known formats
   - Handle common variations
   - Return confidence scores

3. **Add NLP Layer (if needed)**
   - Use spaCy for entity recognition
   - Extract: product names, dosages, timing, forms
   - Handle ambiguous matches

4. **OpenAI Fallback**
   - Design prompt for structured extraction
   - Use function calling for consistent output
   - Handle API errors gracefully

5. **Caching Strategy**
   - Store parsed results in PostgreSQL
   - Use pgvector for similarity matching
   - Implement cache invalidation rules

6. **Testing**
   - Create test cases for each layer
   - Include edge cases and malformed input
   - Target 95% accuracy on common formats

Save to packages/parser/ with comprehensive tests
Update parser documentation