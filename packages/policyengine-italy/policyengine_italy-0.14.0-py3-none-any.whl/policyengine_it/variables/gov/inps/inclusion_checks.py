from policyengine_it.model_api import *


class inclusion_checks(Variable):
    value_type = float
    entity = Household
    label = "Total inclusion check value"
    definition_period = MONTH

    def formula(household, period, parameters):
        # On paper, members of various different vulnerable groups
        # qualify for this program. However, our source material only
        # calculates this for children, hence the formula

        value = parameters(period).gov.inps.inclusion_checks.amount

        person = household.members

        return value * household.any(person("is_child", period))
