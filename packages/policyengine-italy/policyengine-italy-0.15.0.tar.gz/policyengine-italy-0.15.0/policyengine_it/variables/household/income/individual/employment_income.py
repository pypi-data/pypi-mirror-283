from policyengine_it.model_api import *

label = "Earnings"


class employment_income(Variable):
    # In a more built-out model, there would be multiple different
    # categories of income that all add together to form
    # total_individual_pre_tax_income. However, the existing model does not
    # differentiate, so we'll assume all income is employment_income
    value_type = float
    entity = Person
    label = "All income gained from standard employment"
    unit = EUR
    documentation = "Income from standard employment"
    definition_period = YEAR
