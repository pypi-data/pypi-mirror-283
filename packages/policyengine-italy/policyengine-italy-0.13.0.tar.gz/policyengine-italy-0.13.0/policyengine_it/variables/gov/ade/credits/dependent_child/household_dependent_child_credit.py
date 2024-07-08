from policyengine_it.model_api import *


class household_dependent_child_credit(Variable):
    value_type = float
    entity = Household
    label = "tax"
    documentation = (
        "Household-level calculation of dependent child income tax credit."
    )
    unit = EUR
    definition_period = YEAR

    def formula(household, period, parameters):

        dependents = household.members("dependent_child_credit", period)
        print(dependents)
        return household.sum(dependents)
