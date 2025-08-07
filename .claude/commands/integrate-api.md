Integrate vendor API: $ARGUMENTS

Create a robust API integration following this pattern:

1. **Research API**
   - Read API documentation
   - Identify required endpoints
   - Note rate limits and auth requirements

2. **Design Adapter**
   - Create adapter interface
   - Map vendor data to SnapStack schema
   - Handle vendor-specific quirks

3. **Implement Integration**
   - Authentication flow
   - Request/response handling
   - Error handling and retries
   - Rate limiting with exponential backoff

4. **Add Caching**
   - Cache strategy (TTL, invalidation)
   - Store in Redis/PostgreSQL
   - Handle stale data gracefully

5. **Testing**
   - Mock API responses
   - Test error scenarios
   - Verify rate limit handling
   - Check data mapping accuracy

6. **Monitoring**
   - Log all API calls
   - Track success/failure rates
   - Alert on degradation

Create in apps/backend/integrations/[vendor-name]/
Include comprehensive documentation