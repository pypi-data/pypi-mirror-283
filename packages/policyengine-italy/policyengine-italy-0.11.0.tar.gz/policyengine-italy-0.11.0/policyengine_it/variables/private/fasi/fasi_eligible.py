from policyengine_it.model_api import *


class fasi_eligible(Variable):
    value_type = bool
    entity = Person
    label = "Eligible for Fondo Assistenza Sanitaria Industria (FASI)"
    definition_period = YEAR

    def formula(person, period, parameters):
        fasi_eligible_groups = parameters(period).private.fasi.eligibility

        employment_category = person(
            "employment_category", period
        ).decode_to_str()[0]

        return employment_category in fasi_eligible_groups
