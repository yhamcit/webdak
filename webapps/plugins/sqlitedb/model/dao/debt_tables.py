from datetime import datetime

from pony.orm import PrimaryKey, Required, Optional, composite_key





class LocalPublicDebt():
    id = PrimaryKey(int)

    country = Optional(str)
    province = Required(str)
    metropolis = Optional(str)
    city = Required(str)
    district = Optional(str)

    local_debt_balances = Required(float)
    total_debt_upper_limit = Optional(float)
    total_local_bonds = Optional(float)
    total_debt_amount = Optional(float)
    total_gdp_amount = Optional(float)
    debt_to_gdp_ratio = Optional(float)
    local_general_public_revenue = Optional(float)
    debt_to_revenue_ratio = Optional(float)
    
    statistical_scope = Required(str)
    update_time = Required(datetime)
