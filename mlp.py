import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from data_handler_mlp import label_data
import joblib

def split_data(x, y, test_size=0.1):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)

    x_train = x_train.reshape(-1,1)
    x_test = x_test.reshape(-1,1)

    return x_train, x_test, y_train, y_test


def create_mlp(hidden_layers=(100, 100, 100, 100, 100), activation='relu', max_iter=10000):
    model = MLPRegressor(hidden_layer_sizes=hidden_layers,
                         activation=activation,
                         max_iter=max_iter,
                         random_state=42)
    return model

def train_model(model, x_train, y_train):
    model.fit(x_train, y_train)
    return model

def evaluate_model(model, x_test, y_test):
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

# Function to save the trained MLP model to a file
def save_model(model, filename):
    try:
        joblib.dump(model, filename)
        print("Model saved successfully as", filename)
    except Exception as e:
        print("Error saving the model:", e)

# Function to load a saved MLP model from a file
def load_model(filename):
    try:
        model = joblib.load(filename)
        print("Model loaded successfully from", filename)
        return model
    except Exception as e:
        print("Error loading the model:", e)
        return None

def main():

    provas = ['CN', 'MT', 'LC', 'CH']

    for prova in provas:
        x,y = label_data(prova, 'anything really')
        x_train, x_test, y_train, y_test = split_data(x, y)

        model = create_mlp()
        model = train_model(model, x_train, y_train)

        mse, r2 = evaluate_model(model, x_test, y_test)

        # Print the evaluation results
        print("Mean Squared Error:", mse)
        print("R-squared:", r2)

        model_filename = "models/trained_model_" + prova + ".joblib"
        save_model(model, model_filename)

if __name__ == "__main__":
    main()

