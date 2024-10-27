import asyncio
import numpy as np
import pandas as pd
import matplotlib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def make_dataset(file_csv_path):
    try:
        df = pd.read_excel(file_csv_path)
        return df
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        raise

def new_value(df, col_name, month_num):
    experiment_numbers = df.index.tolist()

    X = [[num] for num in experiment_numbers]  # Признаки (номер эксперимента)
    y = df[col_name]  # Целевая переменная (результат эксперимента)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    new_value = [[experiment_numbers[-1]+month_num]]  # Значение фактора, для которого вы хотите предсказать результат
    predicted_target = model.predict(new_value)
    
    return predicted_target[0]