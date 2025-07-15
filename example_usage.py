#!/usr/bin/env python3
"""
Example usage of the House Price Prediction Model

This script demonstrates how to use the HousePricePredictor class
for various scenarios including custom data and individual predictions.
"""

from house_price_predictor import HousePricePredictor
import pandas as pd
import numpy as np

def example_with_custom_data():
    """
    Example using custom house data
    """
    print("Example 1: Using Custom Data")
    print("-" * 40)
    
    # Create some custom house data
    custom_data = pd.DataFrame({
        'square_footage': [1800, 2200, 1500, 3000, 2500, 1200, 2800, 1900, 2600, 3200],
        'bedrooms': [3, 4, 2, 5, 3, 2, 4, 3, 4, 5],
        'bathrooms': [2, 3, 1, 3, 2, 1, 3, 2, 3, 4],
        'price': [280000, 350000, 220000, 480000, 380000, 180000, 420000, 290000, 390000, 520000]
    })
    
    # Initialize and train the model
    predictor = HousePricePredictor()
    
    print("Training model with custom data...")
    metrics = predictor.train(custom_data, test_size=0.3)
    
    # Print results
    predictor.print_model_summary(metrics)
    
    # Make a prediction
    predicted_price = predictor.predict(2000, 3, 2)
    print(f"\nPrediction for 2000 sqft, 3 bed, 2 bath house: ${predicted_price:,.2f}")
    
    return predictor

def example_with_generated_data():
    """
    Example using generated sample data
    """
    print("\n\nExample 2: Using Generated Sample Data")
    print("-" * 40)
    
    # Initialize predictor
    predictor = HousePricePredictor()
    
    # Generate and use sample data
    data = predictor.generate_sample_data(n_samples=500)
    
    print("Training model with generated data...")
    metrics = predictor.train(data)
    
    # Print summary
    predictor.print_model_summary(metrics)
    
    return predictor

def example_batch_predictions():
    """
    Example of making batch predictions
    """
    print("\n\nExample 3: Batch Predictions")
    print("-" * 40)
    
    # Initialize and train with sample data
    predictor = HousePricePredictor()
    data = predictor.generate_sample_data(n_samples=200)
    predictor.train(data)
    
    # Create batch of houses to predict
    houses_to_predict = np.array([
        [1600, 2, 1],  # Small house
        [2000, 3, 2],  # Medium house
        [2800, 4, 3],  # Large house
        [3500, 5, 4],  # Very large house
        [1200, 1, 1],  # Studio/small apartment
    ])
    
    # Make batch predictions
    predictions = predictor.predict_batch(houses_to_predict)
    
    print("Batch Predictions:")
    for i, (house, price) in enumerate(zip(houses_to_predict, predictions)):
        sqft, beds, baths = house
        print(f"  House {i+1}: {sqft} sqft, {beds} bed, {baths} bath → ${price:,.2f}")

def example_model_interpretation():
    """
    Example showing how to interpret the model coefficients
    """
    print("\n\nExample 4: Model Interpretation")
    print("-" * 40)
    
    # Initialize and train model
    predictor = HousePricePredictor()
    data = predictor.generate_sample_data(n_samples=1000)
    metrics = predictor.train(data)
    
    print("Understanding the model coefficients:")
    print(f"Base price (intercept): ${metrics['intercept']:,.2f}")
    
    sqft_coef = metrics['coefficients']['square_footage']
    bed_coef = metrics['coefficients']['bedrooms']
    bath_coef = metrics['coefficients']['bathrooms']
    
    print(f"\nPrice per square foot: ${sqft_coef:.2f}")
    print(f"Additional value per bedroom: ${bed_coef:,.2f}")
    print(f"Additional value per bathroom: ${bath_coef:,.2f}")
    
    # Example calculation
    example_sqft, example_beds, example_baths = 2000, 3, 2
    manual_prediction = (metrics['intercept'] + 
                        example_sqft * sqft_coef + 
                        example_beds * bed_coef + 
                        example_baths * bath_coef)
    
    model_prediction = predictor.predict(example_sqft, example_beds, example_baths)
    
    print(f"\nManual calculation for {example_sqft} sqft, {example_beds} bed, {example_baths} bath:")
    print(f"  ${metrics['intercept']:,.2f} + ({example_sqft} × ${sqft_coef:.2f}) + ({example_beds} × ${bed_coef:,.2f}) + ({example_baths} × ${bath_coef:,.2f})")
    print(f"  = ${manual_prediction:,.2f}")
    print(f"Model prediction: ${model_prediction:,.2f}")
    print(f"Difference: ${abs(manual_prediction - model_prediction):.2f} (should be ~0)")

def main():
    """
    Run all examples
    """
    print("House Price Prediction Model - Usage Examples")
    print("=" * 50)
    
    # Run examples
    example_with_custom_data()
    example_with_generated_data()
    example_batch_predictions()
    example_model_interpretation()
    
    print("\n" + "=" * 50)
    print("All examples completed!")

if __name__ == "__main__":
    main()