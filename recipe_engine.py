import pandas as pd
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class RecipeEngine:
    def __init__(self, dataset_path="data/recipes.csv"):
        """Initialize the recipe engine with a dataset"""
        self.load_dataset(dataset_path)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.recipe_vectors = None
        self.process_dataset()
        
    def load_dataset(self, dataset_path):
        """Load and prepare the recipe dataset"""
        try:
            self.recipes_df = pd.read_csv(dataset_path)
            print(f"Loaded {len(self.recipes_df)} recipes")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self._create_sample_dataset()
            self.recipes_df = pd.read_csv("data/recipes.csv")
            print(f"Created and loaded sample dataset with {len(self.recipes_df)} recipes")
    
    def _create_sample_dataset(self):
        """Create a sample dataset if none exists"""
        if not os.path.exists('data'):
            os.makedirs('data')
        
        sample_data = {
            'recipe_name': [
                'Spaghetti Carbonara',
                'Vegetable Stir Fry',
                'Chocolate Chip Cookies',
                'Chicken Curry',
                'Greek Salad',
                'Mushroom Risotto',
                'Apple Pie',
                'Beef Tacos',
                'Vegetable Soup',
                'Banana Bread',
                'Vegetarian Lasagna',
                'Chicken Alfredo',
                'Homemade Pizza',
                'Beef Stew',
                'Tomato Soup',
                'Vegetable Biryani',
                'Spinach Quiche',
                'Chicken Noodle Soup',
                'Vegan Black Bean Burger',
                'Shrimp Scampi'
            ],
            'ingredients': [
                'spaghetti, eggs, pancetta, parmesan cheese, black pepper, salt',
                'broccoli, carrots, bell peppers, snap peas, garlic, ginger, soy sauce, vegetable oil',
                'flour, butter, sugar, brown sugar, eggs, vanilla extract, chocolate chips, baking soda, salt',
                'chicken thighs, curry powder, onions, garlic, ginger, coconut milk, tomatoes, cilantro',
                'cucumber, tomatoes, red onion, feta cheese, olives, olive oil, lemon juice, oregano',
                'arborio rice, mushrooms, onion, garlic, white wine, vegetable broth, parmesan cheese, butter',
                'flour, butter, sugar, apples, cinnamon, nutmeg, lemon juice, salt',
                'ground beef, taco seasoning, tortillas, lettuce, tomatoes, cheese, sour cream, salsa',
                'vegetable broth, carrots, celery, onions, potatoes, tomatoes, peas, garlic, herbs',
                'ripe bananas, flour, sugar, eggs, butter, baking soda, salt, vanilla extract',
                'lasagna noodles, tomato sauce, ricotta cheese, spinach, zucchini, eggplant, mozzarella, parmesan',
                'fettuccine, chicken breasts, heavy cream, garlic, parmesan cheese, butter, salt, pepper',
                'pizza dough, tomato sauce, mozzarella cheese, pepperoni, bell peppers, mushrooms, basil',
                'beef chuck, potatoes, carrots, onions, celery, beef broth, tomato paste, garlic, herbs',
                'tomatoes, onions, garlic, vegetable broth, cream, basil, olive oil, sugar',
                'basmati rice, mixed vegetables, yogurt, ginger, garlic, garam masala, turmeric, cumin, coriander',
                'eggs, spinach, onion, cheese, heavy cream, pie crust, nutmeg, salt, pepper',
                'chicken, egg noodles, carrots, celery, onion, chicken broth, garlic, thyme, bay leaf',
                'black beans, quinoa, bell peppers, onion, garlic, cumin, bread crumbs, avocado',
                'shrimp, linguine, garlic, butter, white wine, lemon juice, red pepper flakes, parsley'
            ],
            'instructions': [
                'Boil pasta. Mix eggs, cheese. Cook pancetta. Combine all while pasta is hot.',
                'Heat oil. Stir-fry garlic and ginger. Add vegetables. Add soy sauce. Serve hot.',
                'Cream butter and sugars. Add eggs and vanilla. Mix dry ingredients. Add chocolate chips. Bake at 375°F for 10 minutes.',
                'Brown chicken. Add onions, garlic, and ginger. Add curry powder. Add coconut milk and tomatoes. Simmer. Serve with rice.',
                'Chop vegetables. Mix with feta and olives. Dress with olive oil and lemon juice. Sprinkle oregano.',
                'Sauté onions and mushrooms. Add rice and toast. Add wine. Gradually add broth. Stir constantly. Finish with butter and cheese.',
                'Make dough. Mix apples with sugar and spices. Assemble pie. Bake at 375°F for 45 minutes.',
                'Brown beef with taco seasoning. Warm tortillas. Assemble tacos with toppings.',
                'Sauté onions, carrots, and celery. Add broth and potatoes. Simmer. Add remaining vegetables. Season and serve.',
                'Mash bananas. Mix with butter and sugar. Add eggs and vanilla. Mix in dry ingredients. Bake at 350°F for 60 minutes.',
                'Cook lasagna noodles. Layer with vegetables, sauce, and cheeses. Bake at 375°F for 45 minutes.',
                'Cook pasta. Sauté chicken until done. Add garlic and cream. Stir in cheese. Toss with pasta.',
                'Roll out dough. Add sauce and toppings. Bake at 475°F for 12 minutes.',
                'Brown beef. Add vegetables and broth. Simmer for 2 hours. Add potatoes and cook until tender.',
                'Sauté onions and garlic. Add tomatoes and simmer. Blend until smooth. Add cream and seasoning.',
                'Sauté spices. Add vegetables and rice. Add water and cook until rice is tender.',
                'Mix eggs, cream, and fillings. Pour into crust. Bake at 375°F for 35 minutes.',
                'Simmer chicken in broth. Remove and shred. Cook vegetables in broth. Add chicken and noodles.',
                'Mash beans. Mix with quinoa and vegetables. Form patties. Pan-fry until crispy.',
                'Cook pasta. Sauté garlic in butter. Add shrimp, wine, and lemon. Toss with pasta.'
            ],
            'cook_time': [
                20,
                15,
                25,
                40,
                10,
                30,
                60,
                25,
                45,
                65,
                55,
                30,
                25,
                120,
                30,
                45,
                40,
                35,
                25,
                20
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv('data/recipes.csv', index=False)
    
    def process_dataset(self):
        """Process and vectorize the recipe dataset"""
        self.recipes_df['recipe_text'] = (
            self.recipes_df['recipe_name'].fillna('') + ' ' +
            self.recipes_df['ingredients'].fillna('')
        )
        
        self.recipe_vectors = self.vectorizer.fit_transform(self.recipes_df['recipe_text'])
    
    def search_recipes(self, query, constraints=None, top_n=3):
        """Search for recipes matching the query and constraints"""
        query_vector = self.vectorizer.transform([query])
        
        similarity_scores = cosine_similarity(query_vector, self.recipe_vectors).flatten()
        
        filtered_indices = self._filter_by_constraints(constraints)
            
        if not filtered_indices:
            filtered_indices = list(range(len(self.recipes_df)))
        
        top_indices = sorted([(i, similarity_scores[i]) for i in filtered_indices], 
                            key=lambda x: x[1], reverse=True)[:top_n]
        
        results = []
        for idx, score in top_indices:
            recipe = self.recipes_df.iloc[idx].copy()
            recipe['match_score'] = score
            results.append(recipe)
            
        return results
    
    def _filter_by_constraints(self, constraints):
        """Apply all constraints to filter recipe indices"""
        if not constraints:
            return list(range(len(self.recipes_df)))
        
        filtered_indices = []
        for i, recipe in self.recipes_df.iterrows():
            if self._meets_constraints(recipe, constraints):
                filtered_indices.append(i)
        
        return filtered_indices
    
    def _meets_constraints(self, recipe, constraints):
        """Check if a recipe meets all the specified constraints"""
        if not constraints:
            return True
        
        for constraint_type, constraint_value in constraints.items():
            if constraint_type == 'exclude_ingredients':
                if isinstance(constraint_value, list):
                    for ingredient in constraint_value:
                        if ingredient.lower() in recipe.get('ingredients', '').lower():
                            return False
                elif constraint_value.lower() in recipe.get('ingredients', '').lower():
                    return False
            
            elif constraint_type == 'include_ingredients':
                if isinstance(constraint_value, list):
                    for ingredient in constraint_value:
                        if ingredient.lower() not in recipe.get('ingredients', '').lower():
                            return False
                elif constraint_value.lower() not in recipe.get('ingredients', '').lower():
                    return False
            
            elif constraint_type == 'max_time' and 'cook_time' in recipe:
                if recipe['cook_time'] > constraint_value:
                    return False
        
        return True
    
    def format_recipe(self, recipe):
        """Format a recipe for display"""
        formatted = f"\n{'='*50}\n"
        formatted += f"📝 {recipe['recipe_name'].upper()}\n"
        formatted += f"{'='*50}\n\n"
        
        formatted += f"⭐ Match Score: {recipe.get('match_score', 0):.2f}\n"
        if 'cook_time' in recipe and recipe['cook_time']:
            formatted += f"⏱️ Cook Time: {recipe['cook_time']} minutes\n"
        
        formatted += f"\n📋 INGREDIENTS:\n"
        ingredients = recipe['ingredients'].split(',')
        for i, ingredient in enumerate(ingredients, 1):
            formatted += f"  {i}. {ingredient.strip()}\n"
        
        formatted += f"\n📝 INSTRUCTIONS:\n"
        instructions = recipe['instructions'].replace('. ', '.\n').split('\n')
        for i, step in enumerate(instructions, 1):
            if step.strip():
                formatted += f"  {i}. {step.strip()}\n"
        
        return formatted