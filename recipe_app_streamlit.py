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


def save_recipe_sql(name, ingredients, instructions, nutrition, serving_size):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Recipes (name, ingredients, instructions, serving_size, calories, fat, carbohydrates, protein)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        "\n".join(ingredients),
        instructions,
        serving_size,
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
        if len(row) < 9:
            continue  # skip incomplete rows
        recipes.append({
            "id": row[0],
            "name": row[1],
            "ingredients": row[2].split("\n"),
            "instructions": row[3],
            "serving_size": row[4],
            "nutrition": {
                "calories": row[5],
                "fat": row[6],
                "carbohydrates": row[7],
                "protein": row[8],
            }
        })
    conn.close()
    return recipes

st.title("📋 Recipe Manager (SQL Edition)")

with st.form("recipe_form", clear_on_submit=True):
    name = st.text_input("Recipe Name")
    ingredients = st.text_area("Ingredients (one per line)").split("\n")
    instructions = st.text_area("Instructions")
    serving_size = st.text_input("Serving Size")
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
        save_recipe_sql(name, ingredients, instructions, nutrition, serving_size)
        st.success("✅ Recipe saved to SQL Server!")

st.subheader("📚 All Recipes")
recipes = load_recipes_sql()
for recipe in recipes:
    with st.expander(recipe["name"]):
        st.markdown(f"**Serving Size:** {recipe['serving_size']}")
        st.markdown("**Ingredients:**")
        st.markdown("\n".join(f"- {item}" for item in recipe["ingredients"]))
        st.markdown("**Instructions:**")
        st.markdown(recipe["instructions"])
        st.markdown("**Nutrition Facts:**")
        st.markdown(f"Calories: {recipe['nutrition']['calories']} kcal")
        st.markdown(f"Fat: {recipe['nutrition']['fat']} g")
        st.markdown(f"Carbs: {recipe['nutrition']['carbohydrates']} g")
        st.markdown(f"Protein: {recipe['nutrition']['protein']} g")
