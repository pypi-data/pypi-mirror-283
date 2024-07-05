from policyengine_it.model_api import *


class head_income(Variable):
    value_type = bool
    entity = Household
    label = "Income of head of household"
    definition_period = YEAR

    def formula(household, period, parameters):
        person = household.members

        # Find spouse's income specifically
        is_head: bool = person("is_head", period)
        head_income: float = (
            person("total_individual_pre_tax_income", period) * is_head
        )

        return head_income
