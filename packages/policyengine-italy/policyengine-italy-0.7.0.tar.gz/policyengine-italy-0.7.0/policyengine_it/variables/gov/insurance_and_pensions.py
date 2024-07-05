from policyengine_it.model_api import *


class insurance_and_pensions(Variable):
    value_type = float
    entity = Person
    label = "insurance and pensions, total"
    unit = EUR
    definition_period = YEAR
    adds = ["social_security", "mario_negri"]
