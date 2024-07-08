from policyengine_it.model_api import *


class low_income_credit(Variable):
    value_type = float
    entity = Person
    label = "Value returned by the low income tax credit"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("low_income_eligible", period)
        exemption_rate = parameters(
            period
        ).gov.ade.credits.low_income.exemption_rate
        income = person("total_individual_pre_tax_income", period)
        exempted_income = exemption_rate * income

        return is_eligible * exempted_income
