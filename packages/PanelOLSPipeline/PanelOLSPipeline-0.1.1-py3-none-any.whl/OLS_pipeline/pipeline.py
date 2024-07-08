import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np

def preprocess_data(df, normalize_cols, weight_dict, interaction_pairs):
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # Normalize the specified columns
    scaler = MinMaxScaler()
    df[normalize_cols] = scaler.fit_transform(df[normalize_cols])

    # Calculate the weighted average for the impact measure
    df['COVID_Impact_Measure'] = sum(df[col] * weight for col, weight in weight_dict.items())

    # Create interaction terms
    for (col1, col2) in interaction_pairs:
        df[f'Interaction_{col1}_{col2}'] = df[col1] * df[col2]

    df.set_index(['Country', 'Year'], inplace=True)

    # Scale the data
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

    return X_scaled

def fit_models(X_scaled, dependent_var, independent_vars):
    y = X_scaled[dependent_var]
    X = X_scaled[independent_vars]
    X = sm.add_constant(X)

    # Check and remove variables causing multicollinearity
    while True:
        vif_data = calculate_vif(X)
        max_vif = vif_data['VIF'].max()
        if max_vif > 10 or (vif_data['VIF'] == float('inf')).any():
            max_vif_feature = vif_data.sort_values('VIF', ascending=False)['feature'].iloc[0]
            if max_vif_feature == 'const':  # Skip removing 'const' if it's causing issues
                break
            independent_vars.remove(max_vif_feature)
            X = X_scaled[independent_vars]
            X = sm.add_constant(X)
        else:
            break

    # Check for minimum data requirements
    if y.isnull().all() or X.isnull().all().all():
        raise ValueError("Insufficient data to fit the model. Check for missing values or data structure issues.")

    # Fixed effects model
    fixed_effects_model = PanelOLS(y, X, entity_effects=True, check_rank=False)
    fixed_effects_results = fixed_effects_model.fit(cov_type='robust')

    # Random effects model
    try:
        random_effects_model = RandomEffects(y, X).fit(cov_type='heteroskedastic')
    except ZeroDivisionError as e:
        raise ZeroDivisionError("Random Effects model fitting encountered a division by zero error. Check the panel data structure.") from e

    return fixed_effects_results, random_effects_model

def calculate_vif(X):
    vif_data = pd.DataFrame()
    vif_data['feature'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif_data

def pipeline(data_path, dependent_var, independent_vars, normalize_cols, weight_dict, interaction_pairs):
    df = pd.read_csv(data_path)
    X_scaled = preprocess_data(df, normalize_cols, weight_dict, interaction_pairs)

    # Update independent_vars to include dynamically created interaction terms
    for (col1, col2) in interaction_pairs:
        interaction_term = f'Interaction_{col1}_{col2}'
        if interaction_term not in independent_vars:
            independent_vars.append(interaction_term)

    fixed_effects_results, random_effects_model = fit_models(X_scaled, dependent_var, independent_vars)
    vif_data = calculate_vif(sm.add_constant(X_scaled[independent_vars]))

    return fixed_effects_results, random_effects_model, vif_data

