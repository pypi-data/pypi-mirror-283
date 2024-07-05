from policyengine_it.model_api import *


class shepherd_fund(Variable):
    # The Shepherd Fund consists of a required fixed payment from all
    # contributors, which we model, plus optional payments, which are not
    # included in our source material. This is created for future expansion
    value_type = float
    entity = Person
    label = "Total Shepherd Fund contribution"
    definition_period = YEAR
    adds = ["shepherd_fund_base_amount"]
