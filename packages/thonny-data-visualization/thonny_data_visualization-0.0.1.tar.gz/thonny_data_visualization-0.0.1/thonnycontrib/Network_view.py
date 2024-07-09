# -*- coding: utf-8 -*-
from logging import getLogger
from thonny import get_workbench, ui_utils, get_runner
from thonny.common import InlineCommand, ValueInfo
from thonny.languages import tr
import tkinter as tk
import builtins
import time as t
from thonnycontrib.Network import DB
from thonnycontrib.representation_format import repr_format
import thonnycontrib.sender as sender

builtin_types = [str(getattr(builtins, d)) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
builtin_types.append("<class 'function'>")
builtin_types.append("<class 'method'>")
builtin_types.append("<class 'NoneType'>")
builtin_types.append("<class 'module'>")
builtin_types.append("<class 'builtin_function_or_method'>")
builtin_data_struct = ["<class 'dict'>", "<class 'list'>", "<class 'set'>", "<class 'tuple'>"]

logger = getLogger(__name__)

class NetworkXView(tk.Frame, ui_utils.TreeFrame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.rect_padding = 5

        self.iter = 0

        self.lazy_on = False

        self.name = 'GV'

        self.parent_id = None
        self.object_id = None
        self.object_name = None
        self.var_to_request = {}
        self.extendeRequest = None
        self.extendeRequestReduc=None

        self.tree_db = {}
        self.type_db = {}
        self.repr_db = {}
        self.nodeCreated={}
        self.edgeCreated=set()

        self._last_progress_message = None
        
        DB.init_DB(self)
        
        get_workbench().bind("ToplevelResponse", self._handle_toplevel_response, True)
        get_workbench().bind("DebuggerResponse", self._debugger_response, True)
        get_workbench().bind("get_object_info_response", self._handle_object_info_event, True)
        get_workbench().bind("BackendRestart", self._on_backend_restart, True)


    def on_extendButton_click(self):
        # Define the action for button 1
        self.setReduc=0
        for i in self.G.nodes:
            self.G.nodes[i]['reduced']=0
        DB.draw_graph(self)
        self.selected_button_extReduc.set(1)
        self.update_button_states()

    def on_ReducButton_click(self):
        # Define the action for button 2
        self.setReduc=4
        for node in self.G.nodes:
            if len(self.G.nodes[node]['pointeur'])<1:
                self.G.nodes[node]['reduced'] = 1
            else:
                change = False
                etat = self.G.nodes[node]['pointeur'][0]['visible']
                for i in self.G.nodes[node]['pointeur']:
                    if i['visible'] != etat:
                        change=True
                        break
                if change:
                    self.G.nodes[node]['reduced'] = 2
                elif etat==True:
                    self.G.nodes[node]['reduced'] = 3
                else:
                    self.G.nodes[node]['reduced'] = 4
        DB.draw_graph(self)
        self.selected_button_extReduc.set(2)
        self.update_button_states()
        
    def update_button_states(self):
        # Update the relief of buttons based on selected_button_extReduc
        buttonextend_relief = tk.SUNKEN if self.selected_button_extReduc.get() == 1 else tk.RAISED
        buttonreduc_relief = tk.SUNKEN if self.selected_button_extReduc.get() == 2 else tk.RAISED
        self.extendButton.config(relief=buttonextend_relief)
        self.ReducButton.config(relief=buttonreduc_relief)

    def _on_backend_restart(self, event=None):
        DB.clearAll(self)
        self.parent_id = None
        self.object_id = None
        self.object_name = None
        self.var_to_request = {}
        self.extendeRequest = None
        self.extendeRequestReduc=None
        self.tree_db = {}
        self.type_db = {}
        self.repr_db = {}
        self.nodeCreated={}
        self.edgeCreated=set()
        self._last_progress_message = None

    
    def on_node_click(self, event):
        # Check if clicked on a node
        node = DB.getClickedNode(self, event)
        if node is not None:
            # Store the clicked node and its offset
            self.selected_node = node
            self.offset = DB.getOffset(self, event, node)
            if DB.isCliqueOnReduc(self, event.x, event.y, node):
                DB.changeReduc(self, node)
                DB.draw_graph(self)
            elif DB.isCliqueOnReducPointeur(self, event.x, event.y, node):
                self.extendLazyReduc(node)
            elif not DB.isReduced(self,node):
                for pB in range(DB.getLenPointeur(self, node)):
                    if DB.isCliqueOnPointeur(self, event.x, event.y, node, pB):
                        if DB.isPointeurOpen(self, node, pB):
                            DB.changePointeur(self, node, pB)
                            DB.draw_graph(self)
                        else:
                            #DB.changePointeur(self, node, pB)
                            self.extendLazy(self.tree_db[DB.getPointeurId(self, node, pB)][0], DB.getPoiteurName(self, node, pB),self.tree_db[DB.getPointeurId(self, node, pB)][1], node, pB)
            
    def on_node_drag(self, event):
        # Move the selected node to the mouse position
        DB.moveNode(self, event, self.selected_node, self.offset)

    def _handle_toplevel_response(self, event):
        if "globals" in event and event["globals"]:
            self.update(event["globals"])
        
    def _debugger_response(self, event):
        self._last_progress_message = event
        frame_info=None
        frameNotFind=True
        for ff in self._last_progress_message.stack:
            if ff.id == event.stack[-1].id:
                frame_info = ff
                frameNotFind = False
                break
        if frameNotFind:
            raise ValueError("Could not find frame %d" % event.stack[-1].id)
        self.update(frame_info.globals, frame_info.locals)
    
    def update(self, globals_, locals_ = None):
        
        self.nodeCreated={}
        self.edgeCreated=set()
        
        self.parent_id = None
        self.object_id = None
        self.object_name = None
        self.extendeRequest = None
        self.extendeRequestReduc=None
        self.tree_db = {}
        self.type_db = {}
        self.repr_db = {}
        l = []

        globalst = None
        localst = None
        if (globals_):
            globalst = globals_.copy()
        if (locals_):
            localst = locals_.copy()
        self.var_to_request["globals"] = globalst
        self.var_to_request["locals"] = localst
        self.var_to_request["children"] = {}

        self.send_request()
    
    def send_request(self):
        if not self.var_to_request["globals"] and not self.var_to_request["locals"] and not self.var_to_request["children"]:
            self.var_to_request["globals"] = {}
            self.var_to_request["locals"] = {}
            self.var_to_request["children"] = {}
            self.object_id = None
            self.parent_id = None
            if self.extendeRequest:
                DB.showNodeEdge(self, self.extendeRequest[0], self.extendeRequest[1])
                self.extendeRequest=None
                self.extendeRequestReduc=None
            elif self.extendeRequestReduc:
                parentID=self.extendeRequestReduc[0]
                pB=self.extendeRequestReduc[1]
                self.extendeRequest=None
                self.extendeRequestReduc=None
                DB.showNodeEdge(self, parentID, pB, False)
                self.extendLazyReduc2(parentID, pB+1)
            else:
                self.extendeRequest = None
                self.extendeRequestReduc=None
                self.clear_some()
                DB.draw_graph(self)

        else:
            sender.send(self)
    
    def _handle_object_info_event(self, msg):
        
        if msg.info["id"] == self.object_id:
            if "error" in msg.info.keys() or (hasattr(msg, "not_found") and msg.not_found):
                self.object_id = None
                self.object_name = None
                self.extendeRequest = None
                self.extendeRequestReduc=None
                DB.draw_graph(self)
                
            else:
                object_infos = msg.info
                object_infos["name"] = self.object_name
                
                if (object_infos["type"] != "<class 'method'>"):
                    self.format(object_infos)

                self.send_request()
        
        elif self.object_id != None and msg.get("command_id") != 'GV ' + str(self.iter):
            sender.fast_send(self)
            
    def reset_data(self):
        print("Data has been reset")
    
    def reset(self, node):
        self.nodeCreated[node]={}
        for pB in range(DB.getLenPointeur(self, node)):
            self.nodeCreated[node][DB.getPoiteurName(self, node, pB)] = DB.isPointeurOpen(self, node, pB)
        DB.nodeReset(self, node)
    
    def format(self, object_infos):
        if ((self.parent_id == "Globals" and not DB.isThereNode(self, "Globals")) or (self.parent_id == "Locals" and not DB.isThereNode(self, "Locals"))):
            DB.addNode(self, self.parent_id)
            self.nodeCreated[self.parent_id]={}
        elif ((self.parent_id == "Globals" and DB.isThereNode(self, "Globals") and  'Globals' not in self.nodeCreated) or (self.parent_id == "Locals" and DB.isThereNode(self, "Locals") and  'Locals' not in self.nodeCreated)):
            self.reset(self.parent_id)
        
        name = str(object_infos["name"])
        DB.addNodeText(self, self.parent_id, name)

        tp = object_infos["type"]
        
        s, at_bool = repr_format(self, object_infos['repr'])
            
        if (tp not in builtin_types or tp in builtin_data_struct):
            
            if (object_infos["id"] not in self.tree_db.keys()):

                if at_bool:
                    if (tp not in self.type_db.keys()):
                        self.type_db[tp] = 0
                    self.type_db[tp] += 1
                    s += " n°" + str(self.type_db[tp])
                    
                elif (tp in builtin_data_struct):
                    s = tp[8:-2] + " : " + s
                    
                
                self.tree_db[object_infos["id"]] = (s, object_infos)
                self.repr_db[object_infos["repr"]] = s
                DB.addPointeur(self, self.parent_id, name, object_infos['id'], self.nodeCreated[self.parent_id])
                self.extend(s, name, object_infos)
                
            else:
                DB.addPointeur(self, self.parent_id, name, object_infos['id'], self.nodeCreated[self.parent_id])
                DB.addEdge(self, self.parent_id, object_infos["id"],name)
                if (self.parent_id, object_infos["id"],name) not in self.edgeCreated:
                    self.edgeCreated.add((self.parent_id, object_infos["id"],name))
                    
                
        else :
            DB.addNodeText2(self, self.parent_id, " : " + s)

    def extend(self, s, name, object_infos):
        node_id = object_infos["id"]
        if DB.isThereNode(self, node_id):
            self.reset(self.parent_id)
            self.extendSuite(object_infos, self.parent_id, name)
                        
    def extendLazy(self, s, name, object_infos, parentID,pB):
        node_id = object_infos["id"]
        if not DB.isThereNode(self, node_id):
            DB.addNode(self, node_id, s)
            self.nodeCreated[node_id]={}
            self.extendSuite(object_infos, parentID, name)
            self.extendeRequest=(parentID, pB)
            self.send_request()
        else:
            if DB.isThereEdge(self, parentID, node_id, name):
                DB.showNodeEdge(self, parentID, pB)
            else:
                DB.addEdge(self, parentID, node_id,name)
                if (parentID, node_id,name) not in self.edgeCreated:
                    self.edgeCreated.add((parentID, node_id,name))
                DB.showNodeEdge(self, parentID, pB)
                
    def extendLazyReduc(self, parentID):
        if DB.isNodeOpen(self, parentID):
            DB.changeReducPointeur(self, parentID)
            DB.draw_graph(self)
        else:
            self.extendLazyReduc2(parentID, 0)
    
    def extendLazyReduc2(self, parentID, n):
        l=DB.getLenPointeur(self, parentID)
        if n<l:
            for pB in range(n, l):
                if not DB.isPointeurOpen(self, parentID, pB):
                    object_infos=self.tree_db[DB.getPointeurId(self, parentID, pB)][1]
                    node_id = object_infos["id"]
                    name=DB.getPoiteurName(self, parentID, pB)
                    if not DB.isThereNode(self, node_id):
                        s=self.tree_db[DB.getPointeurId(self, parentID, pB)][0]
                        DB.addNode(self, node_id, s)
                        self.nodeCreated[node_id]={}
                        self.extendSuite(object_infos, parentID, name)
                        self.extendeRequestReduc=(parentID, pB)
                        self.send_request()
                        return
                    elif not DB.isThereEdge(self,parentID, node_id, pB):
                        DB.addEdge(self, parentID, node_id,name)
        DB.changeReducPointeur(self, parentID)
        DB.draw_graph(self)
        
    def extendSuite(self,object_infos, parentID, name):
        node_id = object_infos["id"]
        DB.addEdge(self, parentID, node_id,name)
        if (parentID, node_id,name) not in self.edgeCreated:
            self.edgeCreated.add((parentID, node_id,name))
        
        tp = object_infos['type']
        if (tp not in builtin_types):
            attributes = object_infos['attributes']
            if (len(attributes) != 0):
                self.var_to_request["children"][node_id] = {}
                i = 0
                for attr in attributes:
                    if ('<built-in method' not in attributes[attr].repr):
                        self.var_to_request["children"][node_id][attr] = ValueInfo(attributes[attr].id, attributes[attr].repr)
                    if(i >= 100):
                        break
                    i+=1
        
        elif (tp in builtin_data_struct):
            if (tp == "<class 'dict'>"):
                entries = object_infos['entries']
                if (len(entries) != 0):
                    self.var_to_request["children"][node_id] = {}
                    for i in range(len(entries)):
                        entr = entries[i]
                        self.var_to_request["children"][node_id][str(i) + ".key"] = ValueInfo(entr[0].id, entr[0].repr)
                        self.var_to_request["children"][node_id][str(i) + ".values"] = ValueInfo(entr[1].id, entr[1].repr)
                        if(i >= 100):
                            break
            else:
                elements = object_infos['elements']
                if (len(elements) != 0):
                    self.var_to_request["children"][node_id] = {}
                    for i in range(len(elements)):
                        elem = elements[i]
                        self.var_to_request["children"][node_id][i] = ValueInfo(elem.id, elem.repr)
                        if(i >= 100):
                            break

    def clear_some(self):
        DB.removeNode(self, self.nodeCreated)
        self.nodeCreated={}
        DB.removeEdge(self, self.edgeCreated)
        self.edgeCreated=set()

def load_plugin() -> None:
    get_workbench().add_view(NetworkXView, tr("NetworkX view"), "s")
