from policyengine_it.model_api import *


class mario_negri_base_amount(Variable):
    value_type = float
    entity = Person
    label = "Fixed, flat base amount paid by all Mario Negri contributors"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("mario_negri_eligible", period)
        base_amount = parameters(period).private.mario_negri.base_amount

        return is_eligible * base_amount
