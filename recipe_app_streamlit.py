import streamlit as st
import json
import os
import pyodbc

# SQL Connection settings (replace with your actual values)
def get_connection():
    secrets = st.secrets["azure_db"]
    conn_str = (
        f"DRIVER={{{secrets['driver']}}};"
        f"SERVER={secrets['server']};"
        f"DATABASE={secrets['database']};"
        f"UID={secrets['user']};"
        f"PWD={secrets['password']}"
    )
    return pyodbc.connect(conn_str)

def save_recipe_sql(name, ingredients, instructions, nutrition):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Recipes (name, ingredients, instructions, calories, fat, carbohydrates, protein)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        "\n".join(ingredients),
        instructions,
        nutrition.get("calories", 0),
        nutrition.get("fat", 0),
        nutrition.get("carbohydrates", 0),
        nutrition.get("protein", 0),
    ))
    conn.commit()
    conn.close()

def load_recipes_sql():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Recipes")
    rows = cursor.fetchall()
    recipes = []
    for row in rows:
        if len(row) < 8:
            continue  # skip incomplete rows
        recipes.append({
            "id": row[0],
            "name": row[1],
            "ingredients": row[2].split("\n"),
            "instructions": row[3],
            "nutrition": {
                "calories": row[4],
                "fat": row[5],
                "carbohydrates": row[6],
                "protein": row[7],
            }
        })
    conn.close()
    return recipes

st.title("📋 Recipe Manager")

with st.form("recipe_form", clear_on_submit=True):
    name = st.text_input("Recipe Name")
    ingredients = st.text_area("Ingredients (one per line)").split("\n")
    instructions = st.text_area("Instructions")
    col1, col2 = st.columns(2)
    with col1:
        calories = st.number_input("Calories", min_value=0.0)
        fat = st.number_input("Fat (g)", min_value=0.0)
    with col2:
        carbs = st.number_input("Carbohydrates (g)", min_value=0.0)
        protein = st.number_input("Protein (g)", min_value=0.0)

    submitted = st.form_submit_button("Save Recipe")
    if submitted:
        nutrition = {
            "calories": calories,
            "fat": fat,
            "carbohydrates": carbs,
            "protein": protein
        }

        try:
            save_recipe_sql(name, ingredients, instructions, nutrition)
            st.success("✅ Recipe saved to SQL Server!")
        except TypeError as e:
            st.error(f"❌ TypeError: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")

st.subheader("📚 All Recipes")
recipes = load_recipes_sql()
for recipe in recipes:
    with st.expander(recipe["name"]):
        st.markdown("**Ingredients:**")
        st.markdown("\n".join(f"- {item}" for item in recipe["ingredients"]))
        st.markdown("**Instructions:**")
        st.markdown(recipe["instructions"])
        st.markdown("**Nutrition Facts:**")
        st.markdown(f"Calories: {recipe['nutrition']['calories']} kcal")
        st.markdown(f"Fat: {recipe['nutrition']['fat']} g")
        st.markdown(f"Carbs: {recipe['nutrition']['carbohydrates']} g")
        st.markdown(f"Protein: {recipe['nutrition']['protein']} g")
