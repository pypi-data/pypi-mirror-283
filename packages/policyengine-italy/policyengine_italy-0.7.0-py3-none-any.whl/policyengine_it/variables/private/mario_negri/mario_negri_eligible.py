from policyengine_it.model_api import *


class mario_negri_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Mario Negri Fund"
    definition_period = YEAR

    def formula(person, period, parameters):
        mn_eligible_groups = parameters(period).private.mario_negri.eligibility

        employment_category = person(
            "employment_category", period
        ).decode_to_str()[0]

        if employment_category in mn_eligible_groups:
            return True
        else:
            return False
