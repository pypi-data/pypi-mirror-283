from policyengine_it.model_api import *


class individual_net_income(Variable):
    value_type = float
    entity = Person
    label = "Individual net income"
    unit = EUR
    definition_period = YEAR
    adds = ["total_individual_pre_tax_income"]
    subtracts = ["income_tax", "insurance_and_pensions"]
