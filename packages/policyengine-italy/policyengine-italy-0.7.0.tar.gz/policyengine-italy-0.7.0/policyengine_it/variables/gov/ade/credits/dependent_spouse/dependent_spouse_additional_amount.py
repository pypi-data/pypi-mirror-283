from policyengine_it.model_api import *


class dependent_spouse_additional_amount(Variable):
    value_type = float
    entity = Household
    label = "Dependent spouse income tax credit additional amount"
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.ade.credits.dependent_spouse

        is_eligible = household("dependent_spouse_eligible", period)
        income = household("household_market_income", period)
        additional_amount = p.additional.calc(income)

        return is_eligible * additional_amount
