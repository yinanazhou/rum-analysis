import os
import pandas as pd

# Define the input directory and output file name
input_dir = './data/'
output_file = 'dataset.csv'

# Create an empty DataFrame to store the data
combined_data = pd.DataFrame()

# Loop through all the CSV files in the input directory
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith('.csv'):
        # Read the CSV file into a DataFrame
        data = pd.read_csv(os.path.join(input_dir, filename), index_col=False)
        # Append the data to the combined DataFrame
        combined_data = combined_data.append(data, ignore_index=True)
        print(filename)

# Write the combined data to a new CSV file
combined_data.to_csv(output_file, index=False)
