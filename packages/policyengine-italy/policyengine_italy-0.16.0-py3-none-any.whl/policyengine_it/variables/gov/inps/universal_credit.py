from policyengine_it.model_api import *


class universal_credit(Variable):
    value_type = float
    entity = Household
    label = "Single and universal allowance for dependent children amount"
    definition_period = MONTH

    def formula(household, period, parameters):

        p = parameters(period).gov.inps.universal_credit
        person = household.members

        qualifying_deps = household.sum(
            person("age", period) < p.max_dependent_age
        )

        # Determine if household is in standard or higher bracket
        head_income = household("head_market_income", period)

        bracket = where(head_income > p.higher.threshold, "higher", "standard")

        base_amount = p.base_amount.calc(person("age", period))

        age_factor = where(
            bracket == "higher",
            1,
            p.standard.age_factor.calc(person("age", period)),
        )

        number_deps_factor = where(
            bracket == "higher",
            1,
            p.standard.number_dependents_factor.calc(qualifying_deps),
        )

        return household.sum(base_amount * age_factor) * number_deps_factor
