import numpy as np

def create_input_data(df, last_n_hours=24):
    last_data = df[-last_n_hours:]
    X = last_data.values
    return X

def predict_next_day(models, df):
    predictions = {}
    last_n_hours = 24
    X = create_input_data(df, last_n_hours)

    predictions['xgb'] = models['xgb'].predict(X)
    predictions['rf'] = models['rf'].predict(X)
    predictions['svm'] = models['svm'].predict(X)

    X_reshaped = X.reshape((1, X.shape[0], X.shape[1]))
    predictions['gru'] = models['gru'].predict(X_reshaped).flatten()
    predictions['lstm'] = models['lstm'].predict(X_reshaped).flatten()

    return predictions
