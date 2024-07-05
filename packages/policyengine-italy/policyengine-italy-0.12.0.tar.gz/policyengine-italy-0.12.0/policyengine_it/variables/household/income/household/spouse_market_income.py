from policyengine_it.model_api import *


class spouse_market_income(Variable):
    value_type = float
    entity = Household
    label = "Market income of dependent spouse within household"
    definition_period = YEAR

    def formula(household, period, parameters):
        person = household.members

        # Find spouse's income specifically
        is_spouse: bool = person("is_spouse", period)
        market_income = person("total_individual_pre_tax_income", period)

        spouse_market_income: float = np.where(
            is_spouse, person("total_individual_pre_tax_income", period), 0
        )
        spouse_market_income: float = household.sum(market_income * is_spouse)

        return spouse_market_income
