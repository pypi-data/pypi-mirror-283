from policyengine_it.model_api import *


class shepherd_fund_base_amount(Variable):
    value_type = float
    entity = Person
    label = "Fixed, flat base amount paid by all Shepherd Fund contributors"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("shepherd_fund_eligible", period)
        base_amount = parameters(period).private.shepherd_fund.base_amount

        return is_eligible * base_amount
