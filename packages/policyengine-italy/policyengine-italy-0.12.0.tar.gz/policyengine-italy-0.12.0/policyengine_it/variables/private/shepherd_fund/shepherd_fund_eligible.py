from policyengine_it.model_api import *


class shepherd_fund_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Shepherd Fund"
    definition_period = YEAR

    def formula(person, period, parameters):
        sf_eligible_groups = parameters(
            period
        ).private.shepherd_fund.eligibility

        employment_category = person(
            "employment_category", period
        ).decode_to_str()[0]

        return employment_category in sf_eligible_groups
