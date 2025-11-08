# FINE3300-2025-A2
Assignment 2 for FINE 3300 - Loan Amortization and Payment Schedule &amp; Consumer Price Index
# FINE3300 Assignment 2

This repository contains the code and documentation for Assignment 2 of FINE3300. The assignment focuses on working with files, NumPy, Pandas, and Matplotlib to analyze mortgage payment schedules and Consumer Price Index (CPI) data for Canada and its provinces.

## Project Overview

### Part A: Loan Amortization and Payment Schedule
- Implements a `MortgagePayment` class in Python to calculate mortgage payments.  
- Generates full loan amortization schedules, including period, starting balance, interest, payment, and ending balance.  
- Supports six different mortgage terms and saves each schedule as a separate worksheet in a single Excel file.  
- Uses Matplotlib to generate a graph showing the decline of loan balances over time for all six mortgage terms and saves the figure as a PNG file.

### Part B: Consumer Price Index (CPI) Analysis
- Reads and combines 11 CPI data files (Canada overall and 10 provinces) into a single Pandas DataFrame.  
- Computes average month-to-month changes for categories like Food, Shelter, and All-items excluding Food and Energy.  
- Identifies the province with the highest inflation in these categories.  
- Calculates equivalent salaries across provinces using All-items CPI.  
- Analyzes nominal and real minimum wages using CPI adjustments.  
- Computes annual CPI changes for services across Canada and all provinces and identifies regions with the highest inflation.  

## Files
- `mortgage_schedule.py` – Python script for Part A mortgage payment schedules.  
- `MortgageSchedules.xlsx` – Excel file containing all six amortization schedules.  
- `MortgageBalanceDecline.png` – Graph depicting loan balance decline over six mortgage terms.  
- `CPI_analysis.py` – Python script for Part B CPI analysis.  
- CPI CSV files – Monthly CPI data for Canada and provinces.  
- `MinimumWages.csv` – Minimum wage data for Canadian provinces.

## Usage
1. Run `mortgage_schedule.py` to generate amortization schedules and the balance decline graph.  
2. Run `CPI_analysis.py` to perform CPI analysis and minimum wage calculations.  
3. Results are saved as Excel files and PNG figures for reference.
