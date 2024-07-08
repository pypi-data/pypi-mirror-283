from policyengine_it.model_api import *


class count_dependents(Variable):
    value_type = int
    entity = Household
    label = "Dependents"
    unit = EUR
    documentation = "Number of dependents"
    definition_period = YEAR
    adds = ["is_dependent"]
