import pandas as pd
import math

class SIPCalculator():
    def __init__(self):
        self.investment_dataframe = None
        self.final_investment_amount = -1

    def validate_dataframe(self, dataframe):
        if not isinstance(dataframe, pd.DataFrame):
            raise Exception("Not a pandas dataframe.")
        
        df_columns = dataframe.columns
        required_columns = ['amount', 'rate_of_interest', 'number_of_years']
        
        if len(df_columns) != 3:
            raise Exception("The dataframe should contain 3 columns (amount, rate_of_interest, number_of_years) - found {0}".format(len(df_columns)))

        for column in required_columns:
            if column not in df_columns:
                raise Exception("The dataframe is missing '{0}' column. Following columns were found - {1}".format(column, str(list(df_columns))))

        # check if all values are numeric
        try:
            pd.to_numeric(dataframe['amount'])
            pd.to_numeric(dataframe['rate_of_interest'])
            pd.to_numeric(dataframe['number_of_years'])
        except:
            raise Exception("The values are not numeric.")

        return

    def calculate_total_investment(self):
        total_investment_term = self.investment_dataframe['number_of_years'].sum()
        final_investment_amount, current_year = 0, 0

        for index, row in self.investment_dataframe.iterrows():
            amount, rate_perc, years = row
            current_year += years
            monthly_compounding_rate = 1 + float(rate_perc) / 1200
            cur_investment = amount * monthly_compounding_rate * (math.pow(monthly_compounding_rate, years * 12) - 1) / (monthly_compounding_rate - 1)
            final_investment_amount += (cur_investment * math.pow(monthly_compounding_rate, (total_investment_term - current_year) * 12))

        return final_investment_amount

        
    def update_investments(self, csv_location, is_header_present = True):
        header = None
        if is_header_present:
            header = 0

        dataframe = pd.read_csv(csv_location, header = header)
        self.validate_dataframe(dataframe)
        self.investment_dataframe = dataframe
        self.final_investment_amount = self.calculate_total_investment()

        return

    def get_investment_value(self):
        return self.final_investment_amount