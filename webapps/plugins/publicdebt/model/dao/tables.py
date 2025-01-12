from dataclasses import dataclass
from datetime import datetime




@dataclass
class LocalPublicDebt():
    country: str
    province: str
    metropolis: str
    city: str
    district: str

    local_debt_balances: float
    total_debt_upper_limit: float
    total_local_bonds: float
    total_debt_amount: float
    total_gdp_amount: float
    debt_to_gdp_ratio: float
    local_general_public_revenue: float
    debt_to_revenue_ratio: float
    
    statistical_scope: str
    update_time: datetime

    

create_table_stmt = """
    CREATE TABLE IF NOT EXISTS area_public_debt(
        id INTEGER PRIMARY KEY, 
        country TEXT, 
        province TEXT NOT NULL, 
        metropolis TEXT, 
        city TEXT NOT NULL, 
        district TEXT, 
        local_debt_balances REAL NOT NULL,  # 地方债余额
        total_debt_upper_limit REAL, 
        total_local_bonds REAL,             # 地方债券总额
        total_debt_amount REAL,             # 地方债务总额
        total_gdp_amount REAL, 
        debt_to_gdp_ratio REAL,             # 负债率
        local_general_public_revenue REAL,  # 一般性公共财政盈余
        debt_to_revenue_ratio REAL,         # 债务盈余率
        statistical_scope TEXT NOT NULL, 
        update_time TEXT NOT NULL UNIQUE
    )
    """

insert_debt = """
    INSERT INTO area_public_debt 
        (country, province, metropolis, city, local_debt_balances, statistical_scope, update_time) 
    VALUES 
        ('中国', '四川', '成都', '成都', 8073, '一般债务', '2024-12-31 00:00:00')
    """

query_debt = """
    SELECT * FROM area_public_debt
    """

default_query_conditions = {
    'country': None, 
    'province': None, 
    'metropolis': None, 
    'city': None, 
    'district': None, 
    'local_debt_balances': None, 
    'total_debt_upper_limit': None, 
    'total_local_bonds': None, 
    'total_debt_amount': None, 
    'total_gdp_amount': None, 
    'debt_to_gdp_ratio': None, 
    'local_general_public_revenue': None, 
    'debt_to_revenue_ratio': None, 
    'statistical_scope': None, 
    'update_time': None
    }

def generat_table_stmt():

    return """
        CREATE TABLE IF NOT EXISTS area_public_debt(
            id INTEGER PRIMARY KEY, 
            country TEXT, 
            province TEXT NOT NULL, 
            metropolis TEXT, 
            city TEXT NOT NULL, 
            district TEXT, 
            local_debt_balances REAL NOT NULL,
            total_debt_upper_limit REAL, 
            total_local_bonds REAL,
            total_debt_amount REAL,
            total_gdp_amount REAL, 
            debt_to_gdp_ratio REAL,
            local_general_public_revenue REAL,
            debt_to_revenue_ratio REAL,
            statistical_scope TEXT NOT NULL, 
            update_time TEXT NOT NULL UNIQUE
        )
    """

def insert_record_stmt(data_mapping: dict):

    insert_record_stmt = f"""
        INSERT INTO area_public_debt 
            {str(tuple(data_mapping.keys()))} 
        VALUES 
            {str(tuple(data_mapping.values()))} 
        """
    
    return insert_record_stmt
    
def simple_query_stmt(fields: dict):

    if any(fields.values()):
        match_condition = ' AND '.join(' = '.join((str(k), f"'{str(v)}'")) for k, v in fields.items() if v)
        where_clause = f"WHERE {match_condition}"
    else:
        where_clause = ""

    simple_query_stmt = f"""
        SELECT {', '.join(fields.keys())} FROM area_public_debt {where_clause}
        """

    return simple_query_stmt