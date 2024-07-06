import os
import getpass
import argparse
import pyodbc

import panel as pn
from pathlib import Path
import json
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
from collections import namedtuple

DendronInfo = namedtuple('DendronInfo', ['www', 'username', 'dendron_path', 'dataset_path', 'cfg_path', 'tmp_path'])

def directory(www=False):
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
    # Extension
    pn.extension(throttled=True)
    pn.extension(notifications=True)
    pn.extension('tabulator')
    pn.extension(loading_spinner='dots')
    #pn.extension('filedropper')
    pn.param.ParamMethod.loading_indicator = True

    pn.extension('terminal')
    pn.config.console_output = 'disable'

    pn.extension('tabulator')
    pn.extension(
        disconnect_notification="""Server Connected Closed <br /> <button class="btn btn-outline-light" onclick="location.reload();">Click To Reconnect</button> """
    )

def auto_save():
    if dataset_selector.save_auto:
        logger.info('save dataset')
        dataset.dump()
              
def create_app(dendron_info):

    def get_cfg_filename():
        return dendron_info.cfg_path / Path('pyDendron.cfg.json')

    def get_dataset(cfg_filename):
        os.makedirs(os.path.dirname(cfg_filename), exist_ok=True)
        return Dataset(username=dendron_info.username)

    def remove_notification():
        def on_rm_notification(event):
            pn.state.notifications.clear()
            for pane in panel_list:
                pane._layout.loading = False
            
        rm_notification = pn.widgets.Button(name='Clear notifications', icon="trash", button_type='default', align=('end', 'center'))
        rm_notification.on_click(on_rm_notification)
        return rm_notification
    
    def save_cfg(cfg_filename):
        def on_save_param(event):
            with open(cfg_filename, 'w') as f:
                data = {
                    'param_detrend' : param_detrend.param.serialize_parameters(),
                    'param_chronology' : param_chronology.param.serialize_parameters(),
                    'param_column' : param_column.columns.value,
                    'param_column_stat': param_column_stats.columns.value,
                    'param_package' : param_package.param.serialize_parameters(),
                }
                json.dump(data, f)
            ploter.dump_cfg()
            crossdating.dump_cfg()

        save_cfg = pn.widgets.Button(name='Save parameters', icon="settings", button_type='default', align=('end', 'center'))
        save_cfg.on_click(on_save_param)
        return save_cfg
    
    def load_cfg(cfg_filename):
        # Indice, Chronology, Columns selector
        try:
            if Path(cfg_filename).is_file():
                with open(cfg_file, 'r') as f:
                    data = json.load(f)
                    param_detrend = ParamDetrend(**ParamDetrend.param.deserialize_parameters(data['param_detrend']))
                    param_chronology = ParamChronology(**ParamChronology.param.deserialize_parameters(data['param_chronology']))
                    param_column = ParamColumns(columnList=data['param_column'])
                    param_column_stats = ParamColumnStats(columnList=data['param_column_stats'])
                    param_package = ParamPackage(**ParamPackage.param.deserialize_parameters(data['param_package']))
            else:
                    #print('no cfg')
                    param_detrend = ParamDetrend()
                    param_chronology = ParamChronology()
                    param_column = ParamColumns()
                    param_column_stats = ParamColumnStats()
                    param_package = ParamPackage()
        except Exception as inst:
            logger.warrning(f'ignore cfg files, version change.')
            param_detrend = ParamDetrend()
            param_chronology = ParamChronology()
            param_column = ParamColumns()
            param_column_stats = ParamColumnStats()
            param_package = ParamPackage()    
        finally:
            return param_detrend, param_chronology, param_column, param_column_stats, param_package
            
    def get_gps():
            # GPS 
        return pn.pane.Markdown("""<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-map">
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M3 7l6 -3l6 3l6 -3v13l-6 3l-6 -3l-6 3v-13" />
        <path d="M9 4v13" />
        <path d="M15 7v13" />
        </svg><a href="https://nominatim.openstreetmap.org" target="_blank">Open GPS site</a>""")
       
    def get_template(rm_notification, save_param, gps_code):
        logo = os.path.join(os.path.dirname(__file__), 'img', 'trees.svg')
        # Template MaterialTemplate VanillaTemplate BootstrapTemplate FastListTemplate, EditableTemplate
        template = pn.template.FastListTemplate(title='pyDendron', #editable=True,
                                                logo=logo,
                                                meta_author='LIUM, Le Mans Université',
                                                meta_keywords='Dendrochronology',
                                                )
        # Remove notification
        template.header.append(rm_notification)
        template.header.append(save_param)
        template.header.append(gps_code)
        return template

    def get_dataselector(dataset, dendron_info):
        return DatasetSelector(dataset, path=dendron_info.dataset_path, filters=['dataset*.p'], )

    def get_dataset_treeview(dataset, param_column, param_chronology, panel_list):
        treeview = DatasetTreeview(dataset, param_column, param_chronology)
        panel_list.append(treeview)

        return treeview, treeview.get_sidebar()
    
    panel_list = []
    cfg_filename = get_cfg_filename()
    dataset = get_dataset(cfg_filename)
    bt_notification = remove_notification()
    bt_save_cfg = save_cfg(cfg_filename)
    bt_gps = get_gps()
    
    template = get_template(bt_notification, bt_save_cfg, bt_gps)
    param_detrend, param_chronology, param_column, param_column_stats, param_package = load_cfg(cfg_filename)

    # Dataset selector
    dataset_selector = get_dataselector(dataset, dendron_info)
    
    # Dataset View
    dataset_package_ploter = DatasetPackage(dataset, param_column, param_package, param_detrend, param_chronology, title='Ploter')
    dataset_package = DatasetPackage(dataset, param_column, param_package, param_detrend, param_chronology, title='hyp')
    master_dataset_package = DatasetPackage(dataset, param_column, param_package, param_detrend, param_chronology, title='Master')
    panel_list.append(dataset_package_ploter)
    panel_list.append(master_dataset_package)

    # TreeView
    treeview, sidebar_treeview = get_dataset_treeview(dataset, param_column, param_chronology, panel_list)

    # Add to sidebar
    template.sidebar.append('## Datasets')
    template.sidebar.append(dataset_selector.get_sidebar())
    template.sidebar.append('## Parameters')
    sidebar_column = param_column.get_sidebar()
    template.sidebar.append(sidebar_column)
    template.sidebar.append(sidebar_treeview)
    sidebar_package = param_package.get_sidebar()
    template.sidebar.append(sidebar_package)
    sidebar_detrend = param_detrend.get_sidebar()
    template.sidebar.append(sidebar_detrend) 
    sidebar_chronology = param_chronology.get_sidebar()
    template.sidebar.append(sidebar_chronology)

    # Package Editor
    package_editor = DatasetPackageEditor(dataset, param_column, param_package, param_column_stats)
    panel_list.append(package_editor)

    # Package Builder
    package_builder = DatasetPackageBuilder(treeview)
    panel_list.append(package_builder)

    #Ploter
    ploter = PloterPanel(dataset_package_ploter, cfg_path=dendron_info.cfg_path)
    sidebar_ploter = ploter.get_sidebar(visible=False)
    template.sidebar.append(sidebar_ploter)
    panel_list.append(ploter)

    # CrossDating
    crossdating = CrossDatingPanel(dataset_package, master_dataset_package, dendron_info.cfg_path)
    sidebar_crossdating = crossdating.get_sidebar(visible=False)
    template.sidebar.append(sidebar_crossdating)
    panel_list.append(crossdating)

    #Tools
    dataset_package_tools = DatasetPackage(dataset, param_column, param_package, title='tools')
    tools = ToolsPanel(dataset, param_column, dataset_package_tools, dendron_info, filters=['dataset*.p'])
    sidebar_tools = tools.get_sidebar(visible=False)
    template.sidebar.append(sidebar_tools)
    panel_list.append(tools)

    tab_package = pn.Tabs(('Create', package_builder), 
                            ('Manage', package_editor), 
                            #('Summary', package_statistics),
                            dynamic=True, styles={'font-size': '16px'})

    #Debug / Logs
    debug = DebugPanel(dataset)
    panel_list.append(debug)

    # General tabs
    tabs = pn.Tabs(
                ('Dataset', treeview), 
                ('Package', tab_package),
                ('Ploter', ploter), 
                ('Crossdating', crossdating), 
                ('Tools', tools), 
                ('Debug/Log', debug), 
                dynamic=False, margin=0, styles={'padding' : '0px', 'font-size': '18px'})

    def sidebar_widget(event):
        sidebar_treeview.visible = False
        sidebar_ploter.visible = False
        sidebar_crossdating.visible = False
        sidebar_tools.visible = False
        sidebar_detrend.visible = True
        sidebar_chronology.visible = True
        sidebar_column.visible = True
        sidebar_package.visible = True
        if event.obj.active == 0: # Treeview
            sidebar_treeview.visible = True
            sidebar_detrend.visible = False
            sidebar_package.visible = False
        elif  event.obj.active == 1: # Package
            sidebar_detrend.visible = False
            sidebar_chronology.visible = False
        elif  event.obj.active == 2: # Plot
            sidebar_ploter.visible = True
            #dataset_package_ploter.sync_dataset(None)
            sidebar_detrend.visible = True
        elif  event.obj.active == 3: # CrossDating
            sidebar_crossdating.visible = True
            #dataset_package.sync_dataset(None)
            #master_dataset_package.sync_dataset(None)
            sidebar_detrend.visible = True
        elif  event.obj.active == 4: # Tools
            sidebar_tools.visible = True
            sidebar_detrend.visible = False
            sidebar_chronology.visible = False
        elif  event.obj.active == 5: # Debug
            sidebar_detrend.visible = False
            sidebar_chronology.visible = False
            sidebar_column.visible = False

    template.main.append(tabs)
    tabs.param.watch(sidebar_widget, ['active'], onlychanged=True)

    return template

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
    logger.info('Create application template')
    template = create_app(dendron_info)
    logger.info('End of initialisation')
    template.servable()
    
    # Callback: autosave 
    logger.info('add_periodic_callback ')
    cb = pn.state.add_periodic_callback(auto_save, 1000*60*5) 
