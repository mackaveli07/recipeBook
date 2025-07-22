import streamlit as st
import json
import os

DATA_DIR = "data"
RECIPE_FILE = os.path.join(DATA_DIR, "recipes.json")

def load_recipes():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(RECIPE_FILE):
        try:
            with open(RECIPE_FILE, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []

def save_recipes(recipes):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(RECIPE_FILE, "w") as f:
        json.dump(recipes, f, indent=4)

def add_or_update_recipe(index, name, ingredients, instructions, nutrition, serving_size):
    recipes = load_recipes()
    new_recipe = {
        "name": name,
        "ingredients": [i.strip() for i in ingredients.split("\\n") if i.strip()],
        "instructions": instructions.strip(),
        "nutrition": nutrition,
        "serving_size": serving_size
    }
    if index is None:
        recipes.append(new_recipe)
    else:
        recipes[index] = new_recipe
    save_recipes(recipes)


def add_recipe(name, ingredients, instructions, nutrition, serving_size):
    recipes = load_recipes()
    new_recipe = {
        "name": name,
        "ingredients": [i.strip() for i in ingredients.split("\n") if i.strip()],
        "instructions": instructions.strip(),
        "nutrition": nutrition,
        "serving_size": serving_size
    }
    recipes.append(new_recipe)
    save_recipes(recipes)

def main():
    st.set_page_config(page_title="Recipe App", layout="centered")
    st.title("🍽️ My Recipe Book")

    menu = st.sidebar.radio("Navigate", ["Add Recipe", "View Recipes"])

    if menu == "Add Recipe":
        st.header("➕ Add New Recipe")
        name = st.text_input("Recipe Name")
        ingredients = st.text_area("Ingredients (one per line)")
        instructions = st.text_area("Instructions")

        st.subheader("🍎 Nutrition Facts")
        calories = st.number_input("Calories", min_value=0.0, format="%.2f")
        fat = st.number_input("Fat (g)", min_value=0.0, format="%.2f")
        carbs = st.number_input("Carbohydrates (g)", min_value=0.0, format="%.2f")
        protein = st.number_input("Protein (g)", min_value=0.0, format="%.2f")

        serving_size = st.text_input("Serving Size (e.g., 1 cup, 2 slices)")

        if st.button("Save Recipe"):
            if not name or not ingredients or not instructions or not serving_size:
                st.warning("Please fill in all fields.")
            else:
                nutrition = {
                    "calories": calories,
                    "fat": fat,
                    "carbohydrates": carbs,
                    "protein": protein
                }
                add_recipe(name, ingredients, instructions, nutrition, serving_size)
                st.success(f"Recipe '{name}' saved!")

    elif menu == "View Recipes":
        st.header("📚 Stored Recipes")
        recipes = load_recipes()
        if not recipes:
            st.info("No recipes found.")
        else:
            for r in recipes:
                with st.expander(r["name"]):
                    st.subheader("Ingredients")
                    st.markdown("\n".join(f"- {i}" for i in r["ingredients"]))

                    st.subheader("Instructions")
                    st.markdown(r["instructions"])

                    if "serving_size" in r:
                        st.markdown(f"**Serving Size**: {r['serving_size']}")

                    if "nutrition" in r:
                        st.subheader("🍎 Nutrition Facts")
                        n = r["nutrition"]
                        st.markdown(
                            f"- **Calories**: {n.get('calories', 0)} kcal\n"
                            f"- **Fat**: {n.get('fat', 0)} g\n"
                            f"- **Carbohydrates**: {n.get('carbohydrates', 0)} g\n"
                            f"- **Protein**: {n.get('protein', 0)} g"
                        )

if __name__ == "__main__":
    main()
