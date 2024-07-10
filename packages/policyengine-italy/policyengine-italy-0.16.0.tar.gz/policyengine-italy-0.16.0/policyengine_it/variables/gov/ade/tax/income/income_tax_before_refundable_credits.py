from policyengine_it.model_api import *


class income_tax_before_refundable_credits(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    unit = EUR
    label = "Italian national income tax before refundable credits"
    documentation = "Income tax liability (including other taxes) after non-refundable credits are used, but before refundable credits are applied"

    def formula(person, period, parameters):
        income_tax_before_credits = person("income_tax_before_credits", period)
        non_refundable_tax_credits = person(
            "non_refundable_tax_credits", period
        )
        return max_(income_tax_before_credits - non_refundable_tax_credits, 0)
