import pandas as pd
import numpy as np

# ---------------------------------------------------
# 1. Load Raw CSV
# ---------------------------------------------------
input_file = "EXP_1_120slpm_10per_90sec_2222_25-08-22_10-58-35.csv"
df = pd.read_csv(input_file)

print("Original Shape:", df.shape)

# ---------------------------------------------------
# 2. Fix Timestamp Format (mm:ss.ms → seconds)
# ---------------------------------------------------
def convert_timestamp(x):
    try:
        m, s = x.split(":")
        return float(m) * 60 + float(s)
    except:
        return np.nan

df["Timestamp_sec"] = df["Timestamp"].astype(str).apply(convert_timestamp)
df.drop(columns=["Timestamp"], inplace=True)

# ---------------------------------------------------
# 3. Remove Empty or Useless Columns
# ---------------------------------------------------
df = df.dropna(axis=1, how="all")                  # remove fully empty columns
df = df.loc[:, df.apply(pd.Series.nunique) > 1]    # remove constant columns

# ---------------------------------------------------
# 4. Convert numeric columns automatically
# ---------------------------------------------------
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

# ---------------------------------------------------
# 5. Handle Missing Values
# ---------------------------------------------------
df = df.ffill().bfill()    # forward + backward fill

# ---------------------------------------------------
# 6. Remove Duplicate Rows
# ---------------------------------------------------
df = df.drop_duplicates()

# ---------------------------------------------------
# 7. Save Cleaned CSV (for dashboard)
# ---------------------------------------------------
output_file = "cleaned_data.csv"
df.to_csv(output_file, index=False)

print("\nData Cleaning Completed!")
print("Cleaned Data Shape:", df.shape)
print("File Saved As:", output_file)