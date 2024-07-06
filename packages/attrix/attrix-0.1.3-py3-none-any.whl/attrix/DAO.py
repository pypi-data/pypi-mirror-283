import pandas as pd
import datetime
from os.path import join
from functools import reduce
import json
import warnings
import logging

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

class RiskModelReader:
    model_dates = [],
    model_meta = {
      'model_id': None,
      'model_path': None,
      'model_folder': None,
      'file_path': None,
      'file_prefix': None,
      'file_suffix': None,
      'model_start_date': None,
      'model_desc': None,
      'model_calendar': None,  # i.e. USA
      'file_folder': {},
      'file_structure': {},
      'model_calendar_path': None
    }
    
    def __init__(self, meta_file):
        with open(meta_file) as f:
            self.model_meta.update(json.load(f))
        self.model_dates = self._get_model_dates()
    
    @staticmethod
    def _dated_to_yyyy_mm(dated):
        dt = datetime.datetime.strptime(dated, '%Y-%m-%d')
        return dt.strftime('%Y'), dt.strftime('%m')
    
    @staticmethod
    def _isc_to_dense(df_isc):
        P, rows, cols = df_isc.set_index(('SecurityId1','SecurityId2'))['Covariance'].to_sparse().to_coo()
        return pd.DataFrame(P.todense(), columns=cols, index= rows)
    
    def _get_folder(self, dated, file):
        yyyy, mm =  self._dated_to_yyyy_mm(dated)
        return self.model_meta.get('file_path').format(model_path=self.model_meta.get('model_path'),
                                                       model_folder=self.model_meta.get('model_folder'), 
                                                       file_folder=self.model_meta.get('file_folder')[file], 
                                                       yyyy=yyyy, mm=mm)
    
    def _get_file_path(self, dated, file):
        dt = datetime.datetime.strptime(dated, '%Y-%m-%d')
        file_prefix = self.model_meta.get('file_prefix')
        file_suffix = self.model_meta.get('file_suffix')
        file_prefix = datetime.datetime.strftime(dt, file_prefix) if file_prefix is not None else ''
        file_suffix = datetime.datetime.strftime(dt, file_suffix) if file_suffix is not None else ''
        return join(self._get_folder(dated, file), file_prefix + file + file_suffix)
    
    def _get_model_dates(self, end_date = datetime.date.today().strftime('%Y-%m-%d')):
        model_dates = pd.bdate_range(start=self.model_meta.get('model_start_date'), end=end_date).strftime('%Y-%m-%d').to_list()
        if self.model_meta.get('model_calendar') is not None:
            with open(self.model_meta.get('model_calendar_path')) as holidaycal_file:
                holidaycal = json.load(holidaycal_file)[self.model_meta.get('model_calendar')]
            model_dates = [day for day in model_dates if day not in holidaycal]
        return model_dates
    
    def _read_files(self, file_type, files):
        if file_type in ('idm', 'att', 'exp', 'zsc', 'cov', 'ret', 'fmp', 'comp_idm', 'comp_att', 'comp_exp'):
            return reduce(lambda df_left, df_right: pd.merge(df_left, df_right, left_index=True, right_index=True, how='left'), 
                          [pd.read_csv(x, index_col=0) for x in files])
        elif file_type in ('rsk','comp_rsk'):
            return reduce(lambda df_left, df_right: pd.merge(df_left, df_right, left_index=True, right_index=True, how='left'), 
                          [pd.read_csv(x, index_col=0) for x in files])[['TotalRisk', 'SpecificRisk']]
        elif file_type in ('isc','comp_weight'):
            return pd.concat([pd.read_csv(x) for x in files], axis=0)
        else:
            logging.warning('File type not recognized.')
            return pd.DataFrame()
                  
    def get_risk_model_data(self, dated, data_types=[]):
        if dated not in self.model_dates:
            dated_ = dated
            dated = max([d for d in self.model_dates if d < dated])
            logging.warning(f'The date {dated_} is not within the model dates, use {dated} instead')
        logging.debug('Getting risk model data from flat files for {}.'.format(dated))
        file_structure = self.model_meta.get('file_structure')
        if len(data_types)>0:
            file_structure = {key: file_structure.get(key) for key in data_types if key in file_structure.keys()}
        files = self.model_meta.get('file_folder').keys()
        rmd = {k: self._read_files(k, [self._get_file_path(dated, x) for x in fls if x in files]) 
                    for k, fls in file_structure.items()}
        return rmd

class BaseDAO:
    _reader = None

    def __init__(self, config = None):
        self.config = {
                "meta_file": None,
        }
        if config is not None:
            self.config.update(config)
        if self.config.get('meta_file') is not None: 
            self.set_reader(self.config.get('meta_file'))

    def set_reader(self, meta_file):
        self.config['meta_file'] = meta_file
        self._reader = RiskModelReader(meta_file)

    def _get_concat_data(self, t, axis=0, reset_index=True):
        if self._reader is None:
            raise ValueError('Reader not set up yet!')
        data_types = self.config.get('data_types')
        data = self._reader.get_risk_model_data(t, data_types=data_types)
        if reset_index:
            return pd.concat(data.values(),axis=axis).reset_index()
        else:
            return pd.concat(data.values(),axis=axis)


class SecurityDAO(BaseDAO):
    DEFAULT_CONFIG = {
            'meta_file': None,
            'mapping_cols': [],
            'time_col': 'Date',
            'id_col': 'SecurityID',
            'portfolio_col': 'Portfolio',
            'weight_col': 'Weight',
            'data_types': ['idm','comp_idm']
    }
    def __init__(self, config = None):
        config_ = self.DEFAULT_CONFIG
        if config is not None:
            config_.update(config)
        super().__init__(config_)
        print('Available mappings: (Ticker,Country), (SEDOL7) or (CUSIP)')

    def set_mapping_cols(self, mapping_cols):
        self.config['mapping_cols'] = mapping_cols

    def map(self, df):
        time_col = self.config.get('time_col')
        df_ = df.groupby([time_col])[df.columns].apply(self._map_one)
        df_.reset_index(drop=True, inplace=True)
        return(df_)

    def _map_one(self, df):
        config = self.config
        id_col, time_col, portfolio_col, mapping_cols = config.get('id_col'), config.get('time_col'), config.get('portfolio_col'), config.get('mapping_cols')
        init_id_col = mapping_cols[0]
        t = df[time_col].iloc[0]

        data = self._get_concat_data(t, axis=0, reset_index=True)
        df_ = df.merge(data, how='left', on=mapping_cols)
        df_['Status'] = 'Mapped'
        df_.loc[df_[id_col].isna(),'Status'] = 'Unknown'
        user_portfolios = list(df_[portfolio_col].unique())
        df_.loc[df_[init_id_col].isin(user_portfolios),'Status'] = 'User Provided'
        df_.loc[df_[id_col].isna(),id_col] = df_.loc[df_[id_col].isna(),init_id_col].values # let the unknown security be the initial id
        return(df_)

    def to_weight_list(self, df, t):
        """
        Convert a mapped dataframe to a dict of weights on one point-in-time (only include the covered assets)
        """
        config = self.config
        time_col, id_col, portfolio_col, weight_col = config.get('time_col'), config.get('id_col'), config.get('portfolio_col'), config.get('weight_col')
        df = df[(df[time_col]==t) & (df['Status']!='Unknown')] 
        portfolios = list(df[portfolio_col].unique())
        return {p: df[df[portfolio_col]==p].set_index(id_col)[weight_col] for p in portfolios}


class ETFDAO(BaseDAO):
    DEFAULT_CONFIG = {
            "meta_file": None,
            "data_types": ["comp_weight"],
            "weight_col": "ConstituentWeight",
            "id_col": "ConstituentID",
            "composite_id_col": "CompositeID"
    }

    def __init__(self, config = None):
        config_ = self.DEFAULT_CONFIG
        if config is not None:
            config_.update(config)
        super().__init__(config_)

    def get_etf_weight_list(self, ids, dated):
        composite_id_col = self.config.get('composite_id_col')
        data = self._get_concat_data(dated, reset_index=False)
        data = data[data[composite_id_col].isin(ids)]
        comp_ids = list(data.CompositeID.unique())
        return {comp_id: self._get_weights(data[data[composite_id_col]==comp_id]) for comp_id in comp_ids}

    def _get_weights(self, df):
        weight_col = self.config.get('weight_col')
        id_col = self.config.get('id_col')
        return df.set_index(id_col)[weight_col]


class SecurityReturnDAO(BaseDAO):
    DEFAULT_CONFIG = {
            "meta_file": None,
            "data_types": ["att","comp_att"],
            "price_col": "Price"
    }

    def __init__(self, config = None):
        config_ = self.DEFAULT_CONFIG
        if config is not None:
            config_.update(config)
        super().__init__(config_)

    def _get_price_at_t(self, t):
        config = self.config
        price_col = config.get('price_col')
        data = self._get_concat_data(t, axis=0, reset_index=False)
        return data.loc[:,price_col]

    def get_forward_return_mat(self, t_list): 
        price_mat = pd.DataFrame({t: self._get_price_at_t(t) for t in t_list})
        price_mat.ffill(axis=1, inplace=True)
        return_mat = price_mat.pct_change(axis=1).shift(periods=-1,axis=1)
        return return_mat

    def get_forward_return(self, t):
        next_t = self.get_next_t(t)
        if next_t is not None:
            return self.get_forward_return_mat([t,next_t]).iloc[:,0]
        else:
            return self.get_forward_return_mat([t]).iloc[:,0]

    def set_t_list(self, t_list):
        self.t_list = t_list

    def get_next_t(self,t):
        t_list = self.t_list
        idx = t_list.index(t)
        if idx >= len(t_list)-1:
            return None
        else:
            return t_list[idx+1]


class FactorReturnDAO:
    rmr = None
    config = {
            "meta_file": None,
            "start_date": None,
            "end_date": None,
            "data_type": ["ret"],
            "column": "Return"
    }

    def __init__(self, rmr = None, config = None):
        if config is not None:
            self.config.update(config)
        if rmr is not None:
            self.rmr = rmr
        else:
            self.rmr = RiskModelReader(self.config.get('meta_file'))

    def set_start_date(self, dated):
        self.config['start_date'] = dated

    def set_end_date(self, dated):
        self.config['end_date'] = dated

    def _get_dates(self, start_date=None, end_date=None):
        rmr = self.rmr
        if start_date is None:
            start_date = self.config.get("start_date")
        if end_date is None:
            end_date = self.config.get("end_date")
        dates = rmr.model_dates
        dates = [dated for dated in dates if (dated<=end_date) & (dated>=start_date)]
        return dates

    def _get_column_dated(self, dated):
        rmr = self.rmr
        config = self.config
        data_dict = rmr.get_risk_model_data(dated, config.get("data_type"))
        data = pd.concat(list(data_dict.values()), axis=0)
        return data.loc[:,config.get("column")]

    def get_forward_return(self, dates=None): 
        if dates is None:
            dates = self._get_dates()
        ts_mat = pd.DataFrame({dated: self._get_column_dated(dated)/100 for dated in dates})
        ts_mat = ts_mat.shift(-1, axis=1)
        return ts_mat
