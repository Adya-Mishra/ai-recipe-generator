# 🍳 AI Recipe Generator

An intelligent recipe recommendation system that helps you find the perfect dish based on your preferences, available ingredients, and time constraints.

## 📋 Features

- **Natural Language Understanding**: Ask for recipes in plain English
- **Smart Filtering**: Specify ingredients to include or exclude
- **Time-Based Recommendations**: Find quick recipes when you're in a hurry
- **Command-Line Interface**: Easy to use text-based interface
- **Web Interface**: Beautiful responsive web UI (requires Flask)

## 🛠️ Requirements

- Python 3.8 or higher
- Dependencies:
  - Flask==3.1.0
  - nltk==3.8.1
  - numpy==2.2.4
  - pandas==2.2.3
  - scikit-learn==1.6.1
  - spacy==3.8.4

## 🚀 Installation

1. Clone this repository or download the source code:

```bash
git clone https://github.com/Adya-Mishra/ai-recipe-generator.git
cd ai-recipe-generator
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Download the SpaCy language model:

```bash
python -m spacy download en_core_web_md
```

## 🧠 How It Works

The AI Recipe Generator combines several intelligent components:

1. **Natural Language Understanding (NLU)**: Interprets your recipe requests using pattern matching and SpaCy NLP
2. **Recipe Engine**: Searches for recipes that match your criteria using TF-IDF vectorization and cosine similarity
3. **Sample Dataset**: Includes a variety of recipes to get you started (automatically generated if no dataset is provided)

## 💻 Usage

### Command-Line Interface

Run the recipe generator with the command-line interface:

```bash
python main.py
```

Example queries:
- "Show me a recipe for chocolate cake"
- "I want something with pasta"
- "Give me a quick breakfast idea"
- "I need a recipe without dairy"

### Web Interface

Run the recipe generator with the web interface (requires Flask):

```bash
python main.py --web
```

Then open your browser and navigate to: http://127.0.0.1:5000

## 📁 Project Structure

- `main.py`: Entry point for the application, handles CLI and web interfaces
- `nlu.py`: Natural Language Understanding component for interpreting user requests
- `recipe_engine.py`: Core search functionality for finding recipes
- `data/recipes.csv`: Recipe database (auto-generated if not provided)

## 🔍 Adding Your Own Recipes

To use your own recipe collection, create a CSV file with the following columns:
- `recipe_name`: The name of the recipe
- `ingredients`: Comma-separated list of ingredients
- `instructions`: Steps to prepare the recipe
- `cook_time`: Preparation time in minutes

Place this file at `data/recipes.csv` or specify a custom path when initializing the RecipeEngine.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
