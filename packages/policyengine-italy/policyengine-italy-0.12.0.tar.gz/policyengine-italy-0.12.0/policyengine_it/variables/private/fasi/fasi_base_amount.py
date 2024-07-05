from policyengine_it.model_api import *


class fasi_base_amount(Variable):
    value_type = float
    entity = Person
    label = "Fixed, flat base amount paid by all Fondo Assistenza Sanitaria Industria (FASI) contributors"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_eligible = person("fasi_eligible", period)
        base_amount = parameters(period).private.fasi.base_amount

        return is_eligible * base_amount
