from policyengine_it.model_api import *


class dependent_child_credit(Variable):
    value_type = float
    entity = Person
    label = "Dependent child income tax credit amount"
    definition_period = YEAR

    def formula(person, period, parameters):
        p = parameters(period).gov.ade.credits.dependent_child

        is_eligible = person("dependent_child_eligible", period)
        is_disabled = person("is_disabled", period)
        amount = where(is_disabled, p.amount.disabled, p.amount.standard)

        return is_eligible * amount
