from policyengine_it.model_api import *


class mario_besusso(Variable):
    value_type = float
    entity = Person
    label = "Total amount paid by Mario Besusso contributors"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("mario_besusso_eligible", period)
        income = person("total_individual_pre_tax_income", period)

        p = parameters(period).private.mario_besusso.rates

        amount = p.calc(income)

        return is_eligible * amount
