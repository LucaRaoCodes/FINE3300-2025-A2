# mortgage_schedule.py
# FINE3300 - Assignment 2, Part A
# Author: Luca Rao

import pandas as pd
import matplotlib.pyplot as plt

class MortgagePayment:
    def __init__(self, quoted_rate, amortization_years):
        self.quoted_rate = quoted_rate
        self.amortization_years = amortization_years

    def _pva(self, r, n):
        """Present value of annuity factor"""
        return (1 - (1 + r) ** -n) / r

    def payments(self, principal):
        periods = {
            "monthly": 12,
            "semi_monthly": 24,
            "bi_weekly": 26,
            "weekly": 52
        }

        results = {}
        for key, m in periods.items():
            r_period = (1 + self.quoted_rate / 2) ** (2 / m) - 1
            n_periods = self.amortization_years * m
            results[key] = principal / self._pva(r_period, n_periods)

        results["acc_bi_weekly"] = results["monthly"] / 2
        results["acc_weekly"] = results["monthly"] / 4

        # Round
        for k in results:
            results[k] = round(results[k], 2)

        return results

    def generate_schedule(self, principal, frequency):
        """Generate a full payment schedule DataFrame for a given frequency"""
        freq_map = {
            "monthly": 12,
            "semi_monthly": 24,
            "bi_weekly": 26,
            "weekly": 52,
            "acc_bi_weekly": 12,   # Accelerated uses monthly equivalent
            "acc_weekly": 12       # Adjusted below in payment calculation
        }

        if frequency in ["acc_bi_weekly"]:
            periods_per_year = 26
        elif frequency in ["acc_weekly"]:
            periods_per_year = 52
        else:
            periods_per_year = freq_map[frequency]

        payment_amount = self.payments(principal)[frequency]
        r_period = (1 + self.quoted_rate / 2) ** (2 / periods_per_year) - 1
        n_periods = self.amortization_years * periods_per_year
        balance = principal

        schedule = []
        for period in range(1, n_periods + 1):
            interest = round(balance * r_period, 2)
            principal_paid = round(payment_amount - interest, 2)
            ending_balance = round(balance - principal_paid, 2)
            schedule.append([period, balance, interest, payment_amount, ending_balance])
            balance = ending_balance
            if balance < 0:  # Safety to avoid negative balances
                balance = 0

        df = pd.DataFrame(schedule, columns=[
            "Period", "Starting Balance", "Interest", "Payment", "Ending Balance"
        ])
        return df


# --- Main program ---
if __name__ == "__main__":
    principal = float(input("Enter principal amount: "))
    rate = float(input("Enter quoted annual rate (e.g., 5.5 for 5.5%): ")) / 100
    years = int(input("Enter amortization period in years: "))

    mortgage = MortgagePayment(rate, years)
    frequencies = ["monthly", "semi_monthly", "bi_weekly", "weekly", "acc_bi_weekly", "acc_weekly"]

    # Save all schedules to Excel
    excel_filename = "MortgageSchedules.xlsx"
    with pd.ExcelWriter(excel_filename) as writer:
        for freq in frequencies:
            df = mortgage.generate_schedule(principal, freq)
            sheet_name = freq.replace("_", " ").title()
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"All schedules saved to {excel_filename}")

    # Plot balance decline
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
