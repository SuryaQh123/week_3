"""
sales_analysis.py
------------------
Week 3 Project: Sales Data Analysis

What this script does:
1. Loads sales data from a CSV file (sales_data.csv)
2. Explores the dataset (shape, columns, data types)
3. Cleans the data (handles missing values / duplicates, just in case)
4. Calculates key metrics: total revenue, best-selling product, average order
   value, sales by region, and top customers
5. Prints a clean, readable report to the terminal AND saves the same
   report to analysis_report
"""

import pandas as pd


# DAY 1 - Load the data
# pandas.read_csv() reads a CSV file the same way Excel opens a spreadsheet.
# Every column becomes a "Series" and the whole table becomes a "DataFrame".
def load_data(file_path):
    print(f"Loading data from '{file_path}'...")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} rows successfully.\n")
    return df



# DAY 2 - Explore the data
# Before doing anything with data, it's good practice to actually look at it:
# how many rows/columns are there, what type is each column, and what does
# a sample of the data look like?
def explore_data(df):
    print("=" * 60)
    print("STEP 1: EXPLORING THE DATASET")
    print("=" * 60)

    print(f"\nShape of dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    print("\nColumn names and data types:")
    print(df.dtypes)

    print("\nFirst 5 rows of the dataset:")
    print(df.head())

    print("\nBasic statistics for numeric columns:")
    print(df.describe())
    print()


# DAY 3 - Clean the data
# Real-world data is often messy - missing values, duplicate rows, wrong
# data types, etc. This function checks for those problems and fixes them.
# Even if this particular dataset turns out clean, it's good habit to always
# run these checks rather than assume the data is perfect.
def clean_data(df):
    print("=" * 60)
    print("STEP 2: CLEANING THE DATASET")
    print("=" * 60)

    # Check for missing values in each column
    missing_values = df.isnull().sum()
    total_missing = missing_values.sum()

    if total_missing > 0:
        print(f"\nFound {total_missing} missing values:")
        print(missing_values[missing_values > 0])

        # For numeric columns, fill missing values with the column's average
        numeric_cols = df.select_dtypes(include="number").columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                avg_value = df[col].mean()
                df[col] = df[col].fillna(avg_value)
                print(f"Filled missing values in '{col}' with average ({avg_value:.2f})")

        # For text columns, fill missing values with "Unknown"
        text_cols = df.select_dtypes(include="object").columns
        for col in text_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna("Unknown")
                print(f"Filled missing values in '{col}' with 'Unknown'")
    else:
        print("\nNo missing values found. Dataset is already clean on that front.")

    # Check for duplicate rows
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        print(f"\nFound {duplicate_count} duplicate rows. Removing them...")
        df = df.drop_duplicates()
    else:
        print("No duplicate rows found.")

    print()
    return df


# DAY 4 - Analyze the sales data
# This is the core of the project: turning raw rows into useful numbers.
# We calculate more than 3 metrics as required by the brief.
def analyze_sales(df):
    print("=" * 60)
    print("STEP 3: ANALYZING SALES DATA")
    print("=" * 60)

    results = {}

    # Metric 1: Total revenue across all sales
    results["total_revenue"] = df["Total_Sales"].sum()

    # Metric 2: Best-selling product by total revenue
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    results["best_product"] = revenue_by_product.idxmax()
    results["best_product_revenue"] = revenue_by_product.max()
    results["revenue_by_product"] = revenue_by_product

    # Metric 3: Best-selling product by quantity (units sold, not just money)
    quantity_by_product = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
    results["most_units_product"] = quantity_by_product.idxmax()
    results["most_units_sold"] = quantity_by_product.max()

    # Metric 4: Average order value
    results["average_order_value"] = df["Total_Sales"].mean()

    # Metric 5: Highest and lowest single sale
    results["highest_sale"] = df["Total_Sales"].max()
    results["lowest_sale"] = df["Total_Sales"].min()

    # Metric 6: Revenue by region
    results["revenue_by_region"] = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)

    # Metric 7: Top 5 customers by total spend
    results["top_customers"] = df.groupby("Customer_ID")["Total_Sales"].sum().sort_values(ascending=False).head(5)

    return results


# DAY 5 - Build a clean, formatted report

# Instead of just dumping numbers, we format everything nicely so it's
# actually readable. The report is printed to the screen AND saved as a
# markdown file so it can be shared or viewed on GitHub.
def build_report(results, df):
    lines = []
    lines.append("# Sales Data Analysis Report\n")
    lines.append(f"**Total records analyzed:** {len(df)}\n")

    lines.append("## Key Metrics\n")
    lines.append(f"- **Total Revenue:** ₹{results['total_revenue']:,.2f}")
    lines.append(f"- **Average Order Value:** ₹{results['average_order_value']:,.2f}")
    lines.append(f"- **Highest Single Sale:** ₹{results['highest_sale']:,.2f}")
    lines.append(f"- **Lowest Single Sale:** ₹{results['lowest_sale']:,.2f}")
    lines.append(f"- **Best-Selling Product (by revenue):** {results['best_product']} "
                 f"(₹{results['best_product_revenue']:,.2f})")
    lines.append(f"- **Best-Selling Product (by units sold):** {results['most_units_product']} "
                 f"({results['most_units_sold']} units)\n")

    lines.append("## Revenue by Product\n")
    lines.append("| Product | Revenue (₹) |")
    lines.append("|---------|-------------|")
    for product, revenue in results["revenue_by_product"].items():
        lines.append(f"| {product} | {revenue:,.2f} |")
    lines.append("")

    lines.append("## Revenue by Region\n")
    lines.append("| Region | Revenue (₹) |")
    lines.append("|--------|-------------|")
    for region, revenue in results["revenue_by_region"].items():
        lines.append(f"| {region} | {revenue:,.2f} |")
    lines.append("")

    lines.append("## Top 5 Customers by Spend\n")
    lines.append("| Customer ID | Total Spend (₹) |")
    lines.append("|-------------|------------------|")
    for customer, spend in results["top_customers"].items():
        lines.append(f"| {customer} | {spend:,.2f} |")
    lines.append("")

    lines.append("## Insights\n")
    if results["best_product"] == results["most_units_product"]:
        lines.append(
            f"- {results['best_product']} is the clear winner - it leads both in total "
            "revenue and in number of units sold, making it the strongest product overall."
        )
    else:
        lines.append(
            f"- {results['best_product']} brings in the most revenue overall, "
            f"but {results['most_units_product']} sells in the highest quantity, "
            "which suggests these products have different price points and buying patterns."
        )
    top_region = results["revenue_by_region"].idxmax()
    lines.append(f"- {top_region} is the strongest region by total revenue.")
    lines.append(
        f"- The average order value is ₹{results['average_order_value']:,.2f}, "
        "which can be used as a benchmark for future sales targets."
    )

    return "\n".join(lines)


# main function
def main():
    file_path = "sales_data.csv"

    df = load_data(file_path)
    explore_data(df)
    df = clean_data(df)
    results = analyze_sales(df)

    print("=" * 60)
    print("STEP 4: FINAL REPORT")
    print("=" * 60)

    report_text = build_report(results, df)
    print(report_text)

    with open("analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("\nReport saved to analysis_report.md")


if __name__ == "__main__":
    main()
