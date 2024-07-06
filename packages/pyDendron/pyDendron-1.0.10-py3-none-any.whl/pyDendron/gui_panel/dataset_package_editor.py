"""
Package Editor
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"


import pandas as pd
import param
import panel as pn
from panel.viewable import Viewer
from pathlib import Path
from io import BytesIO

from pyDendron.app_logger import logger
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.dataname import *
from pyDendron.gui_panel.tabulator import (_get_selection, get_download_folder, unique_filename)

class DatasetPackageEditor(Viewer):
    selection = param.List(default=[], doc='path')

    def __init__(self, dataset, parameters, **params):
        bt_size = 150
        super(DatasetPackageEditor, self).__init__(**params) 
        
        self.dataset = dataset
        self.param_column = parameters.column
        self.param_column_stats = parameters.column_stats
        self.package = DatasetPackage(dataset, parameters.column, parameters.package, name='')
        self.panel_tabulator = self.package.panel_tabulator
        self.wselection_name = self.package.wselection_name
        self.wselection_name.param.watch(self.on_package_selected,  ['value'], onlychanged=True)

        self.wtabulator = self.package.wtabulator
        
        self.bt_delete = pn.widgets.Button(name='Delete package', icon='file-off', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_delete.on_click(self.on_delete)
        self.bt_erase = pn.widgets.Button(name='Remove row', icon='eraser', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_erase.on_click(self.on_erase)
        
        self.bt_save = pn.widgets.Button(name='Save package', icon='file', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_save.on_click(self.on_save)

        self.bt_stats = pn.widgets.Button(name='Add', icon='add', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_stats.on_click(self.on_stats)

        self.bt_excel = pn.widgets.FileDownload(callback=self.on_excel, filename='package.xlsx', embed=False, 
                                                label='Download Excel', icon='file-export', button_type='primary', 
                                                width=bt_size, align=('start', 'end'))

        self._layout = pn.Column(self.package, 
                                 pn.Row(self.param_column_stats.get_widgets(), self.bt_stats), 
                                 pn.Row(self.bt_erase, self.bt_delete, self.bt_save, self.bt_excel),
                                )
        self.panel_tabulator.collapsed = False
    
    def on_package_selected(self, event):
        self.bt_excel.filename = 'pkg_' +self.wselection_name.value + '.xlsx'
    
    def __panel__(self):
        return self._layout

    def on_excel(self):
        try:
            if (self.wselection_name.value == ''):
                logger.warning('No package')
                return None
            if (self.wtabulator.value is None) or (len(self.wtabulator.value) <=0 ):
                logger.warning('No data')
                return None 

            output = BytesIO()
            with pd.ExcelWriter(output) as writer:
                cols = [x for x in self.wtabulator.value.columns.to_list() if x != ICON] 
                data = self.wtabulator.value[cols]
                data.to_excel(writer, sheet_name=self.wselection_name.value, merge_cells=False, float_format="%.6f")
            output.seek(0)
            return output
        except Exception as inst:
            logger.error(f'on_excel: {inst}', exc_info=True)


    def on_stats(self, event):
        try:
            if (self.wselection_name.value == ''):
                logger.warning('No package')
                return
            if (self.wtabulator.value is None) or (len(self.wtabulator.value) <=0 ):
                logger.warning('No data')
                return     
            self.wtabulator.value = self.dataset.statistics(data=self.wtabulator.value, 
                                            columns=self.wtabulator.value.columns.to_list(), 
                                            stat_columns=self.param_column_stats.get_columns())
        except Exception as inst:
            logger.error(f'on_excel: {inst}', exc_info=True)
        

    def on_delete(self, event):
        if self.wselection_name.value != '':
            self.dataset.delete_package(self.wselection_name.value)
    
    def on_save(self, event):
        try:
            self._layout.loading = True
            self.package.save()
        except Exception as inst:
            logger.error(f'on_erase: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            self._layout.loading = False

    def on_erase(self, event):
        try:
            self._layout.loading = True
            df_selection = _get_selection(self.wtabulator)
            #print('to check:', df_selection.index.to_list(), self.wtabulator.selection)
            self.wtabulator.value = self.wtabulator.value.drop(df_selection.index.to_list())
            #self.wtabulator.value = self.wtabulator.value.drop(self.wtabulator.selection)
        except Exception as inst:
            logger.error(f'on_erase: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False
