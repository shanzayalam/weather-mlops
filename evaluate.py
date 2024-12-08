import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(model_path, test_data_path):
    """
    Evaluate the model on the test dataset and print performance metrics.
    
    Args:
        model_path (str): Path to the saved model file.
        test_data_path (str): Path to the test dataset CSV file.
    """
    try:
        # Load the test dataset
        data = pd.read_csv(test_data_path)
        X_test = data.iloc[:, :-1]  # All columns except the target
        y_test = data.iloc[:, -1]  # Target column

        # Load the trained model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        # Predict on the test data
        y_pred = model.predict(X_test)

        # Calculate performance metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Print metrics
        print("Model Evaluation Metrics:")
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1-Score: {f1:.2f}")

    except Exception as e:
        print(f"An error occurred during model evaluation: {e}")

# Example usage
if __name__ == "__main__":
    model_path = "trained_model.pkl"  # Path to the saved model
    test_data_path = "test_data.csv"  # Path to the test dataset
    evaluate_model(model_path, test_data_path)
