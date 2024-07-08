from policyengine_it.model_api import *


class household_market_income(Variable):
    value_type = float
    entity = Household
    label = "Household market (pre-tax) income"
    unit = EUR
    definition_period = YEAR
    adds = ["total_individual_pre_tax_income"]
