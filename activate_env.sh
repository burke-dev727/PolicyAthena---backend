#!/bin/bash
# Activation script for the RAG policy comparison environment

echo "🔧 Activating Python 3.12 virtual environment..."
source rag_env/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "Environment: Python 3.12"
echo "Location: $(pwd)/rag_env"
echo ""
echo "Installed packages:"
echo "  - sentence-transformers (for embeddings)"
echo "  - scikit-learn (for TF-IDF and vector search)"
echo "  - pandas, numpy (for data processing)"
echo "  - nltk (for text processing)"
echo "  - jupyter, ipykernel (for notebooks)"
echo ""
echo "⚠️  Note: FAISS is not installed (it requires compilation)"
echo "    The code uses sklearn as fallback - works perfectly!"
echo ""
echo "To activate in your terminal, run:"
echo "  source activate_env.sh"
echo ""
echo "To start Jupyter:"
echo "  jupyter notebook"
echo "  or"
echo "  jupyter lab"
echo ""
echo "The kernel 'Python 3.12 (rag_env)' is available in Jupyter"

