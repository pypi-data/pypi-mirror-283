from policyengine_it.model_api import *


class head_market_income(Variable):
    value_type = float
    entity = Household
    label = "Income of head of household"
    definition_period = YEAR

    def formula(household, period, parameters):
        person = household.members

        # Find spouse's income specifically
        is_head = person("is_head", period)
        market_income = person("total_individual_pre_tax_income", period)

        return household.sum(market_income * is_head)
