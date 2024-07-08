from policyengine_it.model_api import *


class mario_negri_variable_amount(Variable):
    value_type = float
    entity = Person
    label = "Variable amount paid by Mario Negri contributors"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("mario_negri_eligible", period)
        income = person("total_individual_pre_tax_income", period)

        p = parameters(period).private.mario_negri.rates

        variable_amount = p.calc(income)

        return is_eligible * variable_amount
