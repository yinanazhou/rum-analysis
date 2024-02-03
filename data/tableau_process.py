import pandas as pd
import pycountry

# Read the CSV file
df = pd.read_csv("./data/preprocessed.csv")

# Create a mapping dictionary for country names to ISO-3166 country codes
country_mapping = {}
for country in pycountry.countries:
    country_mapping[country.name] = country.alpha_2

# Map the values in the "Location" column to ISO-3166 country codes
df["Country"] = df["Location"].map(country_mapping)

# Save the updated DataFrame to a new CSV file
df.to_csv("./data/preprocessed.csv", index=False)
