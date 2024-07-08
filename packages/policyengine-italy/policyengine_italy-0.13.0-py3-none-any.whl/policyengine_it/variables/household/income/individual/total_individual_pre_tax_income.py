from policyengine_it.model_api import *

label = "Earnings"


class total_individual_pre_tax_income(Variable):
    # In a more built-out model, there would be different categories of income
    # that all form part of this variable. However, the existing model only contains
    # 'gross_income' (for head of household) and 'spouse income' (for spouse).
    # This will be used as the stand-in for that, even though it only includes one
    # subset, 'employment_income'.
    value_type = float
    entity = Person
    label = "Total individual pre-tax income"
    unit = EUR
    documentation = "Income from gainful employment"
    definition_period = YEAR
    adds = ["employment_income"]
