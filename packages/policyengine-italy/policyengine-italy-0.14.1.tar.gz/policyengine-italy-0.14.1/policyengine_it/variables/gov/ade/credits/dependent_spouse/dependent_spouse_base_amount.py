from policyengine_it.model_api import *


class dependent_spouse_base_amount(Variable):
    value_type = float
    entity = Household
    label = "Dependent spouse income tax credit base amount"
    definition_period = YEAR
    defined_for = "dependent_spouse_eligible"

    def formula(household, period, parameters):
        p = parameters(period).gov.ade.credits.dependent_spouse

        income = household("household_market_income", period)

        is_eligible = household("dependent_spouse_eligible", period)
        phase_out_amount = p.phase_out.calc(income)

        return is_eligible * max_((p.base_amount - phase_out_amount), 0)
