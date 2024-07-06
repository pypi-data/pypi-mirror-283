# lisite_lib/examples/example_IForest.py

import pandas as pd
from lisite_lib.algorithms.IForest import IsolationForest
from lisite_lib.utils.consts import _IFOREST_ANOMALY_THRESHOLD
from sklearn.preprocessing import LabelEncoder

# Reading Shuttle Data
shuttle_data_path = '../data/shuttle.csv'
shuttle_data = pd.read_csv(shuttle_data_path)

X_shuttle = shuttle_data.iloc[:, :-1]
y_shuttle = shuttle_data.iloc[:, -1]

# Coding the label columns
label_encoder = LabelEncoder()
y_shuttle_encoded = label_encoder.fit_transform(y_shuttle)

# Initialising the Isolation Forest model
sample_size = 256
n_trees = 100
isolation_forest_shuttle = IsolationForest(sample_size=sample_size, n_trees=n_trees)

# Training Models
isolation_forest_shuttle.fit(X_shuttle)

predictions_shuttle, scores_shuttle = isolation_forest_shuttle.predict(X_shuttle, _IFOREST_ANOMALY_THRESHOLD)

output_shuttle = pd.DataFrame({
    'Scores': scores_shuttle.flatten(),
    'Predictions': predictions_shuttle,
    'Actual': y_shuttle_encoded
})

print(output_shuttle.head(30))





