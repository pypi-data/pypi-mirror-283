"""
Package 
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import pandas as pd
import param
import numpy as np
import panel as pn
import copy
from panel.viewable import Viewer

from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters,
                                           _cell_formatters, _hidden_columns, _get_selection)
from pyDendron.estimation import cambium_estimation

class DatasetPackage(Viewer): 
    notify_package_change = param.Event()

    VALUES_PER_LINE = 20
          
    def __init__(self, dataset, param_column, param_package, param_detrend=None, param_chronology=None, **params):
        super(DatasetPackage, self).__init__(**params)   
        self._dt_data = pd.DataFrame()
        self.dt_param = {}
        
        self.param_package = param_package
        #self.param_package.param.watch(self.sync_show_data,  ['show_data'], onlychanged=True)

        self.param_detrend = param_detrend
        if self.param_detrend is not None:
            self.param_detrend.param.watch(self._sync_dt_data,  ['detrend', 'window_size', 'log'], onlychanged=True )
        
        self.param_chronology = param_chronology
        if self.param_chronology is not None:
            self.param_chronology.param.watch(self._sync_dt_data,  ['biweight_mean', 'date_as_offset'], onlychanged=True)

        self.param_column = param_column
        self.wcolumn_selector = self.param_column.columns
        self.wcolumn_selector.param.watch(self.sync_columns, ['value'], onlychanged=True)

        self.dataset = dataset
        self.dataset.param.watch(self.sync_dataset,  ['notify_reload', 'notify_synchronize', 'notify_packages'], onlychanged=True)

        self.wselection_name = pn.widgets.Select(name='Name: '+self.name, options=[])
        self.wselection_name.param.watch(self.sync_data,  ['value'], onlychanged=True)

        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=list(dtype_view.keys())),
                                    hidden_columns=_hidden_columns(), 
                                    text_align=_cell_text_align(dtype_view),
                                    editors=_cell_editors(dtype_view), 
                                    header_filters=_header_filters(dtype_view), 
                                    formatters=_cell_formatters(dtype_view),
                                    frozen_columns=[ICON, KEYCODE], 
                                    show_index=False,
                                    pagination='local',
                                    page_size=100000,
                                    selectable='checkbox', 
                                    sizing_mode='stretch_width',
                                    #height=200,
                                    max_height=400,
                                    min_height=300,
                                    height_policy='max',
                                    row_content = self.get_row_content,
                                    #embed_content=,
                                    #groupby=[KEYCODE+'Parent'],
                                    ) 
        self.wtabulator.param.watch(self.on_selection, ['selection'], onlychanged=True)
        
        self.panel_tabulator = pn.Card(self.wtabulator, margin=(5, 0), collapsed=True, 
                                       sizing_mode='stretch_width',  
                                       #min_height=300,
                                       #max_height=450,
                                       #height_policy='max',

                                       title='Data '+self.name, collapsible=True)
        
        stylesheet = 'p {padding: 0px; margin: 0px;}'
        self.dt_info = pn.pane.Alert('Detrend data is empty set', margin=(0, 0, 5, 5), align=('start', 'end'), stylesheets=[stylesheet])
        
        self._layout = pn.Column(pn.Row(self.wselection_name, self.dt_info), self.panel_tabulator)

    def clone(self, name=''):
        return DatasetPackage(self.dataset, param_column=self.param_column, param_package=self.param_package, 
                              param_detrend=self.param_detrend, param_chronology=self.param_chronology, name=name) 

    def get_package_name(self):
        return self.wselection_name.value

    def on_selection(self, event):
        self.param.trigger('notify_package_change')

    def get_row_content(self, series):
        def array2html(v):
            l = len(v)
            nl = (l + 1) // self.VALUES_PER_LINE + 1
            tmp = np.array([0.0] * nl * self.VALUES_PER_LINE, dtype=object)
            tmp[0:l] = v
            tmp[tmp == 0] = pd.NA
            tmp[len(v)] = ';'
            c = list(range(0, nl * self.VALUES_PER_LINE, self.VALUES_PER_LINE))
            return pd.DataFrame(tmp.reshape(-1, self.VALUES_PER_LINE).T, columns=c).T.style.format(precision=2)
        
        try:
            print('get_row_content')
            #if self.param_package.show_data:
            lst = []
            if series[DATA_VALUES] is not None:
                lst.append((RAW, array2html(series[DATA_VALUES])))
                if self._dt_data is not None:
                    dt_type = self._dt_data.at[series.name, DATA_TYPE]
                    if dt_type != RAW:
                        lst.append((dt_type, array2html(self._dt_data.at[series.name, DATA_VALUES])))
            return pn.Tabs(*lst)
            #return pn.pane.Markdown(f'Show data desactivated in package card: {self.param_package.show_data}')
        except Exception as inst:
            #logger.error(f'get_row_content: {inst}', exc_info=True)
            return pn.pane.Markdown('No detrend data, synchro error.')
        return pn.pane.Markdown('Detrend param is missing')
        
        #a = self._dt_data.at[idx, DATA_VALUES]
        #pn.pane.HTML(f'<span>{self._dt_data.at[idx, DATA_TYPE]}: {a}</span>')        

    def __panel__(self):
        return self._layout

    def sync_columns(self, event):
        self.wtabulator.hidden_columns = _hidden_columns(self.wcolumn_selector.value)

    def sync_dataset(self, event):
        lst = self.dataset.package_keys()
        #logger.info(f'sync_dataset  {self.name}, {lst}')
        self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        self._dt_data = pd.DataFrame()
        self.dt_param = {}
        #logger.info(f' --> sync_dataset  {self.wselection_name.value}, {self.wselection_name.options}')
        self.wselection_name.options = ['None']+lst
        #logger.info(f' --> sync_dataset  {self.wselection_name.value}, {self.wselection_name.options}')
        #if self.wselection_name.value is not None:
        #    self.sync_data(event)

    # def sync_show_data(self, event):
    #     try:
    #         self._layout.loading = True
    #         #if self.param_package.show_data:
    #         #    self.wtabulator.row_content = self.get_row_content
    #         #else:
    #         #    self.wtabulator.row_content = None
    #         self.wtabulator.value = copy.copy(self.wtabulator.value)
    #     except Exception as inst:
    #         logger.error(f'sync_data: {inst}', exc_info=True)
    #         data = pd.DataFrame(columns=list(dtype_view.keys()))
    #         self.wtabulator.value = data
    #     finally:
    #         self._layout.loading = False

    def do_cambium_estimation(self, data):
        data[[CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = pd.NA
        for idx, row in data.iterrows():
            #           param, cambium, bark, sapwood, values
            data.loc[idx, [CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = cambium_estimation(self.param_package, row[CAMBIUM], row[BARK], row[SAPWOOD], row[DATA_VALUES])
                
    def sync_data(self, event):
        try:
            self._layout.loading = True
            tmp_data = pd.DataFrame()
            #logger.info(f'sync_data  {self.name}, {self.get_package_name()}')
            package_name = self.get_package_name()
            if package_name != 'None':

                tmp_data = self.dataset.get_package_components(package_name).reset_index()
                tmp_data.insert(len(tmp_data.columns)-1, OFFSET, tmp_data.pop(OFFSET))
                tmp_data.insert(0, ICON, tmp_data.apply(lambda x: category_html(x), axis=1))
                tmp_data = tmp_data.sort_values(by=KEYCODE)
                self.do_cambium_estimation(tmp_data)
                self.wtabulator.hidden_columns = _hidden_columns(self.wcolumn_selector.value)
                self.wtabulator.value = tmp_data
            else:
                self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        except Exception as inst:
            logger.error(f'sync_data: {inst}', exc_info=True)
            tmp_data = pd.DataFrame(columns=list(dtype_view.keys()))
            self.wtabulator.value = tmp_data
        finally:
            self._sync_dt_data(event)
            self._layout.loading = False
    
    def get_data(self):
        if len(self.wtabulator.value) == 0:
            return self.wtabulator.value
        return self.wtabulator.value.loc[self.wtabulator.value[CATEGORY].isin([CHRONOLOGY, TREE]),:]

    @property
    def data(self):
        d = _get_selection(self.wtabulator)
        if len(d) <= 0:
            d = self.wtabulator.value        
        #print('--> data selection', d.index, self.wtabulator.value.index)
        return d.loc[self.wtabulator.value[CATEGORY].isin([CHRONOLOGY, TREE]),:]

    @property
    def dt_data(self):
        d = _get_selection(self.wtabulator)
        if len(d) <= 0:
            return self._dt_data
        return self._dt_data[self._dt_data.index.isin(d.index)]

    @property
    def log_data(self):
        def apply_log(array):
            return np.log(array)
        
        df = copy.deepcopy(self.data)
        df[DATA_VALUES] = df[DATA_VALUES].apply(apply_log)
        return df

    def _sync_dt_data(self, event):
        def get_dt_param():
            dt_param = {}
            if self.param_detrend is not None:
                dt_param[DETREND] = self.param_detrend.detrend
                dt_param[DETREND_WSIZE] = self.param_detrend.window_size
                dt_param[DETREND_LOG] = self.param_detrend.log
                dt_param[CHRONOLOGY_DATE_AS_OFFSET] = self.param_chronology.date_as_offset
                dt_param[CHRONOLOGY_BIWEIGHT_MEAN] = self.param_chronology.biweight_mean
            return dt_param
        
        try:
            self._layout.loading = True
            tmp_data = self.get_data()
            
            
            idxs = tmp_data[IDX_CHILD].unique().tolist()
            #logger.info(f'_sync_dt_data  {self.name}')
            
            tmp_dt_data = tmp_data
            if len(idxs) <= 0:
                #print('Detrend data is empty set')
                tmp_dt_data = None
                tmp_data = None
                self.dt_info.object = 'Detrend data is empty set'
                self.dt_info.alert_type = 'warning'

            elif (self.param_detrend is  None) or (self.param_detrend.detrend == RAW):
                #print('Detrend data is raw data.')
                self.dt_info.object = 'Detrend data is raw data. '
                self.dt_info.alert_type = 'primary'
            else:
                #print('Detrend other.')
                if len(idxs) != len(tmp_data[IDX_CHILD]):
                    logger.warning(f'Duplicate series in package {self.name}')
                tmp_dt_data = tmp_data[[IDX_CHILD, IDX_PARENT, OFFSET, CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]]
                #print('*tmp_dt_data', tmp_dt_data.columns)
                res = self.dataset.detrend(idxs, self.param_detrend.detrend, self.param_detrend.window_size, 
                                                    self.param_detrend.log, self.param_chronology.date_as_offset, 
                                                    self.param_chronology.biweight_mean)      
                #print('*res', res.columns)
                tmp_dt_data = tmp_dt_data.join(res, on=IDX_CHILD, how='left')
                #print('*tmp_dt_data end', tmp_dt_data.columns)
                self.dt_info.alert_type = 'info'
                if self.param_detrend.log and (self.param_detrend.detrend != BP73):
                    c = f'Detrend data is log({self.param_detrend.detrend}) data. '
                else:
                    c = f'Detrend data is {self.param_detrend.detrend} data. '
                
                c += ', '.join([f'{index}: {valeur}' for index, valeur in tmp_dt_data[CATEGORY].value_counts().items()]) +' in the package. '
                self.dt_info.object = c
                
                if tmp_dt_data[INCONSISTENT].any():
                    self.dt_info.object += ' one or more series is inconsistent.'
                    self.dt_info.alert_type='warning'
                else:
                    self.dt_info.alert_type='primary'
        except Exception as inst:
            #self.wtabulator.value = self.wtabulator.value.copy()
            self.dt_info.object = 'Detrend data is raw data'
            logger.error(f'_sync_dt_data: {inst}', exc_info=True)
        finally:
            self.dt_param = get_dt_param()
            self._dt_data = tmp_dt_data
            self.param.trigger('notify_package_change')
            self._layout.loading = False
    
    def save(self):
        save_package(self.wtabulator.value, self.get_package_name(), self.dataset)

def save_package(dataframe, package_name, dataset):
    #def nan_(df, key):
    #    mask = df[key].isna()
    #    return df.index[mask].to_list()
    
    def get_missing_keycodes(df, key):
        mask = df[key].isna()
        return df.loc[mask, KEYCODE].to_list()
    
    if package_name == '':
        logger.warning(f'Selection name is empty')
    else:
        df = dataframe.set_index([IDX_PARENT, IDX_CHILD], verify_integrity=True)
        paires = df.index.tolist()            
        missing_date_begin = get_missing_keycodes(df, DATE_BEGIN)
        if len(missing_date_begin) > 0:       
            logger.warning(f'{DATE_BEGIN} is missing for {missing_date_begin}')
        missing_offset = get_missing_keycodes(df, OFFSET)
        if len(missing_offset) > 0:       
            logger.warning(f'{OFFSET} is missing for {missing_offset}')
        missing_ring_values = get_missing_keycodes(df, DATA_VALUES)
        if len(missing_ring_values) == 0:      
            dataset.set_package(package_name, paires)
            dataset.dump()
            #(f'Save selection')
        else:
            logger.warning(f'Selection is not save, missing {DATA_VALUES} for {missing_ring_values}')
                
            

        



