
CREATE TABLE Recipes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255),
    ingredients TEXT,
    instructions TEXT,
    
    calories FLOAT,
    fat FLOAT,
    carbohydrates FLOAT,
    protein FLOAT
);
