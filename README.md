# PolicyAthena---backend
A modular, multi-agent AI backend that powers personalized health insurance recommendations. Built with FastAPI and designed around intelligent agents (Input Interpreter, Profile Builder, Plan Matcher, Scorer, and Explainer)

## Project Overview
This project is a web-based application designed to compare products from different websites. It accepts two URLs, attempts to scrape product information from those web pages (using Selenium), and then prompts OpenAI to generate a detailed comparison between the products based on factors provided by the application's frontend.

## Installation
1. Clone the repository: 
```
git clone <repository_url>
```
2. Ensure you are using Python 3.12 or later. If you are using Python 3.11 or earlier, the "setuptools" requirement may not function correctly.
```
brew install python@3.12                    # Mac
winget install -e --id Python.Python.3.12   # Windows
```
3. Create and activate a virtual environment: 
Create a virtual environment
```
python -m venv .venv   # Mac
py -m venv .venv     # Windows
```
Activate the virtual environment
```
source .venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate    # Windows
```
4. Install required dependencies:
```
pip install -r requirements.txt
```
5. Set up environment variables:
- Create a `.env` file in the root of your project with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
```
6. Run the application:
```
uvicorn app.main:app --reload
```
7. Access Swagger for testing:
- Navigate to `http://127.0.0.1:8000/docs` in your browser to access the Swagger UI and test API routes
