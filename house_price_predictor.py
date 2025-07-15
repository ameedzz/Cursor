import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')

class HousePricePredictor:
    """
    A linear regression model to predict house prices based on:
    - Square footage
    - Number of bedrooms
    - Number of bathrooms
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.feature_names = ['square_footage', 'bedrooms', 'bathrooms']
        
    def generate_sample_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """
        Generate synthetic house data for demonstration purposes
        """
        np.random.seed(42)
        
        # Generate realistic house features
        square_footage = np.random.normal(2000, 500, n_samples)
        square_footage = np.clip(square_footage, 800, 5000)  # Reasonable range
        
        bedrooms = np.random.poisson(3, n_samples)
        bedrooms = np.clip(bedrooms, 1, 6)  # 1-6 bedrooms
        
        bathrooms = np.random.poisson(2, n_samples)
        bathrooms = np.clip(bathrooms, 1, 4)  # 1-4 bathrooms
        
        # Generate price based on realistic relationships
        # Base price + price per sqft + bedroom bonus + bathroom bonus + noise
        price = (
            50000 +  # Base price
            square_footage * 120 +  # $120 per sqft
            bedrooms * 15000 +  # $15k per bedroom
            bathrooms * 10000 +  # $10k per bathroom
            np.random.normal(0, 20000, n_samples)  # Random noise
        )
        
        # Ensure no negative prices
        price = np.maximum(price, 50000)
        
        data = pd.DataFrame({
            'square_footage': square_footage,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'price': price
        })
        
        return data
    
    def load_data(self, file_path: str = None) -> pd.DataFrame:
        """
        Load house data from file or generate sample data
        """
        if file_path and pd.io.common.file_exists(file_path):
            data = pd.read_csv(file_path)
            required_columns = self.feature_names + ['price']
            if not all(col in data.columns for col in required_columns):
                raise ValueError(f"Data must contain columns: {required_columns}")
            return data
        else:
            print("No data file provided or file not found. Generating sample data...")
            return self.generate_sample_data()
    
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features and target variables
        """
        X = data[self.feature_names].values
        y = data['price'].values
        return X, y
    
    def train(self, data: pd.DataFrame, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Train the linear regression model
        """
        X, y = self.prepare_data(data)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Make predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'test_mae': mean_absolute_error(y_test, y_test_pred),
            'coefficients': dict(zip(self.feature_names, self.model.coef_)),
            'intercept': self.model.intercept_
        }
        
        # Store test data for visualization
        self.X_test = X_test
        self.y_test = y_test
        self.y_test_pred = y_test_pred
        
        return metrics
    
    def predict(self, square_footage: float, bedrooms: int, bathrooms: int) -> float:
        """
        Predict house price for given features
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        features = np.array([[square_footage, bedrooms, bathrooms]])
        prediction = self.model.predict(features)[0]
        return prediction
    
    def predict_batch(self, features: np.ndarray) -> np.ndarray:
        """
        Predict house prices for multiple houses
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        return self.model.predict(features)
    
    def plot_results(self, save_plot: bool = False):
        """
        Create visualizations of the model performance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before plotting results")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Actual vs Predicted prices
        axes[0, 0].scatter(self.y_test, self.y_test_pred, alpha=0.6)
        axes[0, 0].plot([self.y_test.min(), self.y_test.max()], 
                       [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        axes[0, 0].set_xlabel('Actual Price')
        axes[0, 0].set_ylabel('Predicted Price')
        axes[0, 0].set_title('Actual vs Predicted Prices')
        
        # 2. Residuals plot
        residuals = self.y_test - self.y_test_pred
        axes[0, 1].scatter(self.y_test_pred, residuals, alpha=0.6)
        axes[0, 1].axhline(y=0, color='r', linestyle='--')
        axes[0, 1].set_xlabel('Predicted Price')
        axes[0, 1].set_ylabel('Residuals')
        axes[0, 1].set_title('Residuals Plot')
        
        # 3. Feature importance (coefficients)
        coefficients = self.model.coef_
        axes[1, 0].bar(self.feature_names, coefficients)
        axes[1, 0].set_xlabel('Features')
        axes[1, 0].set_ylabel('Coefficient Value')
        axes[1, 0].set_title('Feature Importance (Coefficients)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Distribution of residuals
        axes[1, 1].hist(residuals, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[1, 1].set_xlabel('Residuals')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Distribution of Residuals')
        
        plt.tight_layout()
        
        if save_plot:
            plt.savefig('house_price_model_results.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def print_model_summary(self, metrics: Dict[str, Any]):
        """
        Print a summary of the model performance
        """
        print("=" * 50)
        print("HOUSE PRICE PREDICTION MODEL SUMMARY")
        print("=" * 50)
        print(f"Model Type: Linear Regression")
        print(f"Features: {', '.join(self.feature_names)}")
        print("\nModel Performance:")
        print(f"  Training R²: {metrics['train_r2']:.4f}")
        print(f"  Testing R²: {metrics['test_r2']:.4f}")
        print(f"  Training RMSE: ${metrics['train_rmse']:,.2f}")
        print(f"  Testing RMSE: ${metrics['test_rmse']:,.2f}")
        print(f"  Training MAE: ${metrics['train_mae']:,.2f}")
        print(f"  Testing MAE: ${metrics['test_mae']:,.2f}")
        
        print("\nModel Coefficients:")
        print(f"  Intercept: ${metrics['intercept']:,.2f}")
        for feature, coef in metrics['coefficients'].items():
            print(f"  {feature.replace('_', ' ').title()}: ${coef:,.2f}")
        
        print("\nInterpretation:")
        print(f"  - Each additional square foot adds ${metrics['coefficients']['square_footage']:.2f} to the price")
        print(f"  - Each additional bedroom adds ${metrics['coefficients']['bedrooms']:,.2f} to the price")
        print(f"  - Each additional bathroom adds ${metrics['coefficients']['bathrooms']:,.2f} to the price")

def main():
    """
    Main function to demonstrate the house price prediction model
    """
    # Initialize the predictor
    predictor = HousePricePredictor()
    
    # Load or generate data
    print("Loading data...")
    data = predictor.load_data()
    print(f"Data loaded: {len(data)} houses")
    
    # Display basic statistics
    print("\nData Overview:")
    print(data.describe())
    
    # Train the model
    print("\nTraining the model...")
    metrics = predictor.train(data)
    
    # Print model summary
    predictor.print_model_summary(metrics)
    
    # Make some example predictions
    print("\n" + "=" * 50)
    print("EXAMPLE PREDICTIONS")
    print("=" * 50)
    
    examples = [
        (2000, 3, 2),
        (1500, 2, 1),
        (3000, 4, 3),
        (1200, 1, 1),
        (2500, 3, 2.5)
    ]
    
    for sqft, beds, baths in examples:
        predicted_price = predictor.predict(sqft, beds, baths)
        print(f"House: {sqft} sqft, {beds} bed, {baths} bath → Predicted Price: ${predicted_price:,.2f}")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    try:
        predictor.plot_results(save_plot=True)
        print("Plots saved as 'house_price_model_results.png'")
    except Exception as e:
        print(f"Could not create plots (possibly no display available): {e}")
    
    return predictor

if __name__ == "__main__":
    model = main()