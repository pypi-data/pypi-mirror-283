from policyengine_it.model_api import *


class dependent_child_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for dependent child income tax credit"
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.ade.credits.dependent_child

        household = person.household

        # Find spouse's income specifically
        spouse_income = household("spouse_market_income", period)

        # Ensure spouse's income is less than household head income
        head_income = household("head_market_income", period)
        is_spouse_less_head = spouse_income < head_income

        # Determine if there are dependents in household over minimum age
        age = person("age", period)
        income = person("total_individual_pre_tax_income", period)
        is_dependent = person("is_dependent", period)

        min_age = p.eligibility.thresholds[0]
        is_eligible_age = age >= min_age

        is_eligible_income = income <= p.eligibility.calc(age)

        return (
            is_spouse_less_head
            & is_eligible_age
            & is_eligible_income
            & is_dependent
        )
