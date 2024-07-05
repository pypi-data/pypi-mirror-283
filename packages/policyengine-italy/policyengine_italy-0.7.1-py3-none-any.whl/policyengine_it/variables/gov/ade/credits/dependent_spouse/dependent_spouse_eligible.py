from policyengine_it.model_api import *


class dependent_spouse_eligible(Variable):
    value_type = bool
    entity = Household
    label = "Eligible for dependent spouse income tax credit"
    definition_period = YEAR

    def formula(household, period, parameters):
        p = parameters(period).gov.ade.credits.dependent_spouse.eligibility

        # Determine if household is married
        household_is_married: bool = household("household_married", period)

        # Pull overall household income pre-credits
        household_income: float = household("household_market_income", period)

        # Find spouse's income specifically
        spouse_income: float = household("spouse_market_income", period)

        # Find values for each eligibility criterium
        elig_income_dist: bool = household_income > spouse_income
        elig_spouse_income: bool = spouse_income <= p.spouse_income
        elig_household_income: bool = household_income <= p.household_income
        elig_marital_status: bool = household_is_married

        eligible = (
            elig_income_dist
            & elig_spouse_income
            & elig_household_income
            & elig_marital_status
        )

        return eligible
