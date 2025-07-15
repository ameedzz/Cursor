# House Price Prediction Model

A comprehensive linear regression model to predict house prices based on square footage, number of bedrooms, and number of bathrooms.

## Features

- **Linear Regression Model**: Uses scikit-learn's LinearRegression for price prediction
- **Multiple Input Features**: Predicts based on square footage, bedrooms, and bathrooms
- **Data Generation**: Automatically generates realistic synthetic data for demonstration
- **Custom Data Support**: Can load and train on your own CSV data
- **Model Evaluation**: Comprehensive metrics including R², RMSE, and MAE
- **Visualization**: Creates plots showing model performance and feature importance
- **Batch Predictions**: Support for predicting multiple houses at once
- **Model Interpretation**: Clear explanation of coefficients and their meaning

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Alternative Installation** (if you prefer conda):
   ```bash
   conda install numpy pandas scikit-learn matplotlib seaborn
   ```

## Quick Start

### Basic Usage

```python
from house_price_predictor import HousePricePredictor

# Initialize the predictor
predictor = HousePricePredictor()

# Load or generate data (will generate sample data if no file provided)
data = predictor.load_data()

# Train the model
metrics = predictor.train(data)

# Print model performance
predictor.print_model_summary(metrics)

# Make a prediction
price = predictor.predict(square_footage=2000, bedrooms=3, bathrooms=2)
print(f"Predicted price: ${price:,.2f}")
```

### Run the Complete Demo

```bash
python house_price_predictor.py
```

This will:
- Generate sample data
- Train the model
- Display performance metrics
- Show example predictions
- Create visualization plots

### Run Usage Examples

```bash
python example_usage.py
```

This demonstrates various usage scenarios including custom data and batch predictions.

## Data Format

If you want to use your own data, create a CSV file with the following columns:

```csv
square_footage,bedrooms,bathrooms,price
2000,3,2,350000
1500,2,1,280000
2500,4,3,420000
...
```

Then load it:

```python
predictor = HousePricePredictor()
data = predictor.load_data('your_data.csv')
```

## Model Performance Metrics

The model provides several evaluation metrics:

- **R² Score**: Coefficient of determination (higher is better, max = 1.0)
- **RMSE**: Root Mean Square Error (lower is better)
- **MAE**: Mean Absolute Error (lower is better)

## Understanding the Model

### Linear Regression Formula

The model predicts house prices using the formula:

```
Price = Intercept + (Square_Footage × Coef1) + (Bedrooms × Coef2) + (Bathrooms × Coef3)
```

### Feature Interpretation

- **Square Footage Coefficient**: Price increase per additional square foot
- **Bedroom Coefficient**: Price increase per additional bedroom
- **Bathroom Coefficient**: Price increase per additional bathroom
- **Intercept**: Base price when all features are zero

## API Reference

### HousePricePredictor Class

#### Methods

- `__init__()`: Initialize the predictor
- `generate_sample_data(n_samples=1000)`: Generate synthetic house data
- `load_data(file_path=None)`: Load data from CSV or generate sample data
- `train(data, test_size=0.2)`: Train the model and return performance metrics
- `predict(square_footage, bedrooms, bathrooms)`: Predict price for a single house
- `predict_batch(features)`: Predict prices for multiple houses
- `plot_results(save_plot=False)`: Create performance visualization plots
- `print_model_summary(metrics)`: Display model performance summary

## Example Outputs

### Model Summary
```
==================================================
HOUSE PRICE PREDICTION MODEL SUMMARY
==================================================
Model Type: Linear Regression
Features: square_footage, bedrooms, bathrooms

Model Performance:
  Training R²: 0.9876
  Testing R²: 0.9823
  Training RMSE: $23,456.78
  Testing RMSE: $28,901.23
  Training MAE: $18,234.56
  Testing MAE: $21,567.89

Model Coefficients:
  Intercept: $45,678.90
  Square Footage: $120.45
  Bedrooms: $15,234.56
  Bathrooms: $12,345.67
```

### Example Predictions
```
House: 2000 sqft, 3 bed, 2 bath → Predicted Price: $350,245.67
House: 1500 sqft, 2 bed, 1 bath → Predicted Price: $275,123.45
House: 3000 sqft, 4 bed, 3 bath → Predicted Price: $485,678.90
```

## Visualizations

The model creates four types of plots:

1. **Actual vs Predicted Prices**: Scatter plot showing model accuracy
2. **Residuals Plot**: Shows prediction errors vs predicted values
3. **Feature Importance**: Bar chart of coefficient values
4. **Residuals Distribution**: Histogram of prediction errors

## Files Description

- `house_price_predictor.py`: Main implementation with the HousePricePredictor class
- `example_usage.py`: Comprehensive examples showing different use cases
- `requirements.txt`: Python dependencies
- `README.md`: This documentation file

## Requirements

- Python 3.7+
- NumPy >= 1.21.0
- Pandas >= 1.3.0
- Scikit-learn >= 1.0.0
- Matplotlib >= 3.4.0
- Seaborn >= 0.11.0

## Limitations

- This is a linear model, so it assumes linear relationships between features and price
- The model uses only three features; real-world price prediction would benefit from additional features (location, age, condition, etc.)
- The synthetic data is generated with known relationships, so real-world performance may vary

## Extensions

You can extend this model by:

- Adding more features (location, house age, garage size, etc.)
- Using more advanced algorithms (Random Forest, Gradient Boosting, Neural Networks)
- Implementing feature engineering (polynomial features, interaction terms)
- Adding cross-validation for more robust evaluation
- Implementing feature scaling/normalization

## License

This project is provided as-is for educational and demonstration purposes.