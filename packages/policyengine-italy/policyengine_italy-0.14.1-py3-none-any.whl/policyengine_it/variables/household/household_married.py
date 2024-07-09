from policyengine_it.model_api import *


class household_married(Variable):
    value_type = bool
    entity = Household
    definition_period = YEAR
    label = "Household head and spouse are married"

    def formula(household, period, parameters):
        person = household.members
        return household.any(person("is_spouse", period))
