import os
import getpass
import argparse
import pyodbc

import panel as pn
from pathlib import Path
import json
from collections import namedtuple
from bokeh.server.contexts import BokehSessionContext

from pyDendron.dataset import Dataset
from pyDendron.gui_panel.sidebar import ParamColumns, ParamDetrend, ParamChronology, ParamPackage, ParamColumnStats
from pyDendron.gui_panel.dataset_selector import DatasetSelector
from pyDendron.gui_panel.dataset_treeview import DatasetTreeview
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.dataset_package_builder import DatasetPackageBuilder
from pyDendron.gui_panel.dataset_package_editor import DatasetPackageEditor
#from pyDendron.gui_panel.dataset_package_statistics import DatasetPackageStatistics
from pyDendron.gui_panel.tools_panel import ToolsPanel
from pyDendron.gui_panel.ploter_panel import PloterPanel
from pyDendron.gui_panel.debug_panel import DebugPanel
from pyDendron.gui_panel.crossdating_panel import CrossDatingPanel
from pyDendron.app_logger import logger

DendronInfo = namedtuple('DendronInfo', ['www', 'username', 'dendron_path', 'dataset_path', 'cfg_path', 'tmp_path'])

def directory(www=False):
    """
    Create directory paths for local or server mode.

    Args:
        www (bool, optional): Flag indicating the mode.

    Returns:
        DendronInfo: An object containing the directory paths.

    """
    dataset_path = Path('./dataset')
    cfg_path = Path('./cfg')
    tmp_path = Path('./tmp')
    username = 'None'
    dendron_path = Path('./pyDendron')
    if www:
        if pn.state.user is not None: 
            username = pn.state.user
        dataset_path =  dataset_path / Path(username)
        cfg_path =  cfg_path / Path(username)
        tmp_path = tmp_path / Path(username)
    else:
        username = getpass.getuser()
        dendron_path = Path(os.path.expanduser("~")) / dendron_path
        dataset_path = dendron_path / dataset_path / Path(username)
        cfg_path = dendron_path / cfg_path / Path(username)
        tmp_path = dendron_path / tmp_path / Path(username)

    os.makedirs(dataset_path, exist_ok=True)
    os.makedirs(cfg_path, exist_ok=True) 
    os.makedirs(tmp_path, exist_ok=True) 
    return DendronInfo(www=www, username=username, dendron_path=dendron_path, dataset_path=dataset_path, 
                       cfg_path=cfg_path, tmp_path=tmp_path)

def set_extension():
    """
    Set the required extensions for the pyDendron panel.

    This function enables the necessary extensions for the pyDendron panel to function properly.
    It enables the 'throttled', 'notifications', 'tabulator', and 'loading_spinner' extensions.
    It also sets the loading indicator to True and disables the console output.

    Parameters:
        None

    Returns:
        None
    """
    pn.extension(throttled=True)
    pn.extension(notifications=True)
    pn.extension('tabulator')
    pn.extension(loading_spinner='dots')
    pn.param.ParamMethod.loading_indicator = True

    pn.extension('terminal')
    pn.config.console_output = 'disable'

    pn.extension('tabulator')
    pn.extension(
        disconnect_notification="""Server Connected Closed <br /> <button class="btn btn-outline-light" onclick="location.reload();">Click To Reconnect</button> """
    )

class Parameters:
    """
    Class representing the parameters for pyDendron.
    """

    def __init__(self, app, cfg_path):
        self.app = app
        self.detrend = None
        self.chronology = None 
        self.column = None 
        self.column_stats = None
        self.package = None
        self.cfg_path = cfg_path
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)

        self.cfg_filename = cfg_path / Path('pyDendron.cfg.json')

        self.bt_save_parameters = pn.widgets.Button(name='Save parameters', icon="settings", button_type='default', align=('end', 'center'))
        self.bt_save_parameters.on_click(self.on_save_param)
        
        self.load()

    def get_widgets(self):
        return self.bt_save_parameters
    
    def save(self):
        logger.info('save parameters')
        with open(self.cfg_filename, 'w') as f:
            data = {
                'detrend' : self.detrend.param.serialize_parameters(),
                'chronology' : self.chronology.param.serialize_parameters(),
                'column' : self.column.columns.value,
                'column_stat': self.column_stats.columns.value,
                'package' : self.package.param.serialize_parameters(),
            }
            json.dump(data, f)
        self.app.ploter.dump_cfg()
        self.app.crossdating.dump_cfg()
    
    def on_save_param(self, event):
        self.save()
        pn.state.notifications.info('Parameters saved')
    
    def load(self):
        """
        Load the parameters from a configuration file.

        Args:
            cfg_filename (str): The path to the configuration file.

        Raises:
            Exception: If there is an error loading the configuration file.
        """
        try:
            if Path(self.cfg_filename).is_file():
                with open(self.cfg_filename, 'r') as f:
                    data = json.load(f)
                    self.detrend = ParamDetrend(**ParamDetrend.param.deserialize_parameters(data['detrend']))
                    self.chronology = ParamChronology(**ParamChronology.param.deserialize_parameters(data['chronology']))
                    self.column = ParamColumns(columnList=data['column'])
                    self.column_stats = ParamColumnStats(columnList=data['column_stat'])
                    self.package = ParamPackage(**ParamPackage.param.deserialize_parameters(data['package']))
            else:
                    #print('no cfg')
                    self.detrend = ParamDetrend()
                    self.chronology = ParamChronology()
                    self.column = ParamColumns()
                    self.column_stats = ParamColumnStats()
                    self.package = ParamPackage()
        except Exception as inst:
            logger.error(f'on_excel: {inst}', exc_info=True)
            logger.warning(f'ignore cfg files, version change.')
            self.detrend = ParamDetrend()
            self.chronology = ParamChronology()
            self.column = ParamColumns()
            self.column_stats = ParamColumnStats()
            self.package = ParamPackage()

class SidebarWidget:
    """
    A class representing a sidebar widget.

    Attributes:
        sidebar (object): The sidebar object.
        objects (dict): A dictionary to store the sidebar objects.
        hiddens (dict): A dictionary to store the paramters to hide depending of ative tab in main panel.
    """

    def __init__(self, app):
        # Add to sidebar
        self.sidebar = app.template.sidebar
        self.objects = {}
        self.hiddens = {}
        self.append_title('## Datasets')
        self.append(app.dataset_selector, 'dataset')
        self.append_title('## Parameters')
        self.append(app.parameters.column, 'param_column')
        self.append(app.parameters.package, 'param_package')
        self.append(app.parameters.detrend, 'param_detrend') 
        self.append(app.parameters.chronology, 'param_chronology')
        self.append(app.treeview, 'treeview')
        self.append(app.ploter, 'ploter')
        self.append(app.crossdating, 'crossdating')
        self.append(app.tools, 'tools')
        
        self.init_hiddens()
        self.active_parameters(app.treeview.name)
        
    def append(self, pane, name):
        """
        Append an parameter object to the sidebar.

        Args:
            pane (Viewer): The pane to be appended.
            name (str): The name of the object.
        """
        sidebar = pane.get_sidebar()
        self.objects[name] = sidebar
        self.sidebar.append(sidebar)

    def append_title(self, title):
        """
        Append a title to the sidebar.

        Args:
            title (str): The title to be appended.
            name (str): The name of the title.
        """
        self.sidebar.append(title)

    def init_hiddens(self):
        """
        Initialize the parameter objects to hide for a given the title of the tab.
        """
        self.hiddens['Treeview'] = ['ploter', 'crossdating', 'tools', 'param_detrend', 'param_package']
        self.hiddens['Package'] = ['treeview', 'ploter', 'crossdating', 'tools', 'param_detrend', 'param_chronology']
        self.hiddens['Ploter'] = ['treeview', 'crossdating', 'tools']
        self.hiddens['Crossdating'] = ['treeview', 'ploter', 'tools']
        self.hiddens['Tools'] = ['treeview', 'ploter', 'crossdating', 'param_detrend', 'param_chronology']
        self.hiddens['Tools'] = ['treeview', 'ploter', 'crossdating', 'tools', 'param_colums', 'param_package', 
                                 'param_detrend', 'param_chronology']
        self.hiddens['Debug'] = ['treeview', 'ploter', 'crossdating', 'tools', 'param_colums', 'param_package', 
                                 'param_detrend', 'param_chronology']

    def active_parameters(self, name):
        """
        Activate the parameters based on the given name of the active tab.

        Args:
            name (str): The name to determine which parameters to activate.
        """
        lst = self.hiddens[name]
        for param_name, param in self.objects.items():
            param.visible = False if param_name in lst else True

class DendronApp:
    """
    The main application class for pyDendron.
    
    Args:
        dendron_info (object): An object containing information about pyDendron.
    """
    def __init__(self, dendron_info):
        self.dendron_info = dendron_info
        self.parameters = Parameters(self, dendron_info.cfg_path)
        self.dataset = Dataset(username=self.dendron_info.username)
        #self.package = DatasetPackage(self.dataset, self.parameters.column, self.parameters.package, 
        #                                              self.parameters.detrend, self.parameters.chronology, name='Default')
        self.template = self.get_template()        
        self.dataset_selector = DatasetSelector(self.dataset, path=self.dendron_info.dataset_path, filters=['dataset*.p'], )
        
        self.treeview = DatasetTreeview(self.dataset, self.parameters, name='Treeview')
        self.tab_package = self.get_tab_package()
        self.ploter = PloterPanel(self.dataset, self.parameters, cfg_path=dendron_info.cfg_path, name='Ploter')
        self.crossdating = CrossDatingPanel(self.dataset, self.parameters, self.dendron_info.cfg_path, name='Crossdating')
        self.tools = ToolsPanel(self.dataset, self.parameters, self.dendron_info, filters=['dataset*.p'], name='Tools')
        self.debug = DebugPanel(self.dataset, self.parameters, self, name='Debug')
        #print('__init__', self.debug)
        
        self.tabs = tabs = pn.Tabs(self.treeview, self.tab_package, self.ploter, self.crossdating, self.tools, ('Debug', self.debug),
                dynamic=False, margin=0, styles={'padding' : '0px', 'font-size': '18px'})
        
        self.template.main.append(self.tabs)
        self.sidebar_widget = SidebarWidget(self)
        
        self.tabs.param.watch(self.on_activate, ['active'], onlychanged=True)

    def get_tab_package(self):
        """
        Get the tab package.
        
        Returns:
            pn.Tabs: The tab panel containing the package builder and package editor.
        """
        package_editor = DatasetPackageEditor(self.dataset, self.parameters, name='Editor')
        package_builder = DatasetPackageBuilder(self.dataset, self.parameters, self.treeview, name='Builder')
        tab_package = pn.Tabs(package_builder, package_editor, name='Package',
                                dynamic=True, styles={'font-size': '16px'})
        return tab_package

    def bt_notification(self):
        """
        Create a button to clear notifications.
        
        Returns:
            pn.widgets.Button: The button to clear notifications.
        """
        def on_rm_notification(event):
            pn.state.notifications.clear()
            #for pane in self.tabs.objects: 
            #    if not isinstance(pane, pn.Column):
            #        pane._layout.loading = False
            
        rm_notification = pn.widgets.Button(name='Clear notifications', icon="trash", button_type='default', align=('end', 'center'))
        rm_notification.on_click(on_rm_notification)
        return rm_notification
    
    def bt_gps(self):
        """
        Create a button to open the GPS site.
        
        Returns:
            pn.pane.Markdown: The button to open the GPS site.
        """
        # GPS 
        return pn.pane.Markdown("""<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-map">
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M3 7l6 -3l6 3l6 -3v13l-6 3l-6 -3l-6 3v-13" />
        <path d="M9 4v13" />
        <path d="M15 7v13" />
        </svg><a href="https://nominatim.openstreetmap.org" target="_blank">Open GPS site</a>""")

    def get_template(self):
        """
        Get the template for the application.
                
        Returns:
            pn.template.FastListTemplate: The template for the application.
        """
        logo = os.path.join(os.path.dirname(__file__), 'img', 'trees.svg')
        template = pn.template.FastListTemplate(title='pyDendron', #editable=True,
                                                logo=logo,
                                                meta_author='LIUM, Le Mans Université',
                                                meta_keywords='Dendrochronology',
                                                )
        # header
        template.header.append(self.bt_notification())
        template.header.append(self.parameters.get_widgets())
        template.header.append(self.bt_gps())
        return template
            
    def on_activate(self, event):
        """
        Event handler for tab activation.
        
        Args:
            event (object): The event object.
        """
        #print('-'*80)
        #print('*** on_activate:', event.obj.active, self.tabs.objects[event.obj.active].name)
        
        self.sidebar_widget.active_parameters(self.tabs.objects[event.obj.active].name)
        
app = None
          
def cb_auto_save():
    """
    Automatically save the dataset.
    """
    if (app is not None) and app.dataset_selector.save_auto:
        logger.info('save dataset')
        app.dataset.dump()
        
#def cb_end_session(session_context: BokehSessionContext):
#    print('session_context:', session_context)
    #logger.info('end session')
    #if (app is not None) and app.dataset_selector.save_auto:
    #    app.dataset.dump()
    #    app.parameters.save()

if __name__.startswith('bokeh_app'):
    parser = argparse.ArgumentParser(description="pydenron: A dendrochronology tool for tree-ring data analysis.")
    parser.add_argument('--www', action='store_true', help='A flag to enable www mode')
    args = parser.parse_args()
    www = args.www

    logger.info('Get paths')
    dendron_info = directory(www)
    logger.info(f'Mode: {dendron_info.www}')
    logger.info(f'username: {dendron_info.username}')
    logger.info(f'dendron_path: {dendron_info.dendron_path}')
    logger.info(f'dataset_path: {dendron_info.dataset_path}')
    logger.info(f'cfg_path: {dendron_info.cfg_path}')
    logger.info(f'tmp_path: {dendron_info.tmp_path}')
    logger.info('Configure panel extensions')
    set_extension()
    logger.info('Create application ')
    app = DendronApp(dendron_info)
    logger.info('End of initialisation')
    app.template.servable()
    # Callback: autosave 
    logger.info('add_periodic_callback ')
    pn.state.add_periodic_callback(cb_auto_save, 1000*60) 
    # pn.state.on_session_destroyed(cb_end_session)
    
