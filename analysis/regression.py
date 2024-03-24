import json
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

data_directory = 'data/match_data'

def get_filepaths():
    filepaths = []
    for filename in os.listdir(data_directory):
        if filename.endswith('.json'):
            filepath = os.path.join(data_directory, filename)
            filepaths.append(filepath)
    return filepaths


def prepare_data(match_files):
    data = []

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                units = set()
                spell = player_data['chosenSpell']
                mercenaries = set()

                for build in player_data['buildPerWave']:
                    for unit in build:
                        unit_id = unit.split(':')[0]
                        units.add(unit_id)

                for wave_mercs in player_data['mercenariesSentPerWave']:
                    for merc in wave_mercs:
                        mercenaries.add(merc)

                data.append({
                    'units': ', '.join(units),
                    'spell': spell,
                    'mercenaries': ', '.join(mercenaries),
                    'game_result': player_data['gameResult']
                })

    return pd.DataFrame(data)

def analyze_significant_factors(match_files, top_n=10):
    data = prepare_data(match_files)

    X = data[['units', 'spell', 'mercenaries']]
    y = data['game_result']

    preprocessor = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'), ['units', 'spell', 'mercenaries'])
        ])

    X_preprocessed = preprocessor.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    feature_names = preprocessor.get_feature_names_out()
    coefficients = model.coef_[0]
    abs_coefficients = abs(coefficients)
    importance = abs_coefficients / abs_coefficients.sum()

    feature_importance = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
    feature_importance = feature_importance.sort_values('Importance', ascending=False).head(top_n)

    plt.figure(figsize=(10, 6))
    plt.bar(feature_importance['Feature'], feature_importance['Importance'])
    plt.xlabel('Feature')
    plt.ylabel('Importance')
    plt.title('Feature Importance')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    p_values = model.p
    significant_features = feature_importance[feature_importance['Feature'].isin(feature_names[p_values < 0.05])]
    print("Significant Features:")
    print(significant_features)

    # Interpret the results and provide recommendations
    print("Recommendations:")
    for _, row in significant_features.iterrows():
        feature = row['Feature']
        importance = row['Importance']
        print(f"- Focus on {feature} (Importance: {importance:.2f})")


files = get_filepaths()
analyze_significant_factors(files)