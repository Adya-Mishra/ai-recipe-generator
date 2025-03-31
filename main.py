import os
import argparse
from recipe_engine import RecipeEngine
from nlu import SimpleNLU

try:
    from flask import Flask, request, render_template, jsonify
    app = Flask(__name__)
except ImportError:
    app = None

recipe_engine = RecipeEngine()
nlu = SimpleNLU()

@app.route('/', methods=['GET'])
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Recipe Generator</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --primary: #ff6b6b;
                --secondary: #4ecdc4;
                --dark: #1a535c;
                --light: #f7fff7;
                --accent: #ff9f1c;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            body {
                background-color: #f5f5f5;
                color: var(--dark);
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            header {
                background-color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 20px 0;
                position: sticky;
                top: 0;
                z-index: 100;
            }
            
            .search-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px 20px;
                max-width: 800px;
                margin: 0 auto;
            }
            
            .logo {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 30px;
            }
            
            .logo h1 {
                font-size: 2.5rem;
                color: var(--primary);
                margin-left: 10px;
            }
            
            .logo i {
                font-size: 2rem;
                color: var(--accent);
            }
            
            .search-box {
                width: 100%;
                position: relative;
                margin-bottom: 20px;
            }
            
            .search-input {
                width: 100%;
                padding: 15px 20px;
                padding-right: 60px;
                border-radius: 50px;
                border: none;
                background: white;
                box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
                font-size: 1.1rem;
                transition: all 0.3s ease;
            }
            
            .search-input:focus {
                outline: none;
                box-shadow: 0 2px 20px rgba(0, 0, 0, 0.15);
            }
            
            .search-button {
                position: absolute;
                right: 5px;
                top: 5px;
                background: var(--primary);
                color: white;
                border: none;
                width: 45px;
                height: 45px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.3s ease;
            }
            
            .search-button:hover {
                background: var(--dark);
            }
            
            .examples {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
                margin-bottom: 30px;
            }
            
            .example-pill {
                background: white;
                border: 1px solid #ddd;
                padding: 8px 15px;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 0.9rem;
            }
            
            .example-pill:hover {
                background: var(--light);
                border-color: var(--primary);
                transform: translateY(-2px);
            }
            
            .results {
                width: 100%;
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 30px;
                margin-top: 40px;
            }
            
            .recipe-card {
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            
            .recipe-card:hover {
                transform: translateY(-5px);
            }
            
            .recipe-image {
                height: 200px;
                background-color: var(--secondary);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                color: white;
            }
            
            .recipe-content {
                padding: 20px;
            }
            
            .recipe-title {
                font-size: 1.3rem;
                margin-bottom: 10px;
                color: var(--dark);
            }
            
            .recipe-meta {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                color: #666;
            }
            
            .recipe-meta i {
                margin-right: 5px;
                color: var(--accent);
            }
            
            .recipe-meta span {
                margin-right: 15px;
            }
            
            .ingredients-title, .instructions-title {
                font-size: 1.1rem;
                margin: 15px 0 10px;
                color: var(--primary);
            }
            
            .ingredients-list, .instructions-list {
                padding-left: 20px;
            }
            
            .ingredients-list li, .instructions-list li {
                margin-bottom: 5px;
            }
            
            .instructions-list li {
                margin-bottom: 10px;
            }
            
            .no-results {
                text-align: center;
                width: 100%;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            
            .no-results i {
                font-size: 3rem;
                color: var(--primary);
                margin-bottom: 20px;
            }
            
            @media (max-width: 768px) {
                .logo h1 {
                    font-size: 2rem;
                }
                
                .search-container {
                    padding: 20px 10px;
                }
                
                .results {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div class="search-container">
                    <div class="logo">
                        <i class="fas fa-utensils"></i>
                        <h1>AI Recipe Generator</h1>
                    </div>
                    <div class="search-box">
                        <input type="text" id="query" class="search-input" placeholder="What would you like to cook today?">
                        <button class="search-button" onclick="searchRecipes()"><i class="fas fa-search"></i></button>
                    </div>
                    <div class="examples">
                        <div class="example-pill" onclick="setExample('Show me a recipe for chocolate cake')">Chocolate cake</div>
                        <div class="example-pill" onclick="setExample('Pasta')">Quick pasta</div>
                        <div class="example-pill" onclick="setExample('Something with no dairy')">No dairy dish</div>
                    </div>
                </div>
            </div>
        </header>
        
        <div class="container">
            <div id="results" class="results"></div>
        </div>
        
        <script>
            function setExample(text) {
                document.getElementById('query').value = text;
                searchRecipes();
            }
            
            function searchRecipes() {
                const query = document.getElementById('query').value;
                if (!query.trim()) return;
                
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<div class="no-results"><i class="fas fa-spinner fa-spin"></i><h2>Searching for recipes...</h2></div>';
                
                fetch('/search?query=' + encodeURIComponent(query))
                    .then(response => response.json())
                    .then(data => {
                        resultsDiv.innerHTML = '';
                        
                        if (data.recipes.length === 0) {
                            resultsDiv.innerHTML = `
                                <div class="no-results">
                                    <i class="far fa-frown"></i>
                                    <h2>No recipes found</h2>
                                    <p>Try different ingredients or a simpler query</p>
                                </div>
                            `;
                            return;
                        }
                        
                        for (const recipe of data.recipes) {
                            const recipeCard = document.createElement('div');
                            recipeCard.className = 'recipe-card';

                            const foodEmojis = ['🍕', '🍔', '🥗', '🍝', '🍲', '🍰', '🍪', '🥘', '🥩', '🍜', '🥑', '🍗', '🥞', '🥐'];
                            const randomEmoji = foodEmojis[Math.floor(Math.random() * foodEmojis.length)];
                            
                            const formattedTitle = recipe.name
                                .split(' ')
                                .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                                .join(' ');
                            
                            const cleanIngredients = recipe.ingredients.map(ingredient => {
                                return ingredient.replace(/[\[\]']/g, '').trim();
                            });
                            
                            const cleanInstructions = recipe.instructions.map(instruction => {
                                return instruction.replace(/[\[\]']/g, '').replace(/^\d+\.\s*/, '').trim();
                            });
                            
                            recipeCard.innerHTML = `
                                <div class="recipe-image">
                                    ${randomEmoji}
                                </div>
                                <div class="recipe-content">
                                    <h2 class="recipe-title">${formattedTitle}</h2>
                                    <div class="recipe-meta">
                                        <i class="far fa-clock"></i>
                                        <span>${recipe.cook_time} minutes</span>
                                    </div>
                                    <h3 class="ingredients-title">Ingredients</h3>
                                    <ul class="ingredients-list">
                                        ${cleanIngredients.map(i => `<li>${i}</li>`).join('')}
                                    </ul>
                                    <h3 class="instructions-title">Instructions</h3>
                                    <ol class="instructions-list">
                                        ${cleanInstructions.map(i => `<li>${i}</li>`).join('')}
                                    </ol>
                                </div>
                            `;
                            
                            resultsDiv.appendChild(recipeCard);
                        }
                    })
                    .catch(error => {
                        resultsDiv.innerHTML = `
                            <div class="no-results">
                                <i class="fas fa-exclamation-triangle"></i>
                                <h2>Error</h2>
                                <p>Something went wrong. Please try again.</p>
                            </div>
                        `;
                        console.error('Error:', error);
                    });
            }
            
            document.getElementById('query').addEventListener('keyup', function(event) {
                if (event.key === 'Enter') {
                    searchRecipes();
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    parsed_data = nlu.parse(query)
    search_query, constraints = nlu.extract_query_info(parsed_data)
    
    recipes = recipe_engine.search_recipes(search_query, constraints)
    
    result = {
        'recipes': []
    }
    
    for recipe in recipes:
        ingredients = []
        if isinstance(recipe['ingredients'], str):
            if recipe['ingredients'].startswith('[') and recipe['ingredients'].endswith(']'):
                try:
                    ingredients_str = recipe['ingredients'][1:-1]
                    import re
                    ingredients = re.findall(r'\'([^\']+)\'|\"([^\"]+)\"', ingredients_str)
                    ingredients = [i[0] if i[0] else i[1] for i in ingredients]
                except:
                    ingredients = [item.strip() for item in recipe['ingredients'].split(',')]
            else:
                ingredients = [item.strip() for item in recipe['ingredients'].split(',')]
        elif isinstance(recipe['ingredients'], list):
            ingredients = recipe['ingredients']
        
        instructions = []
        if isinstance(recipe['instructions'], str):
            if recipe['instructions'].startswith('[') and recipe['instructions'].endswith(']'):
                try:
                    instructions_str = recipe['instructions'][1:-1]
                    import re
                    instructions = re.findall(r'\'([^\']+)\'|\"([^\"]+)\"', instructions_str)
                    instructions = [i[0] if i[0] else i[1] for i in instructions]
                except:
                    raw_instructions = recipe['instructions'].replace('. ', '.|').split('|')
                    instructions = [instr.strip() for instr in raw_instructions if instr.strip()]
            elif '. ' in recipe['instructions']:
                raw_instructions = recipe['instructions'].replace('. ', '.|').split('|')
                instructions = [instr.strip() for instr in raw_instructions if instr.strip()]
            elif '\n' in recipe['instructions']:
                raw_instructions = recipe['instructions'].split('\n')
                instructions = [instr.strip() for instr in raw_instructions if instr.strip()]
            else:
                instructions = [recipe['instructions'].strip()]
        elif isinstance(recipe['instructions'], list):
            instructions = recipe['instructions']
        
        cook_time = int(recipe['cook_time']) if 'cook_time' in recipe else 0
        
        recipe_data = {
            'name': recipe['recipe_name'],
            'cook_time': cook_time,
            'ingredients': ingredients,
            'instructions': instructions
        }
        
        result['recipes'].append(recipe_data)
    
    return jsonify(result)

def run_cli_interface(recipe_engine, nlu):
    """Run command-line interface for the recipe generator"""
    print("\n" + "="*60)
    print("🍳 AI Recipe Generator 🍳".center(60))
    print("="*60)
    print("Ask for any recipe or specify your preferences.")
    print("Examples:")
    print("  - 'Show me a recipe for chocolate cake'")
    print("  - 'I want something with pasta'")
    print("  - 'Give me a quick breakfast idea'")
    print("Type 'exit' to quit.")
    print("="*60 + "\n")
    
    while True:
        user_input = input("\n👨‍🍳 What would you like to cook? ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Thank you for using AI Recipe Generator. Goodbye!")
            break
        
        parsed_data = nlu.parse(user_input)
        query, constraints = nlu.extract_query_info(parsed_data)
        
        print("\n🔍 Understanding your request...")
        if parsed_data["intent"] == "request_recipe":
            print(f"Looking for recipes related to: {query}")
        
        for key, value in constraints.items():
            if key == "include_ingredients":
                if isinstance(value, list):
                    print(f"Must include: {', '.join(value)}")
                else:
                    print(f"Must include: {value}")
            elif key == "exclude_ingredients":
                if isinstance(value, list):
                    print(f"Must exclude: {', '.join(value)}")
                else:
                    print(f"Must exclude: {value}")
            elif key == "max_time":
                print(f"Maximum cooking time: {value} minutes")
        
        recipes = recipe_engine.search_recipes(query, constraints)
        
        if recipes:
            print(f"\nI found {len(recipes)} recipes that match your request:")
            for recipe in recipes:
                print(recipe_engine.format_recipe(recipe))
        else:
            print("\nI couldn't find any recipes matching your criteria. Could you try with different ingredients or preferences?")

def main():
    parser = argparse.ArgumentParser(description='AI Recipe Generator')
    parser.add_argument('--web', action='store_true', help='Run with web interface')
    args = parser.parse_args()
    
    if args.web and app is not None:
        print("\n" + "="*60)
        print("🍳 AI Recipe Generator Web Interface 🍳".center(60))
        print("="*60)
        print("Starting web server. Open http://127.0.0.1:5000 in your browser.")
        print("Press CTRL+C to stop the server.")
        print("="*60 + "\n")
        app.run(debug=True)
    else:
        if args.web and app is None:
            print("Flask is not installed. Running command-line interface instead.")
            print("To use the web interface, install Flask with: pip install flask")
        run_cli_interface(recipe_engine, nlu)

if __name__ == "__main__":
    main()