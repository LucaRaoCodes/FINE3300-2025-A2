# cpi_analysis.py
# FINE3300 - Assignment 2, Part B: Consumer Price Index
# Author: Luca Rao

import pandas as pd
import glob
import os

# Q1: Load and combine individual CPI CSV files into a single DataFrame
def load_cpi_data(data_folder):
    all_files = glob.glob(os.path.join(data_folder, "*.csv"))
    combined = pd.DataFrame()

    for file in all_files:
        jurisdiction = os.path.splitext(os.path.basename(file))[0]
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()  # Remove any extra spaces from column names
        if "Item" not in df.columns:
            df.rename(columns={df.columns[0]: "Item"}, inplace=True)
        # Convert from wide format to long format (Month as variable, CPI as value)
        df_long = df.melt(id_vars=["Item"], var_name="Month", value_name="CPI")
        df_long["Jurisdiction"] = jurisdiction
        combined = pd.concat([combined, df_long], ignore_index=True)

    return combined[["Item", "Month", "Jurisdiction", "CPI"]]

# Q3: Calculate average month-to-month percent changes for selected items
def calculate_monthly_changes(df, items):
    changes = {}
    for jurisdiction in df["Jurisdiction"].unique():
        subset = df[df["Jurisdiction"] == jurisdiction]
        avg_changes = {}
        for item in items:
            item_df = subset[subset["Item"] == item].sort_values("Month")
            item_df["CPI"] = pd.to_numeric(item_df["CPI"], errors="coerce")
            pct_change = item_df["CPI"].pct_change().dropna() * 100
            avg_changes[item] = round(pct_change.mean(), 1)
        changes[jurisdiction] = avg_changes
    return pd.DataFrame(changes).T  # Jurisdictions as rows

# Q5: Calculate equivalent salaries in other provinces using December CPI
def calculate_equivalent_salary(df, base_jurisdiction="Ontario", base_salary=100000):
    dec_cpi = df[(df["Month"].str.contains("Dec")) & (df["Item"] == "All-items")]
    base_cpi = dec_cpi[dec_cpi["Jurisdiction"] == base_jurisdiction]["CPI"].values[0]
    salaries = {}
    for _, row in dec_cpi.iterrows():
        salaries[row["Jurisdiction"]] = round(base_salary * row["CPI"] / base_cpi, 2)
    return salaries

# Q6: Calculate nominal and real minimum wages
def calculate_real_min_wage(min_wages_file, cpi_df):
    min_wages = pd.read_csv(min_wages_file)
    min_wages.columns = min_wages.columns.str.strip()
    dec_cpi = cpi_df[(cpi_df["Month"].str.contains("Dec")) & (cpi_df["Item"] == "All-items")]
    real_wages = {}
    for _, row in min_wages.iterrows():
        jurisdiction = row["Province"]
        nominal = row["MinimumWage"]
        cpi = dec_cpi[dec_cpi["Jurisdiction"] == jurisdiction]["CPI"].values[0]
        real_wages[jurisdiction] = round(nominal / cpi * 100, 2)
    return min_wages, real_wages

# Q7: Compute annual % change in CPI for 'Services' for each jurisdiction
def annual_service_inflation(df):
    results = {}
    for jurisdiction in df["Jurisdiction"].unique():
        subset = df[(df["Jurisdiction"] == jurisdiction) & (df["Item"].str.contains("Services"))].sort_values("Month")
        subset["CPI"] = pd.to_numeric(subset["CPI"], errors="coerce")
        if subset.empty:
            results[jurisdiction] = None  # No data for this jurisdiction
            continue
        first = subset["CPI"].iloc[0]
        last = subset["CPI"].iloc[-1]
        results[jurisdiction] = round((last - first) / first * 100, 1)
    return results

def main():
    data_folder = "data"

    # Q1: Load and combine CPI data
    cpi_df = load_cpi_data(data_folder)

    # Q2: Print first 12 rows of combined CPI data
    print("First 12 rows of combined CPI data:")
    print(cpi_df.head(12))
    print("\n")

    # Q3: Average month-to-month % changes for selected items
    items_of_interest = ["Food", "Shelter", "All-items excluding food and energy"]
    avg_changes = calculate_monthly_changes(cpi_df, items_of_interest)
    avg_changes = avg_changes.drop(index=["MinimumWages"], errors="ignore")  # Remove non-province rows if any
    print("Average month-to-month % change:")
    print(avg_changes)
    print("\n")

    # Q4: Province with highest average change
    highest_avg_change_jurisdiction = avg_changes.mean(axis=1).idxmax()
    print(f"Province with highest average change: {highest_avg_change_jurisdiction}")
    print("\n")

    # Q5: Equivalent salaries to $100,000 in Ontario
    salaries = calculate_equivalent_salary(cpi_df, base_jurisdiction="Ontario", base_salary=100000)
    print("Equivalent salaries based on December CPI:")
    for k, v in salaries.items():
        print(f"{k}: ${v}")
    print("\n")

    # Q6: Nominal and real minimum wages
    min_wages_file = os.path.join(data_folder, "MinimumWages.csv")
    min_wages, real_wages = calculate_real_min_wage(min_wages_file, cpi_df)
    print("Nominal minimum wages:")
    print(min_wages)
    print("\nReal minimum wages:")
    for k, v in real_wages.items():
        print(f"{k}: ${v}")
    highest_real = max(real_wages, key=real_wages.get)
    print(f"Province with highest real minimum wage: {highest_real}")
    print("\n")

    # Q7: Annual % change in CPI for Services
    service_inflation = annual_service_inflation(cpi_df)
    service_inflation_filtered = {k: v for k, v in service_inflation.items() if k != "MinimumWages" and v is not None}

    print("Annual % change in CPI for Services:")
    for k, v in service_inflation_filtered.items():
        print(f"{k}: {v}%")

    # Q8: Region with highest services inflation
    highest_inflation = max(service_inflation_filtered, key=service_inflation_filtered.get)
    print(f"Region with highest services inflation: {highest_inflation}")

if __name__ == "__main__":
    main()

