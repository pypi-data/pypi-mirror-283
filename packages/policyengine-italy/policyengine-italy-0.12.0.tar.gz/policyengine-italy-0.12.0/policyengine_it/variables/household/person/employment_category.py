from policyengine_it.model_api import *


class EmploymentCategory(Enum):
    # This is not defined well in the reference material
    EMPLOYEE = "Standard employee"
    EXECUTIVE = "Executive"
    UNEMPLOYED = "Unemployed"


class employment_category(Variable):
    value_type = Enum
    entity = Person
    label = "Employment category"
    possible_values = EmploymentCategory
    default_value = EmploymentCategory.EMPLOYEE
    definition_period = YEAR
