from policyengine_it.model_api import *


class refundable_tax_credits(Variable):
    value_type = float
    entity = Person
    label = "refundable tax credits"
    unit = EUR
    definition_period = YEAR

    adds = "gov.ade.credits.refundable"
