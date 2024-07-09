from policyengine_it.model_api import *


class non_refundable_tax_credits(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    unit = EUR
    label = "Total value of national non-refundable tax credits"
    adds = "gov.ade.credits.non_refundable"
