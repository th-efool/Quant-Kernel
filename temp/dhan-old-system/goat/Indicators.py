import pandas as pd
def calculate_mcginley(data, column, period):
    """
    Calculate the McGinley Indicator for the given data.
    """
    # Ensure data is not empty and the column exists
    if data.empty or column not in data.columns:
        raise ValueError(f"Data for {column} is missing or empty.")

    mcginley = pd.Series(index=data.index, dtype='float64')  # Initialize as a Series with NaN
    mcginley.iloc[0] = data[column].iloc[0]  # Set the first value equal to the column's first value

    for i in range(1, len(data)):
        mcginley.iloc[i] = mcginley.iloc[i - 1] + (
                (data[column].iloc[i] - mcginley.iloc[i - 1]) /
                (period * (data[column].iloc[i] / mcginley.iloc[i - 1]) ** 4)
        )
    return mcginley
