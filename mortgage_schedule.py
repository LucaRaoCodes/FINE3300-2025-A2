# mortgage_schedule.py
# FINE3300 - Assignment 2, Part A: Loan Amortization and Payment Schedule
# Author: Luca Rao

import pandas as pd
import matplotlib.pyplot as plt

# Q1: Define a class for mortgage payment calculations
class MortgagePayment:
    """
    Class to calculate mortgage payments and generate full payment schedules
    for different payment frequencies.
    """
    def __init__(self, quoted_rate, amortization_years):
        """
        Initialize the mortgage with annual quoted interest rate and
        amortization period in years.
        :param quoted_rate: Annual interest rate as a decimal (e.g., 0.055 for 5.5%)
        :param amortization_years: Mortgage term in years
        """
        self.quoted_rate = quoted_rate
        self.amortization_years = amortization_years

    # Q2: Private method to calculate Present Value of Annuity factor
    def _pva(self, r, n):
        """
        Present Value of Annuity factor.
        :param r: periodic interest rate
        :param n: total number of periods
        :return: annuity factor
        """
        return (1 - (1 + r) ** -n) / r

    # Q3: Calculate payment amounts for six payment options
    def payments(self, principal):
        """
        Calculate mortgage payment amounts for monthly, semi-monthly, bi-weekly,
        weekly, accelerated bi-weekly, and accelerated weekly frequencies.
        :param principal: Loan principal amount
        :return: Dictionary of payment amounts keyed by frequency
        """
        periods = {
            "monthly": 12,
            "semi_monthly": 24,
            "bi_weekly": 26,
            "weekly": 52
        }

        results = {}
        for key, m in periods.items():
            # Convert annual rate to effective rate per period
            r_period = (1 + self.quoted_rate / 2) ** (2 / m) - 1
            n_periods = self.amortization_years * m
            results[key] = principal / self._pva(r_period, n_periods)

        # Calculate accelerated payment options
        results["acc_bi_weekly"] = results["monthly"] / 2
        results["acc_weekly"] = results["monthly"] / 4

        # Round payments to 2 decimal places
        for k in results:
            results[k] = round(results[k], 2)

        return results

    # Q4: Generate full payment schedule as a pandas DataFrame
    def generate_schedule(self, principal, frequency):
        """
        Generate a full mortgage payment schedule for a given frequency.
        Columns: Period, Starting Balance, Interest, Payment, Ending Balance
        :param principal: Loan principal amount
        :param frequency: Payment frequency (e.g., 'monthly', 'bi_weekly', etc.)
        :return: pandas DataFrame of payment schedule
        """
        # Map frequency to periods per year
        freq_map = {
            "monthly": 12,
            "semi_monthly": 24,
            "bi_weekly": 26,
            "weekly": 52,
            "acc_bi_weekly": 12,   # initially monthly equivalent
            "acc_weekly": 12
        }

        # Adjust periods per year for accelerated frequencies
        if frequency == "acc_bi_weekly":
            periods_per_year = 26
        elif frequency == "acc_weekly":
            periods_per_year = 52
        else:
            periods_per_year = freq_map[frequency]

        # Get payment amount for chosen frequency
        payment_amount = self.payments(principal)[frequency]

        # Effective interest rate per period
        r_period = (1 + self.quoted_rate / 2) ** (2 / periods_per_year) - 1
        n_periods = self.amortization_years * periods_per_year
        balance = principal

        # Build schedule row by row
        schedule = []
        for period in range(1, n_periods + 1):
            interest = round(balance * r_period, 2)
            principal_paid = round(payment_amount - interest, 2)
            ending_balance = round(balance - principal_paid, 2)
            schedule.append([period, balance, interest, payment_amount, ending_balance])
            balance = ending_balance
            if balance < 0:  # Avoid negative balances
                balance = 0

        df = pd.DataFrame(schedule, columns=[
            "Period", "Starting Balance", "Interest", "Payment", "Ending Balance"
        ])
        return df

# --- Main Program ---
if __name__ == "__main__":
    # Q5: Prompt user for mortgage details
    principal = float(input("Enter principal amount: "))
    rate = float(input("Enter quoted annual rate (e.g., 5.5 for 5.5%): ")) / 100
    years = int(input("Enter amortization period in years: "))

    mortgage = MortgagePayment(rate, years)
    frequencies = ["monthly", "semi_monthly", "bi_weekly", "weekly", "acc_bi_weekly", "acc_weekly"]

    # Q6: Save all schedules to a single Excel file with multiple worksheets
    excel_filename = "MortgageSchedules.xlsx"
    with pd.ExcelWriter(excel_filename) as writer:
        for freq in frequencies:
            df = mortgage.generate_schedule(principal, freq)
            sheet_name = freq.replace("_", " ").title()
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"All schedules saved to {excel_filename}")

    # Q7: Plot mortgage balance decline for all frequencies
    plt.figure(figsize=(10, 6))
    for freq in frequencies:
        df = mortgage.generate_schedule(principal, freq)
        plt.plot(df["Period"], df["Ending Balance"], label=freq.replace("_", " ").title())
    plt.title("Mortgage Balance Decline Over Time")
    plt.xlabel("Period")
    plt.ylabel("Ending Balance ($)")
    plt.legend()
    plt.grid(True)
    png_filename = "MortgageBalanceDecline.png"
    plt.savefig(png_filename)
    print(f"Graph saved as {png_filename}")
    plt.show()

