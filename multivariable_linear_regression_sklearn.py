# -*- coding: utf-8 -*-
"""multivariable_linear_regression_sklearn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10w3JA652rO9A8T7ltVVldrkFavkzYPJB
"""
import numpy as np
import pandas as pd
import time

# content = "crop_yield(Indian data_set).csv"
content = "crop_yield(USA data_set).csv"
path = "data_set"
path_content = f"{path}/{content}"

df = pd.read_csv(path_content)
print(df)

# **USA Data-set encoding**

# # One-hot encoding
# df_encoded = pd.get_dummies(df, columns=['Crop'])

# Mean encoding
df_encoded = df.copy()
crop_mean_yield = df_encoded.groupby('Crop')['Yield'].mean()
df_encoded['Crop'] = df_encoded['Crop'].map(crop_mean_yield)

# **Indian Data-set encoding**

# # One-hot encoding
# df_encoded = pd.get_dummies(df, columns=['Crop', 'Season', 'State'])

# # Mean encoding
# df_encoded = df.copy()
# crop_mean_yield = df_encoded.groupby('Crop')['Yield'].mean()
# season_mean_yield = df_encoded.groupby('Season')['Yield'].mean()
# state_mean_yield = df_encoded.groupby('State')['Yield'].mean()
# df_encoded['Crop'] = df_encoded['Crop'].map(crop_mean_yield)
# df_encoded['Season'] = df_encoded['Season'].map(season_mean_yield)
# df_encoded['State'] = df_encoded['State'].map(state_mean_yield)

# # Target encoding
# df_encoded = df.copy()
# df_encoded['Crop'] = df_encoded.groupby('Crop')['Yield'].transform('mean')
# df_encoded['Season'] = df_encoded.groupby('Season')['Yield'].transform('mean')
# df_encoded['State'] = df_encoded.groupby('State')['Yield'].transform('mean')

# # Label Encoding
# from sklearn.preprocessing import LabelEncoder
# label_encoder = LabelEncoder()
# df_encoded = df.copy()
# df_encoded['Crop'] = label_encoder.fit_transform(df_encoded['Crop'])
# df_encoded['Season'] = label_encoder.fit_transform(df_encoded['Season'])
# df_encoded['State'] = label_encoder.fit_transform(df_encoded['State'])

# # Feature Hashing
# import hashlib
# def hash_string_to_int(s, num_buckets):
#     return int(hashlib.md5(s.encode()).hexdigest(), 16) % num_buckets
# num_buckets = 10
# df_encoded = df.copy()
# df_encoded['Crop'] = df_encoded['Crop'].apply(lambda x: hash_string_to_int(x, num_buckets))
# df_encoded['Season'] = df_encoded['Season'].apply(lambda x: hash_string_to_int(x, num_buckets))
# df_encoded['State'] = df_encoded['State'].apply(lambda x: hash_string_to_int(x, num_buckets))

# **Display data_set**

print(df_encoded)

# **Mapped value for using Mean encoding**

# crop_mean_yield
# season_mean_yield
# state_mean_yield

# **Check for null value**

print(df_encoded.isnull().sum())

# **Independent variable**

X = df_encoded.drop(columns=['Yield'])
print(X)

# **Dependent variable**

y = df_encoded['Yield']
print(y)

# **Train test seperation**

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# **Assign linear model from sklearn**

from sklearn.linear_model import LinearRegression
lr = LinearRegression()

# **Train model**

start_time = time.time()
lr.fit(X_train, y_train)
end_time = time.time()
training_time = end_time - start_time
print("Training time:", training_time, "seconds")

# **Predict the training model**

y_pred_train = lr.predict(X_train)
# y_pred_train

# **Predict test model**

y_pred_test = lr.predict(X_test)
# y_pred_test

# **Mean square error**

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred_test)
rmse = np.sqrt(mse)
print(rmse)

# **Model accuracy while training**

training_accuracy = lr.score(X_train, y_train)
print(training_accuracy)

# **Model accuracy while testing**

from sklearn.metrics import r2_score
testing_accuracy = r2_score(y_test, y_pred_test)
print(testing_accuracy)

# **Y-intercept**

y_intercept = lr.intercept_
print(y_intercept)

# **Feature coefficients**

coefficients = lr.coef_
print(coefficients)

# **Important stuff**

print(f"Y-intercept (coefficient):\n\ttheta 0 --> {y_intercept} constant_value")
print("\nTheta (coefficients) for Features (independent variable):")

feature_names = X.columns
count = 1
for coefficient, feature in zip(coefficients, feature_names):
    print(f"\ttheta {count} --> {round(coefficient, 10)} for {feature}")
    count += 1
print(f"\nRoot Mean Squared Error (RMSE):\n\t{rmse}")
print(f"\nModel accuracy in training:\n\t{training_accuracy} or {round((training_accuracy*100), 2)}%")
print(f"\nModel accuracy in testing:\n\t{testing_accuracy} or {round((testing_accuracy*100), 2)}%")
print(f"\nTraining time:\n\t{round(training_time, 16)}ms")

# **Total contribution of individual features out of 100%**

abs_coefficients = np.abs(coefficients)
total_contribution = np.sum(abs_coefficients)
percentage_contributions = (abs_coefficients / total_contribution) * 100

feature_contributions = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': coefficients,
    'Contribution (%)': percentage_contributions
})

print(feature_contributions, "\n")
print("Total contribution", total_contribution)

import matplotlib.pyplot as plt

# Combine y-intercept and coefficients
coefficients_with_intercept = [y_intercept] + list(coefficients)  # Include y-intercept as the first element

# Plot
plt.figure(figsize=(16, 8))
features = X.columns
bars = plt.bar(["y-Intercept"] + list(features), coefficients_with_intercept, color='skyblue', edgecolor='black')  # Add "y-Intercept"
plt.axhline(0, color='red', linestyle='--', linewidth=1)

# Annotate each bar with the coefficient value
for bar, value in zip(bars, coefficients_with_intercept):
    height = bar.get_height()
    y_offset = 0.1 if height >= 0 else -0.1  # Adjust label position
    plt.text(bar.get_x() + bar.get_width() / 2, height + y_offset, f"{value:.4f}",
             ha='center', va='bottom' if height >= 0 else 'top', fontsize=10, color='black')

# Add titles and labels
plt.title("Coefficients of Features and y-Intercept", fontsize=16)
plt.xlabel("Features", fontsize=14)
plt.ylabel("Coefficient Value", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.tight_layout()

plt.show()

# **Contribution graph**

plt.figure(figsize=(16, 8))
bars = plt.barh(feature_contributions['Feature'], feature_contributions['Contribution (%)'], color='skyblue')
plt.suptitle('Spiked graph')
plt.title('Feature contribution')
plt.xlabel('Contribution (%)')
plt.gca().invert_yaxis()

for bar, percentage in zip(bars, percentage_contributions):
    plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
             f'{percentage:.2f}%', va='center')

plt.show()

# **Scatter plot graph**

import matplotlib.pyplot as plt

plt.figure(figsize=(28, 12))

plt.subplot(1, 2, 1)
plt.scatter(y_train, y_pred_train, color="skyblue", label="Predicted vs Actual")
plt.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], color="red", linestyle="--", label="y = x (Perfect Prediction)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.title('Training Set: Actual vs Predicted Yield')
plt.xlabel('Actual Yield')
plt.ylabel('Predicted Yield')
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(y_test, y_pred_test, color="skyblue", label="Predicted vs Actual")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", linestyle="--", label="y = x (Perfect Prediction)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.title('Test Set: Actual vs Predicted Yield')
plt.xlabel('Actual Yield')
plt.ylabel('Predicted Yield')
plt.legend()

plt.suptitle('Actual vs Predicted Yield Comparison')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# **Actual vs prediction chart**

plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label='Original Yield Values', marker='o')
plt.plot(y_pred_test, label='Predicted Yield Values', marker='x')
plt.title('Comparison of Original and Predicted Yield Values')
plt.xlabel('Samples')
plt.ylabel('Yield')
plt.legend()
plt.show()

"""# **Actual vs prediction table**"""

print("Actual vs Predicted Yield Values:")
for actual, predicted in zip(y_test, y_pred_test):
    print(f"Actual: {actual:.2f}, Predicted: {predicted:.2f}")