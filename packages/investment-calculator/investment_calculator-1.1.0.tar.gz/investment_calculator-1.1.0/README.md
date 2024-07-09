# InvestmentCalculatorPackage
## Introduction

This python package provides simple functions to calculate investment returns for SIP (Systematic Investment Plan) and Lumpsum investments. It aims to help users easily compute returns without needing to perform complex calculations manually.

## Installation

You can install the `investment_calculator` package via pip:

```bash
pip install investment_calculator
```

## Usage

### Calculating SIP Returns

A systematic investment plan (SIP) is an investment vehicle offeredto investors, allowing them to invest small amounts periodically instead of lumpsums. The frequency of investment is usually weekly, monthly or quarterly.

To calculate returns for SIP investments:

First, prepare a CSV file with columns: amount, rate_of_interest, and number_of_years containing investment details. Here's an example:

```csv
amount,rate_of_interest,number_of_years
20000,12,8
30000,10,15
```
The above csv file indicates that an investment of INR 20,000 was made every month at 12% per annum for the first 8 years, and then, an amount INR 30,000 was invested monthly at 10% per annum for the next 15 years. 

Next, use the SIPCalculator class to process this CSV:

```python
from investment_calculator import SIPCalculator

sip = SIPCalculator()
location = '/home/user/investment.csv'
sip.update_investments(csv_location = location)
print("Total Investment Value: {0}".format(str(sip.final_investment_amount))
```

### Calculating Lumpsum Returns

A lumpsum investment in mutual funds is a one-time payment made in full at the beginning of an investment period. It is a single, large payment made upfront, without any subsequent payments.

To calculate returns for Lumpsum investments:

```python
from investment_calculator import LumpsumCalculator

lumpsum = LumpsumCalculator(amount = 1_000_000, rate_of_interest = 8, investment_term_in_years = 15)
print("Total Investment Value: {0}".format(str(lumpsum.final_investment_amount))
```

Update the values of the parameters for your needs.

### Calculating SWP

SWP (Systematic Withdrawal Plan) is a feature offered to investors where the investor can withdraw a fixed amount of money at regular intervals (monthly, quarterly, etc.) from their investment.

To calculate returns for Lumpsum investments:
```python
from investment_calculator import *

swp = SWPCalculator(
    initial_investment_amount = 1_000_000,
    rate_of_interest = 7,
    initial_monthly_withdrawal = 5_000,
    inflation_rate = 7,
    number_of_years = 30
)

investment_df = swp.get_calculated_swp()
print(investment_df)
```

This functions returns a dataframe which tells you how much money remains of your investment at the end of each year. It also accounts for inflation.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.