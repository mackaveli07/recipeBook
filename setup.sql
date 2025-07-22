DROP TABLE IF EXISTS Recipes;

CREATE TABLE Recipes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    calories FLOAT,
    fat FLOAT,
    carbohydrates FLOAT,
    protein FLOAT
);
