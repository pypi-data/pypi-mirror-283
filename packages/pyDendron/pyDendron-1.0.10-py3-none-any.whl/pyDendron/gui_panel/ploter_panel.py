"""
Ploter panel
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import numpy as np
import pandas as pd
import json
from datetime import datetime

from pathlib import Path
import param
import panel as pn
from panel.viewable import Viewer
from bokeh.io import export_svgs
from bokeh.models import ColumnDataSource


from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.dataset import Dataset
from pyDendron.gui_panel.dataset_package import DatasetPackage

from pyDendron.chronology import data2col
from pyDendron.ploter import Ploter
#from pyDendron.gui_panel.dataset_package import DatasetPackage

class PloterPanel(Viewer):

    def __init__(self, dataset, parameters, cfg_path, **params):
        super(PloterPanel, self).__init__(**params)   
        bt_size = 75
        self.dataset = dataset
        self.parameters = parameters
        
        self.cfg_file = cfg_path / Path(f'pyDendron.ploter.cfg.json')
            
        self.dataset_package = DatasetPackage(dataset, parameters.column, parameters.package, 
                                                      parameters.detrend, parameters.chronology, name='')
        self.dataset_package.param.watch(self._sync_data, ['notify_package_change'], onlychanged=True)

        self.ploter = self.load_cfg()
        
        self.sliding_select = pn.widgets.Select(name='Sliding serie', options=[])
        self.sliding_select.param.watch(self.on_sliding_select, ['value'], onlychanged=True)
        self.ploter.param.watch(self.on_sliding_select, ['y_delta', 'y_height', 'x_offset_mode', 
                                                                      'y_offset_mode', 'draw_type', 'cambium_estimation',
                                                                      ], onlychanged=True)
        
        self.ploter.param.watch(self._sync_data, ['data_type'], onlychanged=True)

        self.x_slider = pn.widgets.IntSlider(name='X Slider', start=0, end=8, step=1, value=0,
                                             sizing_mode='stretch_width')
        self.y_slider = pn.widgets.FloatSlider(name='Y Slider', start=0, end=8, step=1, value=0, 
                                             sizing_mode='stretch_width')
        
        self.x_slider.param.watch(self.on_slider_x, ['value'], onlychanged=True)
        self.y_slider.param.watch(self.on_slider_y, ['value'], onlychanged=True)
        self.bt_save = pn.widgets.Button(name='Save offset', icon='Save', button_type='primary', align=('start', 'center'), width=2*bt_size)
        self.bt_save.on_click(self.on_save_offset)
        
        layout_light = pn.Row(
            self.sliding_select,
            self.x_slider,
            self.y_slider,
            self.bt_save
        )
        self._layout = pn.Column(self.dataset_package, layout_light, self.ploter, name=self.name,
                                  margin=(5, 0), sizing_mode='stretch_width')
    def on_save_offset(self, event):
        pass
    
    def get_sidebar(self, visible=True):
        pploter = pn.Param(self.ploter, name='Dynamic')
        #reploter = pn.Param(self.ploter.param_replot, name='Reset')
        return pn.Card(pploter, title='Plot', sizing_mode='stretch_width', margin=(5, 0), collapsed=True, visible=visible)  

    def dump_cfg(self):
        with open(self.cfg_file, 'w') as fd:
            data = {
                'ploter' : self.ploter.param.serialize_parameters(),
            }
            json.dump(data, fd)

    def load_cfg(self):
        try:
            ploter = Ploter()
            if Path(self.cfg_file).is_file():
                with open(self.cfg_file, 'r') as fd:
                    data = json.load(fd)
                    ploter = Ploter(**Ploter.param.deserialize_parameters(data['ploter']))
        except Exception as inst:
            logger.warrning(f'ignore cfg ploter panel, version change.')
        finally:
            return ploter

    def __panel__(self):
        return self._layout

    def _sync_data(self, event):
        def data_change():
            if event.old is None:
                return True
            if len(event.new.index.to_list()) != len(event.old.index.to_list()):
                return True
            return False
    
        try:
            #if data_change():
            lst = self.dataset_package.data[KEYCODE].to_list() #if self.dataset_package.data is not None else []
            lst.reverse()
            self.sliding_select.options = ['None'] + lst
            
            if self.ploter.data_type == 'Raw':
                #print('ploter panel: raw data.', self.ploter.param_replot.data_type)
                self.ploter.prepare_and_plot(data=self.dataset_package.data)
            elif self.ploter.data_type == 'Detrend':
                #print('ploter panel: detrend data.', self.ploter.param_replot.data_type)
                self.ploter.prepare_and_plot(data=self.dataset_package.dt_data)
            elif self.ploter.data_type == 'Log':
                #print('ploter panel: log data.', self.ploter.param_replot.data_type)
                self.ploter.prepare_and_plot(data=self.dataset_package.log_data)
        except Exception as inst:
            logger.error(f'ploter panel: {inst}', exc_info=True)

    def on_sliding_select(self, event):
        if (self.sliding_select.value != 'None') and (self.ploter.draw_data is not None):
            keycode = self.sliding_select.value
            data = self.ploter.draw_data[keycode]
            fig = self.ploter.figure_pane.object
            self.x_slider.start =  int(fig.x_range.start - data[DATA_LENGTH])
            self.x_slider.end = int(data[DATA_LENGTH] + fig.x_range.end)
            self.x_slider.step = 1
            self.x_slider.value = data['x_offset']
            
            self.y_slider.start = fig.y_range.start - data['w_min'] 
            self.y_slider.end = fig.y_range.end + data['w_max']
            self.y_slider.value = data['y_offset']
            self.y_slider.step = (self.y_slider.end - self.y_slider.start) // 100
            
    def on_slider_x(self, event):
        if (self.ploter.draw_data is not None) and (self.sliding_select.value in self.ploter.draw_data):
            data_slide = self.ploter.draw_data[self.sliding_select.value]
            delta_x = data_slide['x_offset'] - self.x_slider.value
            data_slide['x_offset'] = self.x_slider.value
            for key, info in data_slide.items():
                if isinstance(info, ColumnDataSource):
                    for key in ['x', 'left', 'right']:
                        if key in info.data:
                            info.data[key] = [x - delta_x for x in info.data[key]]
    
    def on_slider_y(self, event):
        if (self.ploter.draw_data is not None) and (self.sliding_select.value in self.ploter.draw_data):
            fig = self.ploter.figure_pane.object
            info = self.ploter.draw_data[self.sliding_select.value]
            delta_y = info['y_offset'] - self.y_slider.value
            info['y_offset'] = self.y_slider.value

            for key, value in info.items():
                if isinstance(value, ColumnDataSource):
                    for key in ['y', 'top', 'bottom']:
                        if key in value.data:
                            value.data[key] = [y - delta_y for y in value.data[key]]
            
            #print('before', info['y_label'], fig.yaxis.major_label_overrides)
            old_y_mean = info['y_label']
            info['y_label'] = round(info['w_mean'] + info['y_offset'], 3)
            self.ploter.on_legend()
            #print('after', info['y_mean'], fig.yaxis.major_label_overrides)

