from policyengine_it.model_api import *


class is_dependent(Variable):
    value_type = bool
    entity = Person
    label = "Is a dependent"
    definition_period = YEAR

    def formula(person, period, parameters):
        head = person("is_head", period)
        spouse = person("is_spouse", period)
        return ~head & ~spouse
