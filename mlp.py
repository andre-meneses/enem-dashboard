# Importing required libraries
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Function to generate synthetic data for demonstration purposes
def generate_synthetic_data(n_samples=100):
    np.random.seed(42)
    X = np.linspace(-10, 10, n_samples).reshape(-1, 1)
    y = np.sin(X) + np.random.normal(0, 0.2, n_samples).reshape(-1, 1)
    return X, y

# Function to split the data into training and testing sets
def split_data(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

# Function to create the MLP model
def create_mlp(hidden_layers=(100, 100, 100, 100, 100), activation='relu', max_iter=1000):
    model = MLPRegressor(hidden_layer_sizes=hidden_layers,
                         activation=activation,
                         max_iter=max_iter,
                         random_state=42)
    return model

# Function to train the MLP model
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

# Function to evaluate the MLP model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

def main():
    # Step 1: Generate synthetic data
    X, y = generate_synthetic_data()

    # Step 2: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Step 3: Create the MLP model
    hidden_layers = (100, 100, 100, 100, 100)
    activation = 'relu'
    max_iter = 1000
    model = create_mlp(hidden_layers=hidden_layers, activation=activation, max_iter=max_iter)

    # Step 4: Train the MLP model
    model = train_model(model, X_train, y_train)

    # Step 5: Evaluate the MLP model
    mse, r2 = evaluate_model(model, X_test, y_test)

    # Print the evaluation results
    print("Mean Squared Error:", mse)
    print("R-squared:", r2)

if __name__ == "__main__":
    main()

