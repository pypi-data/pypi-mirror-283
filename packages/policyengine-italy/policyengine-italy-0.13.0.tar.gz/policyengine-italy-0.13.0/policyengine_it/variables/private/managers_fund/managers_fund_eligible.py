from policyengine_it.model_api import *


class managers_fund_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Industrial Company Managers' Pension Fund"
    definition_period = YEAR

    def formula(person, period, parameters):
        mf_eligible_groups = parameters(
            period
        ).private.managers_fund.eligibility

        employment_category = person(
            "employment_category", period
        ).decode_to_str()[0]

        return employment_category in mf_eligible_groups
