import argparse
import os

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def load_data(path: str):
    """Load housing data from a CSV file.

    The CSV file must contain the following columns:
        - square_feet
        - bedrooms
        - bathrooms
        - price
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Data file '{path}' not found. Please provide a CSV file with housing data."\
        )

    df = pd.read_csv(path)
    required = {"square_feet", "bedrooms", "bathrooms", "price"}
    if not required.issubset(df.columns):
        raise ValueError(
            f"CSV file must contain the columns: {', '.join(sorted(required))}."
        )

    X = df[["square_feet", "bedrooms", "bathrooms"]]
    y = df["price"]
    return X, y


def train_model(X, y):
    """Train a linear regression model."""
    model = LinearRegression()
    model.fit(X, y)
    return model


def evaluate(model, X_test, y_test):
    """Evaluate the model and return evaluation metrics."""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)
    return {
        "mse": mse,
        "rmse": rmse,
        "r2": r2,
    }


def main():
    parser = argparse.ArgumentParser(
        description=
        "Train a linear regression model to predict house prices based on square footage, bedrooms, and bathrooms."
    )
    parser.add_argument(
        "--data",
        type=str,
        default="housing_data.csv",
        help="Path to CSV file containing housing data.",
    )
    parser.add_argument(
        "--model-out",
        type=str,
        default="house_price_model.joblib",
        help="Filename to save the trained model.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of data to use as the test set (default: 0.2).",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random state for train/test split (default: 42).",
    )

    args = parser.parse_args()

    # Load data
    X, y = load_data(args.data)

    # Split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    # Train
    model = train_model(X_train, y_train)

    # Evaluate
    metrics = evaluate(model, X_test, y_test)

    print("Model trained successfully!")
    print("Coefficients:")
    print(f"  square_feet: {model.coef_[0]:.4f}")
    print(f"  bedrooms:     {model.coef_[1]:.4f}")
    print(f"  bathrooms:    {model.coef_[2]:.4f}")
    print(f"Intercept:      {model.intercept_:.4f}")
    print("\nEvaluation (test set):")
    print(f"  MSE:  {metrics['mse']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  R^2:  {metrics['r2']:.4f}")

    # Persist the model
    joblib.dump(model, args.model_out)
    print(f"\nTrained model saved to '{args.model_out}'.")


if __name__ == "__main__":
    main()