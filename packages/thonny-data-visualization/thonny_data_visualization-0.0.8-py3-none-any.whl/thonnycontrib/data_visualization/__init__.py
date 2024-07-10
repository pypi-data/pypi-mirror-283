# package marker
from thonny import get_workbench
from thonny.languages import tr
from thonnycontrib.data_visualization.hierarchic_view import HierarchicView
from thonnycontrib.data_visualization.Network_view import NetworkXView

'''Premet de charger les plug-ins au lancement de Thonny'''

def load_plugin() -> None:
    get_workbench().add_view(HierarchicView, tr("Hierarchic view"), "s")
    get_workbench().add_view(NetworkXView, tr("NetworkX view"), "s")