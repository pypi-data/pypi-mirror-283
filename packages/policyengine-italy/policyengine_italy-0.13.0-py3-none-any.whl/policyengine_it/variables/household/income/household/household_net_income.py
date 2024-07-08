from policyengine_it.model_api import *


class household_net_income(Variable):
    value_type = float
    entity = Household
    label = "net income"
    unit = EUR
    definition_period = YEAR
    adds = ["household_market_income", "refundable_tax_credits"]
    subtracts = [
        "household_income_tax_before_refundable_credits",
        "insurance_and_pensions",
    ]
