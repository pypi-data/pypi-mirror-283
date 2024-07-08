from policyengine_it.model_api import *


class social_security(Variable):
    value_type = float
    entity = Person
    label = "Total social security contribution"
    definition_period = YEAR

    def formula(person, period, parameters):
        employment_category = person("employment_category", period)
        category = employment_category.possible_values
        income = person("total_individual_pre_tax_income", period)

        p = parameters(period).gov.inps.social_security.rates

        social_security_amount = select(
            [
                employment_category == category.EMPLOYEE,
                employment_category == category.EXECUTIVE,
                employment_category == category.UNEMPLOYED,
            ],
            [
                p.employee.calc(income),
                p.executive.calc(income),
                p.unemployed.calc(income),
            ],
        )

        return social_security_amount
