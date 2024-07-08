from policyengine_it.model_api import *


class mario_negri(Variable):
    value_type = float
    entity = Person
    label = "Total Mario Negri Fund payment for eligible contributors"
    definition_period = YEAR
    adds = ["mario_negri_base_amount", "mario_negri_variable_amount"]
