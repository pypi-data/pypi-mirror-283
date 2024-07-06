from .TSCollector import TSCollector
import logging
from os.path import join
from functools import reduce
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, hstack, vstack, diags
from .DAO import SecurityDAO, ETFDAO

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def expand_df(df, index=None, columns=None, fillna=0):
    """
    Expand matrix dimensions.

    This function expand matrix index and columns.

    Parameters:
    df (DataFrame): The matrix to be expanded.

    Returns:
    DataFrame: The expanded matrix.
    """
    if index is None:
        index = df.index
    if columns is None:
        columns = df.columns
    extra_columns = list(set(columns) - set(df.columns))
    extra_index = list(set(index) - set(df.index))
    return pd.concat([df, pd.DataFrame(index=extra_index, columns=extra_columns)], axis=0).fillna(fillna)


def expand_basket_weight(basket_weight):
    """
    Expand basket holdings to bottom level.

    This function expand baskets holdings to the bottom level that only holds equity securities.

    Parameters:
    basket_weight (DataFrame): The basket holdings matrix with holdings on the rows, basket names on the columns.

    Returns:
    DataFrame: The expanded holdings matrix.
    """
    basket_weight.fillna(0, inplace=True)
    basket_ids = list(basket_weight.columns)
    non_basket_ids = list(set(basket_weight.index) - set(basket_ids))
    non_basket_ids.sort()
    basket_weight = expand_df(basket_weight, index=basket_ids)
    logging.debug(
        '{} baskets and {} non-basket equities.'.format(len(basket_ids), len(non_basket_ids)))

    B = basket_weight.loc[basket_ids, :]
    B.fillna(0, inplace=True)
    if B.empty:
        logging.debug('No basket cross ownership.')
        return basket_weight.loc[non_basket_ids, :]

    e_B = np.linalg.eig(B)

    if any(np.abs(e_B[0]) >= 1):
        logging.error(
            'Absolute value of eigenvalue greater than 1 of holding matrix. ')
        raise ValueError(
            'Absolute value of eigenvalue greater than 1 of holding matrix. ')
    elif all(e_B[0] == 0):
        # No cross ownership
        A = basket_weight.loc[non_basket_ids, :]
        I = np.eye(B.shape[0])
        return pd.DataFrame(np.dot(A, np.linalg.inv(I - B)),
                            index=non_basket_ids,
                            columns=basket_ids)
    else:
        # Real part of \sum_{i=1}^inf B^i
        B_sum = np.real(np.round(
            np.dot(np.dot(e_B[1], np.diag(1/(1-e_B[0]))), np.linalg.inv(e_B[1])), 15))
        B_sum = pd.DataFrame(B_sum, index=B.index, columns=B.index)
        return pd.DataFrame(np.dot(basket_weight.loc[non_basket_ids], B_sum),
                            index=non_basket_ids,
                            columns=basket_ids)


class PortfolioOne:
    DEFAULT_CONFIG = {
        "root_portfolio": "Main",
        "basket_to_keep": ["ETF"]
    }
    portfolio_weight_list = None
    etf_weight_list = None

    def __init__(self, data, security_dao, etf_dao, config=None):
        config_ = self.DEFAULT_CONFIG
        if config is not None:
            config_.update(config)
        self.config = config_
        # SecurityDAO(self.config.get('security_dao_config'))
        self.security_dao = security_dao
        self.etf_dao = etf_dao  # ETFDAO(self.config.get('etf_dao_config'))
        self.data = self.security_dao.map(data)
        self._init_weight()

    def _get_weight_one(self, df):
        """
        Get a weight series for one portfolio.
        """
        config = self.security_dao.config
        id_col, weight_col = config.get('id_col'), config.get('weight_col')
        return df.set_index(id_col)[weight_col]

    def _get_weight_list(self):
        """
        Get the weight dict for multiple portfolios.
        """
        data = self.data
        config = self.security_dao.config
        id_col, portfolio_col = config.get(
            'id_col'), config.get('portfolio_col')
        portfolios = list(data[portfolio_col].unique())
        return {p: self._get_weight_one(data[data[portfolio_col] == p]) for p in portfolios}

    def get_portfolio_weight_list(self):
        if self.portfolio_weight_list is None:
            self.portfolio_weight_list = self._get_weight_list()
        return self.portfolio_weight_list

    def get_etf_weight_list(self):
        if self.etf_weight_list is None:
            config = self.security_dao.config
            time_col, id_col = config.get("time_col"), config.get("id_col")
            data = self.data
            dated = data[time_col].iloc[0]
            ids = list(data[id_col].unique())
            self.etf_weight_list = self.etf_dao.get_etf_weight_list(
                ids=ids, dated=dated)
        return self.etf_weight_list

    def get_weight_list(self):
        weight_list = self.get_portfolio_weight_list()
        weight_list.update(self.get_etf_weight_list())
        return weight_list

    def get_weight_mat(self):
        weight_list = self.get_weight_list()
        return pd.DataFrame(weight_list).fillna(0)

    def get_root_portfolio_weight(self):
        root = self.config.get('root_portfolio')
        return self.get_portfolio_weight_list().get(root)

    def get_user_basket_ids(self):
        """_summary_
        Get user basket ids excluding root portfolio

        Returns:
            list: user basket ids
        """
        root = self.config.get('root_portfolio')
        user_basket_ids = list(self.get_portfolio_weight_list().keys())
        return list(set(user_basket_ids) - {root})

    def get_etf_ids(self):
        return list(self.get_etf_weight_list().keys())

    def _get_basket_to_keep(self):
        basket_to_keep = self.config.get('basket_to_keep')
        user_basket_ids = self.get_user_basket_ids()
        etf_ids = self.get_etf_ids()
        all_basket_ids = user_basket_ids + etf_ids
        basket_ids = [id for id in basket_to_keep if id in all_basket_ids]
        if "ETF" in basket_to_keep:
            basket_ids = basket_ids + etf_ids
        if "BASKET" in basket_to_keep:
            basket_ids = basket_ids + user_basket_ids
        if "ALL" in basket_to_keep:
            basket_ids = basket_ids + all_basket_ids
        basket_ids = list(set(basket_ids))
        logging.debug('Basket to keep: {}'.format(', '.join(basket_ids)))
        return basket_ids
    
    def set_basket_to_keep(self, basket_to_keep):
        self.config['basket_to_keep'] = basket_to_keep
        self._init_weight()

    def _init_weight(self):
        self._init_h()
        self._init_H()

    def _init_h(self):
        """
        Construct final holding matrix.
        """
        basket_to_keep = self._get_basket_to_keep()
        all_ids = self.get_user_basket_ids() + self.get_etf_ids() + \
            [self.config.get('root_portfolio')
             ]  # all basket ids including portfolio
        basket_to_unfold = list(set(all_ids) - set(basket_to_keep))
        root = self.config.get('root_portfolio')

        # h: the final holdings in output
        weight_mat = self.get_weight_mat()
        weight_mat = weight_mat.loc[:, basket_to_unfold]
        h = expand_basket_weight(weight_mat).loc[:, root]
        h = h[h != 0]

        self.index_h = list(h.index)
        self.h = csr_matrix(h).T

    def _init_H(self):
        """
        Construct the conversion matrix which is used to calculate composite attributes.
        """
        index_h = self.index_h
        basket_to_keep = self._get_basket_to_keep()
        equity_ids = list(set(index_h) - set(basket_to_keep))

        weight_mat_underlying = expand_basket_weight(self.get_weight_mat())
        basket_part = weight_mat_underlying.loc[:, basket_to_keep]
        equity_part = pd.DataFrame(
            np.diag(np.ones(len(equity_ids))), index=equity_ids, columns=equity_ids)
        H = pd.concat([basket_part, equity_part], axis=1).fillna(
            0)  # index are left-aligned
        H = H.loc[:, index_h]

        self.index_H = list(H.index)
        self.H = csr_matrix(H)

    def set_basket_to_keep(self, basket_to_keep):
        self.config['basket_to_keep'] = basket_to_keep
        self._init_weight()


class PortfolioTS(TSCollector):
    def __init__(self, data=None, config=None):
        default_config = {
            "path": "portfolio_data",
            "meta_file": None,
            "root_portfolio": "Main",
            "basket_to_keep": ["ALL_ETF"],
            "security_dao_config": {},
            "etf_dao_config": {}
        }
        if config is not None:
            default_config.update(config)
        super().__init__(default_config)
        if data is not None:
            self._setup_dao()
            time_col = self.config.get("security_dao_config").get("time_col")
            t_list = list(data[time_col].unique())
            t_list.sort()

            def _wrapper(t):
                logging.info(f'Initializing PortfolioOne for {t}')
                return self._init_p1(data[data[time_col] == t])
            self._cache = {t: _wrapper(t) for t in t_list}

    def _init_p1(self, data):
        return PortfolioOne(data, self.security_dao, self.etf_dao, self.config)

    def _setup_dao(self):
        self._use_one_reader()
        self.security_dao = SecurityDAO(self.config.get('security_dao_config'))
        self.etf_dao = ETFDAO(self.config.get('etf_dao_config'))

    def _use_one_reader(self):
        config = self.config
        meta_file = config.get('meta_file')
        if meta_file is not None:
            config['security_dao_config']['meta_file'] = meta_file
            logging.debug(f'Use {meta_file} for security_dao')
            config['etf_dao_config']['meta_file'] = meta_file
            logging.debug(f'Use {meta_file} for etf_dao')
            self.config = config
