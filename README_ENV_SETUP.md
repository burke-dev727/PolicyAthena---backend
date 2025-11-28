# Virtual Environment Setup Guide

## ✅ Current Status

You have a working virtual environment with:
- **Python Version**: 3.12.11
- **Environment Name**: `rag_env`
- **Location**: `./rag_env`

## 📦 Installed Packages

All packages from `requirements.txt` are installed:
- ✅ sentence-transformers (for embeddings)
- ✅ scikit-learn (TF-IDF and vector search)
- ✅ pandas, numpy (data processing)
- ✅ nltk (text processing)
- ✅ jupyter, ipykernel (notebook support)
- ⚠️ FAISS (optional - uses sklearn fallback)

## 🚀 How to Use

### Step 1: Activate the Environment

```bash
source activate_env.sh
```

Or manually:
```bash
source rag_env/bin/activate
```

### Step 2: Start Jupyter

```bash
jupyter notebook
# or
jupyter lab
```

### Step 3: Select Kernel in Jupyter

When you open a notebook, make sure to select:
**Kernel → Python 3.12 (rag_env)**

## 🔧 Creating a Fresh Environment (if needed)

If you need to recreate the environment:

```bash
# Remove old environment
rm -rf rag_env

# Create new environment with Python 3.12
python3.12 -m venv rag_env

# Activate
source rag_env/bin/activate

# Install packages
pip install -r requirements.txt

# Install Jupyter kernel
python -m ipykernel install --user --name=rag_env --display-name="Python 3.12 (rag_env)"
```

## ⚠️ Important Notes

1. **FAISS**: Not installed due to compilation issues. The code automatically uses sklearn as fallback - works perfectly!

2. **OpenMP Warning**: The code sets `KMP_DUPLICATE_LIB_OK=TRUE` automatically to prevent OpenMP library conflicts on macOS.

3. **Python Version**: Requires Python 3.12 or later.

## 📝 Running the Notebook

The notebook `rag_policy_comparison.ipynb` is ready to run. All cells should execute without issues.

## 🐛 Troubleshooting

If you encounter any import errors:

```bash
# Verify environment is activated
which python  # Should show: */rag_env/bin/python

# Check Python version
python --version  # Should be 3.12.x

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

