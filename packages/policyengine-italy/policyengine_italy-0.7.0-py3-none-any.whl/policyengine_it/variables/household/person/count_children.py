from policyengine_it.model_api import *


class count_children(Variable):
    value_type = int
    entity = Household
    label = "Children"
    unit = EUR
    documentation = "Number of dependent children under the age of 19"
    definition_period = YEAR
