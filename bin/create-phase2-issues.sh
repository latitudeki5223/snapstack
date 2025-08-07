#!/bin/bash

echo "🚀 Creating Phase 2: Parser Core Issues"
echo "======================================="

# Create Phase 2 milestone
echo "Creating Phase 2 milestone..."
gh api repos/latitudeki5223/snapstack/milestones \
  --method POST \
  --field title="Phase 2: Parser Core" \
  --field description="Improve parser accuracy and connect to real products" \
  --field due_on="2024-02-07T23:59:59Z" || echo "Milestone may already exist"

# Parser improvement issues
echo ""
echo "Creating parser improvement issues..."

gh issue create \
  --title "Add parser caching with PostgreSQL and pgvector" \
  --body "Implement caching layer for parsed results using PostgreSQL with pgvector for similarity matching. Target >60% cache hit rate after first month." \
  --label "parser,backend,priority" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Create comprehensive parser test corpus (500+ examples)" \
  --body "Build test dataset covering all product categories: electronics, fashion, home, food, etc. Include edge cases and ambiguous inputs." \
  --label "parser,testing" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Implement parser accuracy metrics and tracking" \
  --body "Add accuracy measurement system, track confidence scores, identify failure patterns. Target 95% accuracy." \
  --label "parser,metrics" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Add NLP layer with spaCy for entity recognition" \
  --body "Integrate spaCy as second parser layer for semi-structured text. Should handle 5-50ms response time." \
  --label "parser,enhancement" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Implement LLM fallback layer with OpenAI" \
  --body "Add OpenAI as final fallback for ambiguous inputs. Cache all LLM results. Target 200-500ms response." \
  --label "parser,ai" \
  --milestone "Phase 2: Parser Core"

# API Integration issues
echo ""
echo "Creating API integration issues..."

gh issue create \
  --title "Create mock Sovrn Commerce API adapter" \
  --body "Build mock API with realistic product data for testing. Should return products, prices, affiliate links." \
  --label "api,testing,priority" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Connect parser output to product search" \
  --body "Wire parser results to API search. Transform tokens into search queries, handle multiple products." \
  --label "parser,api,priority" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Build product display in Parser Studio" \
  --body "Show actual products (from mock API) after parsing. Display name, price, image, vendor." \
  --label "ui,admin" \
  --milestone "Phase 2: Parser Core"

# Performance issues
echo ""
echo "Creating performance optimization issues..."

gh issue create \
  --title "Optimize parser confidence scoring algorithm" \
  --body "Improve confidence calculation based on token types and patterns. Weight by success rates." \
  --label "parser,optimization" \
  --milestone "Phase 2: Parser Core"

gh issue create \
  --title "Add parser performance monitoring" \
  --body "Track parse times, cache hit rates, parser layer usage. Add to admin dashboard." \
  --label "parser,monitoring" \
  --milestone "Phase 2: Parser Core"

echo ""
echo "✅ Phase 2 issues created successfully!"
echo ""
echo "View issues at: https://github.com/latitudeki5223/snapstack/issues"