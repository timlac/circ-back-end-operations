import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Assuming you have the true labels in 'y_true' and the predicted labels in 'y_pred'
# Replace 'y_true' and 'y_pred' with the actual true and predicted labels of your classifier

# Create the confusion matrix
conf_matrix = confusion_matrix(y_true, y_pred)

# Convert the confusion matrix to a DataFrame for better visualization
conf_matrix_df = pd.DataFrame(conf_matrix, index=range(44), columns=range(44))

# Set up a smaller heatmap with reduced font size for annotations
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_df, annot=True, fmt='d', cmap='Blues', annot_kws={"size": 8})
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.title('Confusion Matrix')
plt.show()
