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

    elif menu == "View/Edit Recipes":
        st.header("📚 View or Edit Recipes")
        if not recipes:
            st.info("No recipes found.")
        else:
            for i, r in enumerate(recipes):
                with st.expander(r["name"]):
                    st.subheader("Ingredients")
                    st.markdown("\\n".join(f"- {ing}" for ing in r["ingredients"]))

                    st.subheader("Instructions")
                    st.markdown(r["instructions"])

                    st.markdown(f"**Serving Size**: {r['serving_size']}")

                    if "nutrition" in r:
                        st.subheader("🍎 Nutrition Facts")
                        n = r["nutrition"]
                        st.markdown(
                            f"- **Calories**: {n.get('calories', 0)} kcal\\n"
                            f"- **Fat**: {n.get('fat', 0)} g\\n"
                            f"- **Carbs**: {n.get('carbohydrates', 0)} g\\n"
                            f"- **Protein**: {n.get('protein', 0)} g"
                        )

                    if st.button(f"Edit '{r['name']}'", key=f"edit_{i}"):
                        st.session_state.edit_index = i

            if "edit_index" in st.session_state:
                idx = st.session_state.edit_index
                r = recipes[idx]
                st.subheader(f"✏️ Edit Recipe: {r['name']}")
                name = st.text_input("Recipe Name", value=r["name"], key="edit_name")
                ingredients = st.text_area("Ingredients (one per line)", value="\\n".join(r["ingredients"]), key="edit_ingredients")
                instructions = st.text_area("Instructions", value=r["instructions"], key="edit_instructions")
                serving_size = st.text_input("Serving Size", value=r["serving_size"], key="edit_serving")

                n = r.get("nutrition", {})
                calories = st.number_input("Calories", min_value=0.0, format="%.2f", value=n.get("calories", 0.0), key="edit_calories")
                fat = st.number_input("Fat (g)", min_value=0.0, format="%.2f", value=n.get("fat", 0.0), key="edit_fat")
                carbs = st.number_input("Carbohydrates (g)", min_value=0.0, format="%.2f", value=n.get("carbohydrates", 0.0), key="edit_carbs")
                protein = st.number_input("Protein (g)", min_value=0.0, format="%.2f", value=n.get("protein", 0.0), key="edit_protein")

                if st.button("Save Changes"):
                    updated_nutrition = {
                        "calories": calories,
                        "fat": fat,
                        "carbohydrates": carbs,
                        "protein": protein
                    }
                    add_or_update_recipe(idx, name, ingredients, instructions, updated_nutrition, serving_size)
                    st.success(f"Recipe '{name}' updated!")
                    del st.session_state.edit_index

if __name__ == "__main__":
    main()
