import React, { useState } from 'react';

interface Token {
  value: string;
  type: string;
  confidence: number;
  position: number;
  context?: string;
}

interface Product {
  search_query: string;
  tokens: Token[];
  raw_text: string;
  token_count: number;
  priority_tokens: string[];
}

interface ParseResult {
  products: Product[];
  tokens: Token[];
  confidence: number;
  parser_used: string;
  raw_text: string;
}

interface ExampleCategory {
  category: string;
  inputs: string[];
}

const ParserStudio: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [parseResult, setParseResult] = useState<ParseResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [examples, setExamples] = useState<ExampleCategory[]>([]);
  const [showExamples, setShowExamples] = useState(false);

  // Fetch examples on component mount
  React.useEffect(() => {
    fetchExamples();
  }, []);

  const fetchExamples = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/admin/parser/examples');
      const data = await response.json();
      setExamples(data);
    } catch (err) {
      console.error('Failed to fetch examples:', err);
    }
  };

  const handleParse = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to parse');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/admin/parser/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await response.json();

      if (data.success) {
        setParseResult(data.result);
      } else {
        setError(data.error || 'Failed to parse text');
      }
    } catch (err) {
      setError('Failed to connect to parser service');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setInputText(example);
    setShowExamples(false);
  };

  const getTokenTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      exact_phrase: 'bg-purple-100 text-purple-800',
      measurement: 'bg-blue-100 text-blue-800',
      model: 'bg-green-100 text-green-800',
      brand: 'bg-yellow-100 text-yellow-800',
      number: 'bg-orange-100 text-orange-800',
      keyword: 'bg-gray-100 text-gray-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'text-green-600';
    if (confidence >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Parser Studio</h1>
          <p className="text-gray-600 mt-2">
            Test the generic parser with any product text - from electronics to unicorn onesies!
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Panel */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Input Text
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter any product text... e.g., iPhone 15 Pro 256GB, organic honey 32oz, that thing from tiktok"
              />
            </div>

            <div className="flex gap-2 mb-4">
              <button
                onClick={handleParse}
                disabled={loading}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
              >
                {loading ? 'Parsing...' : 'Parse Text'}
              </button>
              <button
                onClick={() => setShowExamples(!showExamples)}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Examples
              </button>
              <button
                onClick={() => {
                  setInputText('');
                  setParseResult(null);
                  setError(null);
                }}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Clear
              </button>
            </div>

            {/* Examples Section */}
            {showExamples && (
              <div className="border border-gray-200 rounded-lg p-4 max-h-96 overflow-y-auto">
                {examples.map((category) => (
                  <div key={category.category} className="mb-4">
                    <h3 className="font-semibold text-sm text-gray-700 mb-2">
                      {category.category}
                    </h3>
                    <div className="space-y-1">
                      {category.inputs.map((example) => (
                        <button
                          key={example}
                          onClick={() => handleExampleClick(example)}
                          className="block w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
                        >
                          {example}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}
          </div>

          {/* Results Panel */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold mb-4">Parse Results</h2>

            {!parseResult ? (
              <div className="text-gray-500 text-center py-12">
                Enter text and click "Parse Text" to see results
              </div>
            ) : (
              <div className="space-y-6">
                {/* Overall Confidence */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">
                      Overall Confidence
                    </span>
                    <span className={`text-lg font-bold ${getConfidenceColor(parseResult.confidence)}`}>
                      {(parseResult.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="mt-2 text-xs text-gray-600">
                    Parser: {parseResult.parser_used}
                  </div>
                </div>

                {/* Products */}
                {parseResult.products.map((product, idx) => (
                  <div key={idx} className="border border-gray-200 rounded-lg p-4">
                    <h3 className="font-semibold text-sm text-gray-700 mb-2">
                      Product {idx + 1}
                    </h3>
                    
                    <div className="mb-3">
                      <div className="text-xs text-gray-600 mb-1">Search Query:</div>
                      <div className="bg-blue-50 text-blue-900 px-3 py-2 rounded font-mono text-sm">
                        {product.search_query}
                      </div>
                    </div>

                    {product.priority_tokens.length > 0 && (
                      <div className="mb-3">
                        <div className="text-xs text-gray-600 mb-1">Priority Tokens:</div>
                        <div className="flex flex-wrap gap-1">
                          {product.priority_tokens.map((token, i) => (
                            <span key={i} className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs">
                              {token}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}

                {/* All Tokens */}
                <div>
                  <h3 className="font-semibold text-sm text-gray-700 mb-3">
                    Extracted Tokens ({parseResult.tokens.length})
                  </h3>
                  <div className="space-y-2">
                    {parseResult.tokens.map((token, idx) => (
                      <div key={idx} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 rounded text-xs ${getTokenTypeColor(token.type)}`}>
                            {token.type}
                          </span>
                          <span className="font-mono text-sm">{token.value}</span>
                        </div>
                        <span className={`text-xs ${getConfidenceColor(token.confidence)}`}>
                          {(token.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParserStudio;