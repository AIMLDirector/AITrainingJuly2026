from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder

import pandas as pd
import numpy as np
# Sample data
data = ['cat', 'dog', 'cat', 'mouse', 'dog']
# Label Encoding
label_encoder = LabelEncoder()
labeled_data = label_encoder.fit_transform(data)    
print("Label Encoded Data:", labeled_data)
# One-Hot Encoding

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(np.array(data).reshape(-1, 1))
print("One-Hot Encoded Data:\n", encoded)


# Ordinal Encoding
ordinal_encoder = OrdinalEncoder()
ordinal_encoded = ordinal_encoder.fit_transform(np.array(data).reshape(-1, 1))
print("Ordinal Encoded Data:\n", ordinal_encoded)

