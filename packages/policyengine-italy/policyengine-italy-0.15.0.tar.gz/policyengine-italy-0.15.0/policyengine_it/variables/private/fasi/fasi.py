from policyengine_it.model_api import *


class fasi(Variable):
    # FASI has one base payment, plus optional additional; however,
    # our source material does not model the optional payments, hence leaving
    # this here for future expansion purposes
    value_type = float
    entity = Person
    label = "Total amount paid by Fondo Assistenza Sanitaria Industria (FASI) contributors"
    definition_period = YEAR
    adds = ["fasi_base_amount"]
