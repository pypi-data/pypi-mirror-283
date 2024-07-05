from policyengine_it.model_api import *


class household_income_tax_before_refundable_credits(Variable):
    value_type = float
    entity = Household
    label = "tax"
    documentation = "Total tax liability before refundable credits."
    unit = EUR
    definition_period = YEAR
    adds = ["income_tax_before_refundable_credits"]
