# -*- coding: utf-8 -*-
from thonnycontrib.Network import graphic
import networkx as nx

def init_DB(self):
    self.setReduc=0
    self.G = nx.DiGraph()
    graphic.init_Graph(self)
    
def clearAll(self):
    self.G.clear()
    graphic.delete(self)
    graphic.scrollregion(self)
    
def addEdge(self, startNode, endNode, startPointer):
    if isThereNode(self, startNode) and isThereNode(self, endNode):
        if self.G.has_edge(startNode, endNode):
            if startPointer in self.G.edges[(startNode, endNode)]['start']:
                return
            else:
                self.G.edges[(startNode, endNode)]['start'].add(startPointer)
        else:
            self.G.add_edges_from([(startNode, endNode,{'start':{startPointer}})], arrowstyle='->', arrowsize=10)

def removeEdge(self, edgeCreated):
    edges = self.G.edges()
    for i in edges:
        for startPointer in self.G.edges[(i[0], i[1])]['start']:
            if (i[0],i[1],startPointer) not in edgeCreated:
                if len(self.G.edges[(i[0], i[1])]['start'])<=1:
                    self.G.remove_edge(i[0], i[1])
                else:
                    self.G.edges[(i[0], i[1])]['start'].remove(startPointer)

def addNode(self, idNode, text = ""):
    if idNode == "Globals":
        self.G.add_nodes_from([('Globals', {'contenue': f'Globals', 'type': 'TypeA', 'couleur': 'deep sky blue', 'pos': (100, 200), 'taille':(0,0,0,0),'visible':False,'reduced':self.setReduc, 'reduc':(0,0), 'pointeur': []})])
    elif idNode == "Locals":
        self.G.add_nodes_from([('Locals', {'contenue': f'Locals', 'type': 'TypeB', 'couleur': 'lime green', 'pos': (100, 50), 'taille':(0,0,0,0),'visible':False,'reduced':self.setReduc, 'reduc':(0,0), 'pointeur': []})])
    else:
        self.G.add_nodes_from([(idNode,{'contenue': text, 'type': 'TypeC', 'couleur': 'turquoise', 'pos': (100, 50), 'taille':(0,0,0,0),'visible':False,'reduced':self.setReduc, 'reduc':(0,0), 'pointeur': []})])

def addNodeText(self, node, text):
    self.G.nodes[node]['contenue']+="\n"+text
    
def addNodeText2(self, node, text):
    self.G.nodes[node]['contenue']+=text

def removeNode(self, nodeCreated):
    nodes = dict(self.G.nodes())
    for i in nodes:
        if i not in nodeCreated:
            self.G.remove_node(i)
        
def nodeReset(self, node, text = ""):
    if node == "Globals":
        self.G.nodes[node]['contenue'] = f'Globals'
        self.G.nodes[node]['pointeur'] = []
    elif node == "Locals":
        self.G.nodes[node]['contenue'] = f'Locals'
        self.G.nodes[node]['pointeur'] = []
    else:
        self.G.nodes[node]['contenue'] = text
        self.G.nodes[node]['pointeur'] = []
    
def addPointeur(self,nodeParent, namePointeur, idPointeur, createdFromParent):
    if namePointeur in createdFromParent:
        self.G.nodes[nodeParent]['pointeur'].append({'name':namePointeur,'id':idPointeur,'visible':createdFromParent[namePointeur],'pSize':(0,0,0,0)})
    else:
        self.G.nodes[nodeParent]['pointeur'].append({'name':namePointeur,'id':idPointeur,'visible':False,'pSize':(0,0,0,0)})
        
def changePointeur(self, node, pB):
    self.G.nodes[node]['pointeur'][pB]['visible'] = not self.G.nodes[node]['pointeur'][pB]['visible']
    
def changeReduc(self, node):
    if self.G.nodes[node]['reduced'] == 0:
        if len(self.G.nodes[node]['pointeur'])<1:
            self.G.nodes[node]['reduced'] = 1 #The node is reduced and doesn't have pointeur
        else:
            change = False
            etat = self.G.nodes[node]['pointeur'][0]['visible']
            for i in self.G.nodes[node]['pointeur']:
                if i['visible'] != etat:
                    change=True
                    break
            if change:
                self.G.nodes[node]['reduced'] = 2 #The node is reduced whit open and close pointeurs
            elif etat==True:
                self.G.nodes[node]['reduced'] = 3 #The node is reduced whit only open pointeur
            else:
                self.G.nodes[node]['reduced'] = 4 #The node is reduced whit only close pointeur
    else:
        self.G.nodes[node]['reduced'] = 0 #The node is not reduced
    self.G.nodes[node]['taille'], self.G.nodes[node]['reduc'] = graphic.getTailleBox(self, node)
    
def changeReducPointeur(self, node):
    if self.G.nodes[node]['reduced']==2 or self.G.nodes[node]['reduced']==4 :
        self.G.nodes[node]['reduced'] = 3
        for pB in range(len(self.G.nodes[node]['pointeur'])):
            self.G.nodes[node]['pointeur'][pB]['visible']=True
    else:
        self.G.nodes[node]['reduced'] = 4
        for pB in range(len(self.G.nodes[node]['pointeur'])):
            self.G.nodes[node]['pointeur'][pB]['visible']=False

                
def draw_graph(self):
    # Clear canvas
    graphic.delete(self)
    for node in self.G.nodes():
        self.G.nodes[node]['visible']=False
    if self.G.has_node('Locals'):
        drawGraphIter(self, 'Locals')
    if self.G.has_node('Globals'):
        drawGraphIter(self, 'Globals')
    
    graphic.scrollregion(self)

def drawGraphIter(self, node):
    self.G.nodes[node]['visible']=True

    # Get bounding box of the text
    self.G.nodes[node]['taille'], self.G.nodes[node]['reduc'] = graphic.getTailleBox(self, node)

    graphic.boite(self, node)
        
    for i in range(len(self.G.nodes[node]['pointeur'])):
        for edge in self.G.edges():
            node1, node2 = edge
            if node1==node:
                if self.G.nodes[node1]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                    if self.G.nodes[node1]['pointeur'][i]['visible']:
                        if self.G.nodes[node2]['visible'] == False:
                            drawGraphIter(self, node2)
                        if self.G.nodes[node]['reduced']>0:
                            graphic.line(self, node1, node2, i)
                        else:
                            graphic.line(self, node1, node2, i)
                    break

def moveNode(self, event, node, offset):
    if node is not None:
        new_x = graphic.getX(self, event.x) - offset[0]
        new_y = graphic.getY(self, event.y) - offset[1]

        self.G.nodes[node]['pos'] = (new_x, new_y)
        draw_graph(self)
    
def showNodeEdge(self, node, pB, FromExtend = True):
    self.G.nodes[node]['pointeur'][pB]['visible'] = not self.G.nodes[node]['pointeur'][pB]['visible']
    if FromExtend:
        graphic.DrawPointeur(self, node, pB, self.G.nodes[node]['pointeur'][pB]['visible'])
    for edge in self.G.edges():
        node1, node2 = edge
        if node1==node:
            if self.G.nodes[node]['pointeur'][pB]['name'] in self.G.edges[edge]['start']:
                showIter(self, node, node2, pB)

    graphic.scrollregion(self)
    
def showIter(self, node1, node2, pB):
    if self.G.nodes[node2]['visible']:
        graphic.line(self, node1, node2, pB)
    else:
        newX = self.G.nodes[node1]['pos'][0] + self.G.nodes[node1]['taille'][2]+20
        newY = findNewY(self, node1)

        self.G.nodes[node2]['visible']=True
        
        self.G.nodes[node2]['taille'], self.G.nodes[node2]['reduc'], self.G.nodes[node2]['pos'] =  graphic.getTailleBox(self, node2, newX, newY)
        # Draw node
        graphic.boite(self, node2)
        
        #draw Edge
        graphic.line(self, node1, node2, pB)
        
        for i in range(len(self.G.nodes[node2]['pointeur'])):
            for edge in self.G.edges():
                node3, node4 = edge
                if node3==node2:
                    if self.G.nodes[node2]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                        if self.G.nodes[node2]['pointeur'][i]['visible']:
                            showIter(self, node3, node4, i)
                        break

def findNewY(self,node):
    maxY= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1]
    for i in range(len(self.G.nodes[node]['pointeur'])):
        for edge in self.G.edges():
            node2, node3 = edge
            if node2==node:
                if self.G.nodes[node]['pointeur'][i]['name'] in self.G.edges[edge]['start']:
                    if self.G.nodes[node]['pointeur'][i]['visible']:
                        if self.G.nodes[node3]['visible']:
                            if self.G.nodes[node3]['pos'][1] + self.G.nodes[node3]['taille'][3]+5>maxY:
                                maxY=self.G.nodes[node3]['pos'][1] + self.G.nodes[node3]['taille'][3]+5
                    break
    return maxY
    
    





def isReduced(self, node):
    return self.G.nodes[node]['reduced']>0

def isNodeOpen(self, node):
    return self.G.nodes[node]['reduced']==3

def isCliqueOnPointeur(self, x, y, node, pB):
    return self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][0] <= graphic.getX(self, x) <= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][2] and self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][1] <= graphic.getY(self, y) <= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][3]

def isCliqueOnReduc(self, x, y, node):
    return self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]-self.line_height/2 <= graphic.getX(self, x) <= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height/2 and self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-self.line_height/2 <= graphic.getY(self, y) <= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+self.line_height/2

def isCliqueOnReducPointeur(self, x, y, node):
    if self.G.nodes[node]['reduced']<2:
        return False
    return self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height-self.line_height/2 <= graphic.getX(self, x) <= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height+self.line_height/2 and self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-self.line_height/2 <= graphic.getY(self, y) <= self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+self.line_height/2

def isPointeurOpen(self, node, pB):
    return self.G.nodes[node]['pointeur'][pB]['visible']

def isThereNode(self, name):
    return self.G.has_node(name)

def isThereEdge(self, startNode, endNode, startPointer):
    return self.G.has_edge(startNode, endNode) and startPointer in self.G.edges[(startNode, endNode)]['start']










def getOffset(self, event, node):
    return (graphic.getX(self, event.x) - self.G.nodes[node]['pos'][0], graphic.getY(self, event.y) - self.G.nodes[node]['pos'][1])

def getClickedNode(self, event):
        # Check if clicked inside a node and return its id
        for node in reversed(list(self.G.nodes())):
            xLeft = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0]
            xRight= self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][2]
            yTop  = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1]
            yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][3] 
            bbox = self.G.nodes[node]['taille']
            if xLeft <= graphic.getX(self, event.x) <= xRight and yTop <= graphic.getY(self, event.y) <= yDown:
                return node
        return None

def getPointeurId(self, node, pB):
    return self.G.nodes[node]['pointeur'][pB]['id']

def getPoiteurName(self, node, pB):
    return self.G.nodes[node]['pointeur'][pB]['name']

def getLenPointeur(self, node):
    return len(self.G.nodes[node]['pointeur'])