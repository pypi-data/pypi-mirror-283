from policyengine_it.model_api import *


class universal_credit_low_income_bonus(Variable):
    value_type = float
    entity = Household
    label = "Single and universal allowance for dependent children, low-income bonus"
    definition_period = MONTH

    def formula(household, period, parameters):

        p = parameters(period).gov.inps.universal_credit_low_income_bonus
        person = household.members
        income = household("head_market_income", period)

        is_eligible = person("age", period) < p.max_dependent_age

        base_amount = where(is_eligible, p.base_amount, 0)

        phase_out_amount = where(is_eligible, p.phase_out.calc(income), 0)

        total = base_amount - phase_out_amount

        return max_(household.sum(total), 0)
