from policyengine_it.model_api import *


class shepherd_fund_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Shepherd Fund"
    definition_period = YEAR

    def formula(person, period, parameters):
        employment_category = person("employment_category", period)

        return (
            employment_category
            == employment_category.possible_values.EXECUTIVE
        )
