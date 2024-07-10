from policyengine_it.model_api import *


class income_tax_before_credits(Variable):
    value_type = float
    entity = Person
    label = "Income tax before all tax credits"
    unit = EUR
    documentation = "Income tax before all tax credits"
    definition_period = YEAR

    def formula(person, period, parameters):
        income = person("total_individual_pre_tax_income", period)
        gov = parameters(period).gov.ade.tax.income
        return gov.income_tax_schedule.calc(income)
