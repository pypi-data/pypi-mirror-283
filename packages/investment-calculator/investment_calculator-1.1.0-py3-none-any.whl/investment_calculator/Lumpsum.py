import math

class LumpsumCalculator:
    def __init__(self, amount, rate_of_interest, investment_term_in_years):
        self.amount = amount
        self.rate_of_interest = rate_of_interest
        self.investment_term_in_years = investment_term_in_years

        compounding_rate = 1 + float(self.rate_of_interest) / 100
        self.final_investment_amount = self.amount * math.pow(compounding_rate, self.investment_term_in_years)