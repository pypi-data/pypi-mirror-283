from policyengine_it.model_api import *


class mario_besusso_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Mario Besusso Fund"
    definition_period = YEAR

    def formula(person, period, parameters):
        mb_eligible_groups = parameters(
            period
        ).private.mario_besusso.eligibility

        employment_category = person(
            "employment_category", period
        ).decode_to_str()[0]

        is_eligible = np.where(
            employment_category in mb_eligible_groups, True, False
        )

        return is_eligible
