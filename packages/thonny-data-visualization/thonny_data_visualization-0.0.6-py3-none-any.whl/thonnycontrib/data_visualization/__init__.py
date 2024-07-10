# package marker
from thonny import get_workbench
from hierarchic_view import HierarchicView
from Network_view import NetworkXView

'''Premet de charger les plug-ins au lancement de Thonny'''

def load_plugin() -> None:
    get_workbench().add_view(HierarchicView, tr("Hierarchic view"), "s")

def load_plugin() -> None:
    get_workbench().add_view(NetworkXView, tr("NetworkX view"), "s")