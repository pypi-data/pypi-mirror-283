from policyengine_it.model_api import *


class person_id(Variable):
    value_type = float
    entity = Person
    label = "Person ID"
    unit = EUR
    definition_period = ETERNITY
