# BM25 当前状态

## ⚠️ 当前问题

**是的，`RAGSearchMethods` 中的 `keyword_search` 方法仍在使用的是 TF-IDF，而不是 BM25。**

## 🔍 现状分析

检查了 notebook，发现：

1. ✅ **Cell 6**: BM25 支持代码已添加
2. ✅ **Cell 8**: 调用 `setup_bm25()` 
3. ❌ **Cell 9 (RAGSearchMethods 类)**: `keyword_search` 方法仍使用 TF-IDF
4. ⚠️ **Cell 11**: 另一个 cell 调用 `setup_tfidf()` 而不是 `setup_bm25()`

## 🎯 需要完成的步骤

### 方案 1: 在 Notebook 中添加代码（推荐）

在运行所有单元格之前，添加一个新的 cell，运行以下代码：

```python
# 将此代码添加到 Notebook 的新 cell 中

# 替换 keyword_search 方法以使用 BM25
def keyword_search_with_bm25(self, query: str, top_k: int = 10):
    """使用 BM25 进行关键词搜索"""
    import re
    
    if not query or not query.strip() or top_k <= 0:
        return []
    
    # 使用 BM25 如果可用
    if self.rag_system.bm25 is not None:
        # 对查询进行 tokenize
        query_tokens = re.findall(r'\b\w+\b', query.lower())
        
        # 获取 BM25 分数
        scores = self.rag_system.bm25.get_scores(query_tokens)
        
        # 获取 top_k 结果
        actual_top_k = min(top_k, len(scores))
        top_indices = scores.argsort()[-actual_top_k:][::-1]
        
        results = []
        for i, idx in enumerate(top_indices):
            if 0 <= idx < len(self.rag_system.policy_data) and scores[idx] > 0:
                item = self.rag_system.policy_data[idx]
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
    else:
        # 如果 BM25 未设置，使用 TF-IDF 作为后备
        from sklearn.metrics.pairwise import cosine_similarity
        query_vector = self.rag_system.tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.rag_system.tfidf_matrix)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for i, idx in enumerate(top_indices):
            if similarities[idx] > 0:
                item = self.rag_system.policy_data[idx]
                results.append({
                    'rank': i + 1,
                    'chunk_id': item['chunk_id'],
                    'policy_id': item['document_id'],
                    'policy_name': item['document_name'],
                    'text': item['original_text'],
                    'embedding_text': item['embedding_text'],
                    'keyword_score': float(similarities[idx]),
                    'metadata': item['metadata']
                })
        return results

# 替换方法
RAGSearchMethods.keyword_search = keyword_search_with_bm25

print("✅ keyword_search 现在使用 BM25!")
```

### 方案 2: 修改现有代码

需要修改 `rag_policy_comparison.ipynb` 中 `RAGSearchMethods` 类的 `keyword_search` 方法（第 545 行），将 TF-IDF 实现替换为上面的 BM25 实现。

## 📝 执行顺序

运行以下 cells 的顺序：

1. **Cell 0-5**: 基础设置
2. **Cell 6**: 添加 BM25 支持到 `PolicyRAGSystem`
3. **Cell 7**: 新 cell - 运行上面的替换代码
4. **Cell 8**: 加载数据并调用 `setup_bm25()`
5. **Cell 9**: 初始化 `RAGSearchMethods`
6. 其余 cells: 正常运行

## ⚙️ 修改 Cell 11

如果您看到有 cell 调用 `setup_tfidf()`，请改为调用 `setup_bm25()`。

## 🧪 验证

验证 BM25 是否工作：

```python
# 测试 keyword_search 是否使用 BM25
results = search_methods.keyword_search("test query", top_k=5)
print(f"找到 {len(results)} 个结果")
if results:
    print(f"第一个结果的 keyword_score: {results[0]['keyword_score']}")
```

如果分数范围是 0-10+，说明在使用 BM25（BM25 的分数通常更高）。
如果分数范围是 0-1，说明仍在用 TF-IDF。


