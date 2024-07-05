from policyengine_it.model_api import *


class managers_fund(Variable):
    value_type = float
    entity = Person
    label = "Total amount paid by Industrial Company Managers' Pension Fund contributors"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("managers_fund_eligible", period)
        income = person("total_individual_pre_tax_income", period)

        p = parameters(period).private.managers_fund.rates

        amount = p.calc(income)

        return is_eligible * amount
