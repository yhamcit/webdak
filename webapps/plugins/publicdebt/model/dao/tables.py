from dataclasses import dataclass
from datetime import datetime

from pony.orm import PrimaryKey, Required, Optional, composite_key




@dataclass
class LocalPublicDebt():
    country: Optional= Optional(str)
    province: Required= Required(str)
    metropolis: Optional= Optional(str)
    city: Required= Required(str)
    district: Optional= Optional(str)

    local_debt_balances: Required= Required(float)
    total_debt_upper_limit: Optional= Optional(float)
    total_local_bonds: Optional= Optional(float)
    total_debt_amount: Optional= Optional(float)
    total_gdp_amount: Optional= Optional(float)
    debt_to_gdp_ratio: Optional= Optional(float)
    local_general_public_revenue: Optional= Optional(float)
    debt_to_revenue_ratio: Optional= Optional(float)
    
    statistical_scope: Required= Required(str)
    update_time: Required= Required(datetime)

