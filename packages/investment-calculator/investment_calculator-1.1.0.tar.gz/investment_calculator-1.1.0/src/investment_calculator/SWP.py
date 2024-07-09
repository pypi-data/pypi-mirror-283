import pandas as pd
from .NumeralSystem import get_indian_numeral

class SWPCalculator:
    def __init__(self, initial_investment_amount, rate_of_interest, initial_monthly_withdrawal, inflation_rate, number_of_years):
        self.initial_investment_amount = initial_investment_amount
        self.rate_of_interest = rate_of_interest
        self.initial_monthly_withdrawal = initial_monthly_withdrawal
        self.inflation_rate = inflation_rate
        self.number_of_years = number_of_years

        self.year = []
        self.yearly_start_amount = []
        self.yearly_withdrawal = []
        self.yearly_final_amount = []

    def get_calculated_swp(self):
        current_amount = self.initial_investment_amount
        current_withdrawal = self.initial_monthly_withdrawal

        for yr in range(self.number_of_years):
            self.year.append(yr + 1)
            self.yearly_start_amount.append(get_indian_numeral(int(current_amount)))
            self.yearly_withdrawal.append(get_indian_numeral(int(current_withdrawal * 12)))
            
            current_amount = current_amount * (1 + float(self.rate_of_interest) / 100) - current_withdrawal * 12
            self.yearly_final_amount.append(get_indian_numeral(int(current_amount)))
            current_withdrawal *= (1 + float(self.inflation_rate) / 100)

            if current_amount < 0:
                break

        swp_dataframe = pd.DataFrame({'year': self.year, 'start_amount': self.yearly_start_amount, 'withdrawal': self.yearly_withdrawal, 'final_amount': self.yearly_final_amount})
        return swp_dataframe



