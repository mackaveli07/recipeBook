
CREATE TABLE Recipes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255),
    ingredients TEXT,
    instructions TEXT,
    serving_size NVARCHAR(100),
    calories FLOAT,
    fat FLOAT,
    carbohydrates FLOAT,
    protein FLOAT
);
