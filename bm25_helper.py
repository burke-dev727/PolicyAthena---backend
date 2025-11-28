"""
Helper code to add BM25 support to the RAG system.
Add this code to your notebook after the PolicyRAGSystem class definition.
"""

# 1. Add to __init__ method (in PolicyRAGSystem class):
# self.bm25 = None
# self.bm25_tokenized_corpus = None

# 2. Add setup_bm25 method:
def setup_bm25(self):
    """
    Setup BM25 for better keyword-based search.
    BM25 is generally better than TF-IDF for search tasks.
    """
    print("🔄 Setting up BM25...")
    
    # Extract texts for BM25
    texts = [item['embedding_text'] for item in self.policy_data]
    
    # Tokenize corpus for BM25
    self.bm25_tokenized_corpus = [self._tokenize(text) for text in texts]
    
    # Create and fit BM25
    self.bm25 = BM25Okapi(self.bm25_tokenized_corpus)
    
    print(f"✅ BM25 setup complete with {len(self.bm25_tokenized_corpus)} documents")

def _tokenize(self, text: str):
    """Tokenize text for BM25."""
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

# 3. Replace keyword_search method:
def keyword_search(self, query: str, top_k: int = 10):
    """
    Perform keyword-based search using BM25.
    
    Args:
        query: Search query
        top_k: Number of top results to return
        
    Returns:
        List of search results with metadata
    """
    if not query or not query.strip():
        return []
    
    if top_k <= 0:
        return []
    
    # Tokenize query
    query_tokens = self._tokenize(query)
    
    # Get BM25 scores
    scores = self.bm25.get_scores(query_tokens)
    
    # Get top results
    actual_top_k = min(top_k, len(scores))
    top_indices = scores.argsort()[-actual_top_k:][::-1]
    
    results = []
    for i, idx in enumerate(top_indices):
        if 0 <= idx < len(self.policy_data) and scores[idx] > 0:
            item = self.policy_data[idx]
            results.append({
                'rank': i + 1,
                'chunk_id': item['chunk_id'],
                'policy_id': item['document_id'],
                'policy_name': item['document_name'],
                'text': item['original_text'],
                'embedding_text': item['embedding_text'],
                'keyword_score': float(scores[idx]),
                'metadata': item['metadata']
            })
    
    return results


