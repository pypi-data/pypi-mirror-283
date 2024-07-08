from policyengine_it.model_api import *


class dependent_spouse_base_amount(Variable):
    value_type = float
    entity = Household
    label = "Dependent spouse income tax credit base amount"
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.ade.credits.dependent_spouse

        is_eligible = household("dependent_spouse_eligible", period)
        income = household("household_market_income", period)
        base_amount = p.base_amount.calc(income)

        phase_out_rate = p.phase_out.calc(income)
        prev_threshold = get_previous_threshold(income, p.phase_out.thresholds)
        phase_out_amount = phase_out_rate * (income - prev_threshold)

        return is_eligible * (base_amount - phase_out_amount)
