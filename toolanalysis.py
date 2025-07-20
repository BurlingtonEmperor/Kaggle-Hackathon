import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import os

SCRIPTS_CSV = 'meta_kaggle/Scripts.csv'
COMPETITIONS_CSV = 'meta_kaggle/Competitions.csv'

# Load data
scripts_df = pd.read_csv(SCRIPTS_CSV, low_memory=False)
competitions_df = pd.read_csv(COMPETITIONS_CSV, low_memory=False)

# get timestamps
merged_df = scripts_df.merge(competitions_df[['Id', 'Deadline']], left_on='CompetitionId', right_on='Id')
merged_df['Year'] = pd.to_datetime(merged_df['Deadline'], errors='coerce').dt.year
merged_df = merged_df.dropna(subset=['Year', 'SourceCode'])

# Step 2: Extract tools/libraries used in the code
def extract_tools(code):
    tools = set()
    if pd.isnull(code):
        return tools
    # Add more patterns as needed
    patterns = {
        'tensorflow': r'import tensorflow|from tensorflow',
        'keras': r'import keras|from keras',
        'sklearn': r'import sklearn|from sklearn',
        'xgboost': r'import xgboost|from xgboost',
        'lightgbm': r'import lightgbm|from lightgbm',
        'pytorch': r'import torch|from torch',
        'numpy': r'import numpy|from numpy',
        'pandas': r'import pandas|from pandas',
        'matplotlib': r'import matplotlib|from matplotlib',
        'seaborn': r'import seaborn|from seaborn',
    }
    for tool, pattern in patterns.items():
        if re.search(pattern, code):
            tools.add(tool)
    return tools

merged_df['tools_used'] = merged_df['SourceCode'].apply(extract_tools)

# Remove empty tool sets
merged_df = merged_df[merged_df['tools_used'].map(len) > 0]
X = merged_df[['Year']].values
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(merged_df['tools_used'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Dense(32, activation='relu', input_shape=(1,)),
    Dense(64, activation='relu'),
    Dense(len(mlb.classes_), activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.2f}")

# predict tool usage in future years
future_years = np.array([[2026], [2027], [2028]])
predictions = model.predict(future_years)
for year, pred in zip(future_years.flatten(), predictions):
    tools_predicted = [tool for tool, prob in zip(mlb.classes_, pred) if prob > 0.5]
    print(f"In {year}, likely tools: {tools_predicted}")
