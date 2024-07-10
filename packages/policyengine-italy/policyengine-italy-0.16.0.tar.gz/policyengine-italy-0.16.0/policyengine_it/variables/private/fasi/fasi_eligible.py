from policyengine_it.model_api import *


class fasi_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Fondo Assistenza Sanitaria Industria (FASI)"
    definition_period = YEAR

    def formula(person, period, parameters):
        employment_category = person("employment_category", period)

        return (
            employment_category
            == employment_category.possible_values.EXECUTIVE
        )
