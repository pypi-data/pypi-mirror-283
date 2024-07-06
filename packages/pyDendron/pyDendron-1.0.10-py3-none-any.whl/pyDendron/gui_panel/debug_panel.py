"""
Debug and log class
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

import pandas as pd
import panel as pn
import param
import sys
from panel.viewable import Viewer

from pyDendron.dataname import *
from pyDendron.app_logger import logger#, stdout_stream_handler

class DebugPanel(Viewer):
    """ Tools to manage dataset. """
        
    def __init__(self, dataset, parameters, app, **params):
        super().__init__(**params)
        self.dataset = dataset
        self.app = app
        self.parameters = parameters
        self.wlog = None
        self.wcrossdating_log = None
        
        # Logger
        self.terminal = pn.widgets.Terminal(
            "Debugger terminal\n\n",
            options={"cursorBlink": True},
            sizing_mode='stretch_both'
        )
        sys.stdout = self.terminal
        #stdout_stream_handler.setStream(self.terminal)
        
        self._layout = pn.Tabs(
            ('Debug', self.terminal), 
            ('Dataset Log', self._log()),
            ('Crossdating Log', self._crossdating_log()),
            ('id Log', self._id()),
            dynamic=False, margin=0, styles={'font-size': '16px'}, name=self.name)
        
        self._layout.param.watch(self.on_tab_change, ['active'], onlychanged=True)

    def __panel__(self):
        """ Return the panel layout."""
        return self._layout

    def _id(self):
        def get_id(event):
            from bokeh.io import curdoc
            doc = curdoc()
            
            id = int_input.value
            print(f"Get id {id}")
            print(doc.get_model_by_id(id))

        int_input = pn.widgets.IntInput(name='id', value=0)
        button = pn.widgets.Button(name='get', button_type='primary')
        button.on_click(get_id)
        
        return pn.Column(int_input, button)
        
    def _log(self):
        self.wlog = pn.widgets.Tabulator(
                            show_index=False,
                            sizing_mode='stretch_width',
                            max_height=800,
                            min_height=400,
                            height_policy='max',
                            )
        return pn.Column(
            self.wlog
        )
    
    def _crossdating_log(self):
        self.wcrossdating_log = pn.widgets.Tabulator(
                            show_index=False,
                            sizing_mode='stretch_width',
                            max_height=800,
                            min_height=400,
                            height_policy='max',
                            )
        return pn.Column(
            self.wcrossdating_log
        )

    def on_tab_change(self, event):
        """ Handle tab change event. """
        if self._layout.active == 1:
            self.wlog.value = self.dataset.get_log()
        elif self._layout.active == 2:
            self.wcrossdating_log.value = self.dataset.get_crossdating_log()
