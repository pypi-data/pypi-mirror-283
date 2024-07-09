from policyengine_it.model_api import *


class household_id(Variable):
    value_type = float
    entity = Household
    label = "Household ID"
    unit = EUR
    definition_period = ETERNITY
