SECURITYDAO_CONFIG = {
    'meta_file': None,
    'mapping_cols': ['Ticker', 'Country'],
    'time_col': 'Date',
    'id_col': 'SecurityID',
    'portfolio_col': 'Portfolio',
    'weight_col': 'Weight',
    'data_types': ['idm','comp_idm']
}

ETFDAO_CONFIG = {
    "meta_file": None,
    "data_types": ["comp_weight"],
    "weight_col": "ConstituentWeight",
    "id_col": "ConstituentID",
    "composite_id_col": "CompositeID"
}

PORTFOLIOONE_CONFIG = {
    "root_portfolio": "Main",
    "basket_to_keep": ["ETF"],
}

PORTFOLIOTS_CONFIG = {
    "path": "portfolio_data",
    "root_portfolio": "Main",
    "basket_to_keep": ["ETF"],
    "meta_file": None,
    "security_dao_config": SECURITYDAO_CONFIG,
    "etf_dao_config": ETFDAO_CONFIG
}

ATTRIBUTIONTS_CONFIG = {
    "path": "attribution_data",
    "additional_t": None,
    "meta_file": None,
    "rmd_reader_config": {
        "meta_file": None
    },
    "return_dao_config": {
        "meta_file": None,
        "data_types": ["att","comp_att"],
        "price_col": "Price"
    }
} 