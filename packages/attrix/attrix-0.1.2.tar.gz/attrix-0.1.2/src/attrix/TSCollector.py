import pickle
import re
import os
import datetime

"""
The class is able to achieve:
1. Specify path and file name convention
2. Create new objects in the memory
3. Save the object to dated file
4. Load the dated file to object dict
5. Apply an operation to each object in the object dict
"""

class TSCollector:
    """
    Time-series object collector.

    Load objects from pickle data or save objects to pickle data.
    """
    def __init__(self, config=None):
        default_config = {
                "path": ".",
                "file_format": "%Y-%m-%d",
                "time_format": "%Y-%m-%d",
                "pattern": "^[0-9-]{10}$"
        }
        if config is not None:
            default_config.update(config)
        self.config = default_config
        self._cache = {}

    @staticmethod
    def _convert(x, format1, format2):
        return datetime.datetime.strptime(x,format1).strftime(format2)

    def _file_to_time(self, x):
        file_format = self.config.get('file_format')
        time_format = self.config.get('time_format')
        return self._convert(x, file_format, time_format)
    
    def _time_to_file(self, x):
        file_format = self.config.get('file_format')
        time_format = self.config.get('time_format')
        return self._convert(x, time_format, file_format)

    @property
    def f_list(self):
        """
        List of existing files.
        """
        path, pattern = self.config.get('path'), self.config.get('pattern')
        if os.path.exists(path):
            regex = re.compile(pattern)
            l = list(filter(regex.match, os.listdir(path)))
            l.sort()
        else:
            l = []
        return l

    @property
    def t_list(self):
        """
        Time list that corresponds to each existing file.
        """
        l = [self._file_to_time(f) for f in self.f_list]
        l.sort()
        return l

    def load_one(self, t):
        """
        Load from 1. cache; 2. pickle file.
        """
        if t not in self._cache.keys():
            f = self._time_to_file(t)
            path = self.config.get('path')
            with open(os.path.join(path,f), 'rb') as file:
                self._cache[t] = pickle.load(file)
        return self._cache.get(t)

    def save_one(self, t):
        """
        Save the cached data to pickle file.
        """
        if t in self._cache.keys():
            f = self._time_to_file(t)
            path = self.config.get('path')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path,f), 'wb') as file:
                pickle.dump(self._cache.get(t), file)

    def load(self, t_list=None):
        if t_list is None:
            t_list = self.t_list
        return {t: self.load_one(t) for t in t_list}

    def save(self, replace=False):
        """
        Save the cached dict of objects to a series of files.

        Parameters:
        data_dict (dict): Object dict tagged with time.
        replace (bool): Replace existing file.
        """
        for t, data in self._cache.items():
            if replace or (t not in self.t_list):
                self.save_one(t)