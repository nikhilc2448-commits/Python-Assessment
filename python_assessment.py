# Python Assessment – Pandas Behaviour & Debugging

import pandas as pd
import numpy as np

# =========================================================
# SECTION A – Predict the Output
# =========================================================

# Q1
# Prediction:
# Output -> [10, 20, 30]
# Because sub is a slice (copy), changing it will not modify df.
# Pandas raises SettingWithCopyWarning.

print("Q1")

df = pd.DataFrame({'a': [1, 2, 3], 'b': [10, 20, 30]})
sub = df[df['a'] > 1]
sub['b'] = 0

print(df['b'].tolist())

# Actual Output:
# [10, 20, 30]

# Explanation:
# The assignment modifies the sliced DataFrame, not the original.
# Use df.loc[df['a'] > 1, 'b'] = 0 instead.


# ---------------------------------------------------------

# Q2
# Prediction:
# Output -> 5
# Duplicate keys create a many-to-many merge.

print("\nQ2")

left = pd.DataFrame({'k': [1, 1, 2], 'v': ['a', 'b', 'c']})
right = pd.DataFrame({'k': [1, 1, 2], 'w': ['x', 'y', 'z']})

print(len(left.merge(right, on='k')))

# Actual Output:
# 5

# Explanation:
# Key=1 appears twice in both tables, producing 2×2 = 4 rows.
# Key=2 matches once, giving 1 more row.
# Total = 5 rows.


# ---------------------------------------------------------

# Q3
# Prediction:
# {'a': 5, 'b': 2}
# None/NaN group is dropped by default.

print("\nQ3")

d = pd.DataFrame({
    'g': ['a', 'b', None, 'a'],
    'v': [1, 2, 3, 4]
})

print(d.groupby('g')['v'].sum().to_dict())

# Include NaN group
print(d.groupby('g', dropna=False)['v'].sum().to_dict())

# Explanation:
# groupby() ignores missing keys unless dropna=False.


# ---------------------------------------------------------

# Q4
# Prediction:
# Output -> 1
# inplace=True on a column selection will not update the original column
# under Copy-on-Write, so one NaN will remain.

print("\nQ4")

df = pd.DataFrame({'x': [1, np.nan, 3]})

# Original code
df['x'].fillna(0, inplace=True)

print(df['x'].isna().sum())

# Correct version
df = pd.DataFrame({'x': [1, np.nan, 3]})
df['x'] = df['x'].fillna(0)

print(df)

# Explanation:
# Assign the result back to the column instead of using inplace=True.


# ---------------------------------------------------------

# Q5
# Prediction:
# False
# True

print("\nQ5")

a = pd.Series([1, np.nan])
b = pd.Series([1, np.nan])

print((a == b).all())
print(a.equals(b))

# Explanation:
# NaN == NaN is False.
# equals() correctly treats NaN in the same position as equal.
# Use equals() to compare datasets.


# =========================================================
# SECTION B – Write the Code
# =========================================================

# Q6
print("\nQ6")

df = pd.DataFrame({
    'payment': ['Net banking', 'NetBanking', ' netbanking ', 'NET BANKING']
})

# strip() + title() is not enough because internal spaces remain.
df['payment'] = (
    df['payment']
    .str.strip()
    .str.lower()
    .str.replace(" ", "", regex=False)
    .replace({'netbanking': 'Net Banking'})
)

print(df)


# ---------------------------------------------------------

# Q7
print("\nQ7")

left = pd.DataFrame({
    'customer_id': [1, 1, 2, 3],
    'name': ['A', 'A', 'B', 'C']
})

right = pd.DataFrame({
    'customer_id': [1, 1, 2],
    'city': ['BLR', 'MYS', 'HYD']
})

merged = left.merge(right, on='customer_id', how='inner')

print("Left shape:", left.shape)
print("Right shape:", right.shape)
print("Merged shape:", merged.shape)

print("\nDuplicate keys in Left:")
print(left[left.duplicated('customer_id', keep=False)])

print("\nDuplicate keys in Right:")
print(right[right.duplicated('customer_id', keep=False)])

# Validate merge
try:
    left.merge(right, on='customer_id', validate='one_to_one')
except Exception as e:
    print("\nValidation Error:")
    print(e)

# Explanation:
# I first checked the shape of both tables and the merged result.
# Then I looked for duplicate customer_id values in both tables.
# Finally, I used validate='one_to_one' to confirm that the merge
# was becoming many-to-many because of duplicate keys.


# ---------------------------------------------------------

# Q8
print("\nQ8")


def column_summary(df, columns):
    result = []

    for col in columns:
        if col in df.columns:
            result.append({
                "Column": col,
                "Missing": df[col].isna().sum(),
                "Distinct": df[col].nunique(dropna=True),
               "DataType": df[col].dtype
            })
        else:
            result.append({
                "Column": col,
                "Missing": "Column Not Found",
                "Distinct": "-",
                "DataType": "-"
            })

    return pd.DataFrame(result)


sample = pd.DataFrame({
    "name": ["A", "B", None],
    "age": [22, 23, 23]
})

print(column_summary(sample, ["name", "age", "salary"]))


# =========================================================
# SECTION C – Debugging
# =========================================================

# Q9
print("\nQ9")


def margin(df):
    df = df.copy()

    df['margin'] = np.where(
        df['sales'] == 0,
        np.nan,
        (df['profit'] / df['sales']) * 100
    )

    return df


sales_df = pd.DataFrame({
    "profit": [100, 50, 25],
    "sales": [200, 0, 50]
})

print(margin(sales_df))

# Explanation:
# Division by zero creates inf.
# Replace those cases with NaN using np.where().


# ---------------------------------------------------------

# Q10

print("\nQ10")
print("1. Check the dataframe shape.")
print("2. Check missing values using isna().sum().")
print("3. Check duplicate records and duplicate keys.")

# Explanation:
# Shape tells me if rows increased unexpectedly.
# Missing values can affect totals.
# Duplicate keys usually cause incorrect merge results.