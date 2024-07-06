from .TSCollector import TSCollector
import logging
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix, hstack, vstack, diags
from .DAO import RiskModelReader, SecurityReturnDAO


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class AttributionCore:
    """
    h: m x 1
    E: m x k
    Gamma: k x k
    Lambda: m x m
    f: k x 1
    r: m x 1
    G: k x g
    """

    def __init__(self, h, E, Gamma, Lambda, f, r, G):
        self._cache = {}
        self.h, self.E = h, E
        self.Gamma, self.Lambda = Gamma, Lambda
        self.f, self.r = f, r
        self.G = G

    def _add_group(self, factor_part, residual_part):
        G = self.G
        group_part = factor_part.dot(G)
        systematic_part = csr_matrix(group_part.sum(axis=1))
        total_part = systematic_part + residual_part
        return hstack([factor_part, group_part, systematic_part, residual_part, total_part])

    @property
    def stock_exposure(self):
        return self.E

    @property
    def stock_var(self):
        if "stock_var" not in self._cache.keys():
            E, Gamma, Lambda = self.E, self.Gamma, self.Lambda
            X = E.dot(Gamma)
            systematic_var = X.multiply(E)
            residual_var = csr_matrix(Lambda.diagonal()).T
            self._cache["stock_var"] = self._add_group(
                systematic_var, residual_var)
        return self._cache.get("stock_var")

    @property
    def stock_total_risk(self):
        if "stock_total_risk" not in self._cache.keys():
            total_var = self.stock_var.tocsr()[:, -1]
            self._cache["stock_total_risk"] = np.sqrt(total_var)
        return self._cache.get("stock_total_risk")

    @property
    def stock_risk(self):
        if "stock_risk" not in self._cache.keys():
            stock_var = self.stock_var
            stock_total_risk = self.stock_total_risk
            self._cache["stock_risk"] = stock_var.multiply(
                stock_total_risk.power(-1))
        return self._cache.get("stock_risk")

    @property
    def stock_return(self):
        if "stock_return" not in self._cache.keys():
            f, E, r = self.f, self.E, self.r
            systematic_part = E.multiply(f.T)
            residual_part = r - csr_matrix(systematic_part.sum(axis=1))
            self._cache["stock_return"] = self._add_group(
                systematic_part, residual_part)
        return self._cache.get("stock_return")

    @property
    def stock_exposure_contri(self):
        if "stock_exposure_contri" not in self._cache.keys():
            h, E = self.h, self.E
            self._cache["stock_exposure_contri"] = E.multiply(h)
        return self._cache.get("stock_exposure_contri")

    @property
    def factor_risk(self):
        Gamma = self.Gamma
        return csr_matrix(np.sqrt(Gamma.diagonal())).T

    @property
    def stock_voladj_exposure_contri(self):
        if "stock_voladj_exposure_contri" not in self._cache.keys():
            stock_exposure_contri, factor_risk = self.stock_exposure_contri, self.factor_risk
            self._cache["stock_voladj_exposure_contri"] = stock_exposure_contri.multiply(
                factor_risk.T)
        return self._cache.get("stock_voladj_exposure_contri")

    @property
    def stock_correlation(self):
        pass
#         if "stock_correlation" not in self._cache.keys():
#             stock_voladj_exposure_contri = self.stock_voladj_exposure_contri
#             stock_risk_contri = self.stock_risk_contri
#         return self._cache.get("stock_correlation")

    @property
    def stock_var_contri(self):
        if "stock_var_contri" not in self._cache.keys():
            h, E, Gamma, Lambda = self.h, self.E, self.Gamma, self.Lambda
            x = h.T.dot(E).dot(Gamma)
            systematic_var_contri = E.multiply(x).multiply(h)
            residual_var_contri = Lambda.dot(h).multiply(h)
            self._cache["stock_var_contri"] = self._add_group(
                systematic_var_contri, residual_var_contri)
        return self._cache.get("stock_var_contri")

    @property
    def port_total_risk(self):
        if "port_total_risk" not in self._cache.keys():
            self._cache["port_total_risk"] = np.sqrt(
                self.stock_var_contri.tocsr()[:, -1].sum())
        return self._cache.get("port_total_risk")

    @property
    def stock_risk_contri(self):
        if "stock_risk_contri" not in self._cache.keys():
            self._cache["stock_risk_contri"] = self.stock_var_contri / \
                self.port_total_risk
        return self._cache.get("stock_risk_contri")

    @property
    def stock_return_contri(self):
        if "stock_return_contri" not in self._cache.keys():
            h = self.h
            self._cache["stock_return_contri"] = self.stock_return.multiply(h)
        return self._cache.get("stock_return_contri")

    @property
    def port_exposure(self):
        if "port_exposure" not in self._cache.keys():
            self._cache["port_exposure"] = csc_matrix(
                self.stock_exposure_contri.sum(axis=0).T)
        return self._cache.get("port_exposure")

    @property
    def port_voladj_exposure(self):
        if "port_voladj_exposure" not in self._cache.keys():
            self._cache["port_voladj_exposure"] = csc_matrix(
                self.port_exposure.multiply(self.factor_risk))
        return self._cache.get("port_voladj_exposure")

    @property
    def port_correlation(self):
        if "port_correlation" not in self._cache.keys():
            Gamma, port_exposure, factor_risk, port_total_risk = self.Gamma, self.port_exposure, self.factor_risk, self.port_total_risk
            self._cache["port_correlation"] = Gamma.dot(
                port_exposure).multiply((factor_risk*port_total_risk).power(-1))
        return self._cache.get("port_correlation")

    @property
    def port_risk(self):
        if "port_risk" not in self._cache.keys():
            self._cache["port_risk"] = csc_matrix(
                self.stock_risk_contri.sum(axis=0).T)
        return self._cache.get("port_risk")

    @property
    def port_return(self):
        if "port_return" not in self._cache.keys():
            self._cache["port_return"] = csc_matrix(
                self.stock_return_contri.sum(axis=0).T)
        return self._cache.get("port_return")


def expand_matrix(df, index=None, columns=None, fillna=0):
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

# v1 = weight_mat.iloc[:,0]
# v2 = weight_mat2.iloc[:,0]
# basket_weight = pd.concat([v1,v2], axis=1, keys=['PORTFOLIO','MYBENCHMARK'])
# rows=['extrarow1','MYBENCHMARK']
# cols=['extracol1','extracol2']
# expand_matrix(weight_mat, index=rows,columns=cols)


def _expand_basket_weight(basket_weight):
    """
    Expand basket holdings to bottom level.

    This function expand baskets holdings to the bottom level that only holds equity securities.

    Parameters:
    basket_weight (DataFrame): The basket holdings matrix with holdings on the rows, basket names on the columns.

    Returns:
    DataFrame: The expanded holdings matrix.
    """
    basket_weight.fillna(0, inplace=True)
    basket_ids = basket_weight.columns
    non_basket_ids = list(set(basket_weight.index) - set(basket_ids))
    basket_weight = expand_matrix(basket_weight, index=basket_ids)
    logging.debug(
        '{} baskets and {} non-basket equities.'.format(len(basket_ids), len(non_basket_ids)))

    B = basket_weight.loc[basket_ids, :]
    B.fillna(0, inplace=True)
    if B.empty:
        logging.info('No basket cross ownership.')
        return basket_weight

    e_B = np.linalg.eig(B)

    if any(np.abs(e_B[0]) >= 1):
        logging.error(
            'Absolute value of eigenvalue greater than 1 of holding matrix. ')
        raise ValueError(
            'Absolute value of eigenvalue greater than 1 of holding matrix. ')
    elif all(e_B[0] == 0):
        # No cross ownership
        A = basket_weight.loc[non_basket_ids]
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


class AttributionData:
    def __init__(self, portfolio, rmd, security_return):
        self._r = security_return
        self.H, self.index_H = portfolio.H, portfolio.index_H
        self.h, self.index_h = portfolio.h, portfolio.index_h
        self.etf_ids = portfolio.get_etf_ids()
        self._init_data(rmd)

    def _init_data(self, rmd):
        self._init_G(rmd)
        self._init_E(rmd)
        self._init_f(rmd)
        self._init_Lambda(rmd)
        self._init_Gamma(rmd)
        self._init_idm(rmd)
        self._init_r()

    def _init_G(self, rmd):
        category_col = 'Category'
        df = rmd.get('ret')
        factor_names = list(df.index)
        factor_alias = list(df['FactorAlias'])
        cates = list(df[category_col].unique())
        df = df[[category_col]]
        df.loc[:, ['Value']] = 1
        df = df.pivot(columns=category_col, values='Value').fillna(0)
        df = df.loc[factor_names, cates]
        G = csr_matrix(df)
        self.G = G
        self.factor_names = factor_names
        self.factor_alias = factor_alias
        self.group_names = cates

    def _init_E(self, rmd):
        index_H = self.index_H
        factor_names = self.factor_names
        exp = rmd.get('exp').loc[index_H, factor_names]
        self._E = csr_matrix(exp)

    def _init_f(self, rmd):
        _r = self._r
        factor_names = self.factor_names
        F = rmd.get('fmp').loc[:, factor_names]
        _r = _r.loc[F.index]
        f = F.T.dot(_r)
        self.f = csr_matrix(f).T

    def _init_Lambda(self, rmd):
        index_H = self.index_H
        id_map = {id: int(i) for i, id in enumerate(index_H)}
        isc = rmd.get('isc')
        isc = isc.loc[isc.SecurityId1.isin(
            index_H) & isc.SecurityId2.isin(index_H)]
        isc = csr_matrix((isc.Covariance, (isc.SecurityId1.map(
            id_map), isc.SecurityId2.map(id_map))), shape=(len(index_H), len(index_H)))
        rsk = diags(list(rmd.get('rsk').loc[index_H, 'SpecificRisk']/100))
        _Lambda = rsk**2 + isc
        self._Lambda = _Lambda

    def _init_Gamma(self, rmd):
        factor_names = self.factor_names
        cov = rmd.get('cov').loc[factor_names, factor_names]
        Gamma = csr_matrix(cov)
        self.Gamma = Gamma

    def _init_idm(self, rmd):
        index_H = self.index_H
        baskets = self.etf_ids

        idm = rmd.get('idm')
        meta = idm.columns  # TODO: meta columns customization
        idm = idm.loc[index_H, meta]

        basket_idm = pd.DataFrame(index=baskets, columns=meta)
        if 'comp_idm' in rmd.keys():
            comp_idm = rmd.get('comp_idm')
            comp_ids = list(set(baskets) & set(comp_idm.index))
            basket_idm.loc[comp_ids, :] = comp_idm.loc[comp_ids, :].values

        idm = pd.concat([idm, basket_idm], axis=0)
        self.idm = idm

    def _init_r(self):
        _r = self._r
        index_H = self.index_H
        _r = csr_matrix(_r.loc[index_H]).T
        self._r = _r

    def _change_portfolio_tree(self, portfolio):
        """
        Transform portfolio to a specific layer.
        """
        self.H = portfolio.H
        self.h, self.index_h = portfolio.h, portfolio.index_h


class AttributionOne:
    config = {}
    cache = {}
    result = {}

    def __init__(self, data, config={}):
        """
        Initialize an object.

        Parameters:
        data: An AttributionData instance.
        config (dict): Attribution configurations.
        """
        self.data = data
        self.config.update(config)
        self._init_core()

    @property
    def h(self):
        return self.data.h

    @property
    def E(self):
        H, _E = self.data.H, self.data._E
        E = H.T.dot(_E)
        return E

    @property
    def Gamma(self):
        return self.data.Gamma

    @property
    def Lambda(self):
        H, _Lambda = self.data.H, self.data._Lambda
        Lambda = H.T.dot(_Lambda).dot(H)
        return Lambda

    @property
    def f(self):
        return self.data.f

    @property
    def r(self):
        H, _r = self.data.H, self.data._r
        r = H.T.dot(_r)
        return r

    @property
    def G(self):
        return self.data.G

    @property
    def index_h(self):
        return self.data.index_h

    @property
    def index_H(self):
        return self.data.index_H

    @property
    def factor_names(self):
        return self.data.factor_names

    @property
    def factor_alias(self):
        return self.data.factor_alias

    @property
    def group_names(self):
        return self.data.group_names

    def _get_full_headers(self):
        factor_alias, group_names = self.factor_alias, self.group_names
        return factor_alias + group_names + ["Systematic", "Residual", "Total"]

    def _init_core(self):
        self.core = AttributionCore(
            self.h, self.E, self.Gamma, self.Lambda, self.f, self.r, self.G)

    def get_stock_exposure_contri(self):
        return pd.DataFrame(self.core.stock_exposure_contri.todense(), index=self.index_h, columns=self.factor_alias)

    def get_port_risk(self):
        return self.core.port_risk

    def get_stock_risk_contri(self):
        return pd.DataFrame(self.core.stock_risk_contri.todense(), index=self.index_h, columns=self._get_full_headers())

    def get_stock_exposure(self):
        return pd.DataFrame(self.core.stock_exposure.todense(), index=self.index_h, columns=self.factor_alias)

    def get_stock_risk(self):
        return pd.DataFrame(self.core.stock_risk.todense(), index=self.index_h, columns=self._get_full_headers())

    def get_stock_var(self):
        return pd.DataFrame(self.core.stock_var.todense(), index=self.index_h, columns=self._get_full_headers())

    def get_stock_return(self):
        return pd.DataFrame(self.core.stock_return.todense(), index=self.index_h, columns=self._get_full_headers())

    def get_stock_return_contri(self):
        return pd.DataFrame(self.core.stock_return_contri.todense(), index=self.index_h, columns=self._get_full_headers())

    def get_port_exposure(self):
        return pd.Series(self.core.port_exposure.toarray().flatten(), index=self.factor_alias)

    def get_port_voladj_exposure(self):
        return pd.Series(self.core.port_voladj_exposure.toarray().flatten(), index=self.factor_alias)

    def get_port_correlation(self):
        return pd.Series(self.core.port_correlation.toarray().flatten(), index=self.factor_alias)

    def get_port_risk(self):
        return pd.Series(self.core.port_risk.toarray().flatten(), index=self._get_full_headers())

    def get_port_risk_pct(self):
        port_risk = self.get_port_risk()
        return port_risk/port_risk.loc['Total']

    def get_port_return(self):
        return pd.Series(self.core.port_return.toarray().flatten(), index=self._get_full_headers())

    def get_port_summary(self):
        return pd.DataFrame({
            'Exposure': self.get_port_exposure(),
            'Exposure (Vol Adj.)': self.get_port_voladj_exposure(),
            'Correlation': self.get_port_correlation(),
            'Risk Contri.': self.get_port_risk(),
            'Risk Contri. (%).': self.get_port_risk_pct(),
            'Return Contri.': self.get_port_return()
        }, index=self._get_full_headers())

    def change_portfolio_tree(self, portfolio):
        self.data._change_portfolio_tree(portfolio)
        self._init_core()


class AttributionTS(TSCollector):
    def __init__(self, portfolio_ts=None, config=None):
        if config is None:
            config = {
                "path": "attribution_data",
                "additional_t": None,
                "meta_file": None,
                "rmd_reader_config": {},
                "return_dao_config": {}
            }
        super().__init__(config)
        if portfolio_ts is not None:
            self._setup_dao()
            self.portfolio_ts = portfolio_ts
            self._init_a1_list()

    def _init_a1_list(self):
        t_list = self.portfolio_ts.t_list
        additional_t = self.config.get('additional_t')
        if (additional_t is not None) and (additional_t > max(t_list)):
            self.return_dao.set_t_list(t_list + [additional_t])
            logging.debug(f'Set additional timestamp to {additional_t}')
        else:
            self.return_dao.set_t_list(t_list)
        self._cache = {t: self._init_a1(t) for t in t_list}

    def _init_a1(self, t):
        logging.info('Initializing AttributionOne for {} ... '.format(t))
        try:
            reader = self.reader
            return_dao = self.return_dao
            p1 = self.portfolio_ts.load_one(t)
            rmd = reader.get_risk_model_data(
                t, ['idm', 'comp_idm', 'exp', 'cov', 'rsk', 'isc', 'fmp', 'ret'])
            security_return = return_dao.get_forward_return(t)
            data = AttributionData(p1, rmd, security_return)
            logging.info('OK')
            return AttributionOne(data)
        except Exception as e:
            logging.info(f'Failed: {e}')
    
    def _setup_dao(self):
        self._use_one_reader()
        self.reader = RiskModelReader(self.config.get(
            'rmd_reader_config').get('meta_file'))
        self.return_dao = SecurityReturnDAO(
            self.config.get('return_dao_config'))

    def _use_one_reader(self):
        config = self.config
        meta_file = config.get('meta_file')
        if meta_file is not None:
            config['rmd_reader_config']['meta_file'] = meta_file
            logging.debug(f'Use {meta_file} for rmd_reader')
            config['return_dao_config']['meta_file'] = meta_file
            logging.debug(f'Use {meta_file} for security_return_dao')
            self.config = config

    def get_port_exposure_ts(self):
        a1_dict = self.load()
        df = pd.concat([a1.get_port_exposure()
                       for key, a1 in a1_dict.items()], axis=1).T
        df.index = list(a1_dict.keys())
        return df

    def get_port_voladj_exposure_ts(self):
        a1_dict = self.load()
        df = pd.concat([a1.get_port_voladj_exposure()
                       for key, a1 in a1_dict.items()], axis=1).T
        df.index = list(a1_dict.keys())
        return df

    def get_port_correlation_ts(self):
        a1_dict = self.load()
        df = pd.concat([a1.get_port_correlation()
                       for key, a1 in a1_dict.items()], axis=1).T
        df.index = list(a1_dict.keys())
        return df

    def get_port_risk_ts(self):
        a1_dict = self.load()
        df = pd.concat([a1.get_port_risk()
                       for key, a1 in a1_dict.items()], axis=1).T
        df.index = list(a1_dict.keys())
        return df

    def get_port_risk_pct_ts(self):
        a1_dict = self.load()
        df = pd.concat([a1.get_port_risk_pct()
                       for key, a1 in a1_dict.items()], axis=1).T
        df.index = list(a1_dict.keys())
        return df

    def get_port_return_ts(self):
        a1_dict = self.load()
        df = pd.concat([a1.get_port_return()
                       for key, a1 in a1_dict.items()], axis=1).T
        df.index = list(a1_dict.keys())
        return df

    def get_port_cum_return_ts(self):
        total_col = 'Total'
        return_mat = self.get_port_return_ts()
        total_return = return_mat.loc[:, total_col]
        total_wealth = (total_return + 1).cumprod().shift(1).fillna(1)
        addable_return_mat = return_mat.mul(
            total_wealth, axis=0).shift(1).fillna(0)
        wealth_mat = addable_return_mat.cumsum(axis=0) + 1
        return wealth_mat

    def get_port_ts_data(self):
        return {
            "Exposure": self.get_port_exposure_ts(),
            "Exposure (Vol Adj.)": self.get_port_voladj_exposure_ts(),
            "Correlation": self.get_port_correlation_ts(),
            "Risk Contri.": self.get_port_risk_ts(),
            "Risk Contri. (%)": self.get_port_risk_pct_ts(),
            "Return Contri.": self.get_port_return_ts(),
            "Cum Return Contri.": self.get_port_cum_return_ts()
        }
