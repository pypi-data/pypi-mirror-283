# -*- coding: utf-8 -*-
import tkinter as tk


def init_Graph(self):
    self.line_height = 0
    self.tailleTitleReduc=20
    
    self.selected_button_extReduc = tk.IntVar(value=1)
    
    self.toolbar = tk.Frame(self)
    self.toolbar.grid(row=0, column=0, sticky="ew")
    self.extendButton = tk.Button(self.toolbar, text="extended", command=self.on_extendButton_click)
    self.extendButton.pack(side=tk.LEFT, padx=5, pady=5)
    self.ReducButton = tk.Button(self.toolbar, text="reduced", command=self.on_ReducButton_click)
    self.ReducButton.pack(side=tk.LEFT, padx=5, pady=5)
    
    self.extendButton.config(relief=tk.SUNKEN if self.selected_button_extReduc.get() == 1 else tk.RAISED)
    self.ReducButton.config(relief=tk.SUNKEN if self.selected_button_extReduc.get() == 2 else tk.RAISED)
    
    self.canvas_frame = tk.Frame(self)
    self.canvas_frame.grid(row=1, column=0, sticky="nsew")
    
    self.canvas = tk.Canvas(self.canvas_frame, bg='white')
    self.canvas.grid(row=0, column=0, sticky="nsew")
    
    self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
    self.scrollbar_x.grid(row=1, column=0, sticky="ew")
    self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
    self.scrollbar_y.grid(row=0, column=1, sticky="ns")
    
    self.canvas.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

    # Configure the weight of rows and columns to make the canvas expandable
    self.grid_rowconfigure(0, weight=0)  # Row 0 for toolbar
    self.grid_rowconfigure(1, weight=1)  # Row 1 for canvas_frame
    self.grid_columnconfigure(0, weight=1)
    self.canvas_frame.grid_rowconfigure(0, weight=1)
    self.canvas_frame.grid_columnconfigure(0, weight=1)

    # Bind events
    self.canvas.bind("<ButtonPress-1>", self.on_node_click)
    self.canvas.bind("<B1-Motion>", self.on_node_drag)
        
def delete(self):
    self.canvas.delete("all")

def getTailleBox(self, node, X=None, Y=None):
    txt = None
    text_lines = self.G.nodes[node]['contenue'].split('\n')
    if self.G.nodes[node]['reduced']>0:
        if len(text_lines[0])>self.tailleTitleReduc:
            txt = text_lines[0][:self.tailleTitleReduc] + " ..."
        else:
            txt=text_lines[0]
    else:
        txt=self.G.nodes[node]['contenue']
    text_id = self.canvas.create_text(0, 0, text=txt, fill='black', anchor='center')
    bbox = self.canvas.bbox(text_id)
    self.canvas.delete(text_id) # Remove the temporary text
    if self.G.nodes[node]['reduced']>0:
        self.line_height = bbox[3] - bbox[1]
        if len(self.G.nodes[node]['pointeur'])==0:
            if X==None:
                return (bbox[0]-2, bbox[1]-2, bbox[2]+self.line_height+4, bbox[3]+2), (bbox[2]+2+self.line_height/2, bbox[1]+self.line_height/2)
            else:
                return (bbox[0]-2, bbox[1]-2, bbox[2]+self.line_height+4, bbox[3]+2), (bbox[2]+2+self.line_height/2, bbox[1]+self.line_height/2), (X+bbox[2]+2, Y+bbox[3]+2)
        else:
            if X==None:
                return (bbox[0]-2, bbox[1]-2, bbox[2]+2*self.line_height+6, bbox[3]+2), (bbox[2]+2+self.line_height/2, bbox[1]+self.line_height/2)
            else:
                return (bbox[0]-2, bbox[1]-2, bbox[2]+2*self.line_height+6, bbox[3]+2), (bbox[2]+2+self.line_height/2, bbox[1]+self.line_height/2), (X+bbox[2]+2, Y+bbox[3]+2)
    else:
        self.line_height = (bbox[3] - bbox[1]) / len(text_lines)
        if X==None:
            return (bbox[0]-2, bbox[1]-2, bbox[2]+self.line_height+4, bbox[3]+2), (bbox[2]+2+self.line_height/2, bbox[1]+self.line_height/2)
        else:
            return (bbox[0]-2, bbox[1]-2, bbox[2]+self.line_height+4, bbox[3]+2), (bbox[2]+2+self.line_height/2, bbox[1]+self.line_height/2), (X+bbox[2]+2, Y+bbox[3]+2)

    
def scrollregion(self):
    if self.G.number_of_nodes() >0:
        max_x = max(self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][2] for node in self.G.nodes())
        max_x = max(max_x+25, self.canvas.winfo_width())
        max_y = max(self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][3] for node in self.G.nodes())
        max_y = max(max_y+25, self.canvas.winfo_height())
        
        min_x = min(self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0] for node in self.G.nodes())
        min_x = min(min_x-25, 0)
        min_y = min(self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1] for node in self.G.nodes())
        min_y = min(min_y-25, 0)

        self.canvas.config(scrollregion=(min_x, min_y, max_x, max_y))
    else:
        self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))
    
    
def boite(self, node):
    txt = None
    if self.G.nodes[node]['reduced']>0:
        text_lines = self.G.nodes[node]['contenue'].split('\n')
        if len(text_lines[0])>self.tailleTitleReduc:
            txt = text_lines[0][:self.tailleTitleReduc] + " ..."
        else:
            txt=text_lines[0]
    else:
        txt=self.G.nodes[node]['contenue']
    self.canvas.create_rectangle(self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0], self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][1], self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][2], self.G.nodes[node]['pos'][1] + self.G.nodes[node]['taille'][3], fill=self.G.nodes[node]['couleur'], tags=node)
    self.canvas.create_text(self.G.nodes[node]['pos'][0], self.G.nodes[node]['pos'][1], text=txt, fill='black', anchor='center', tags=node)
    creeReducBox(self, node)
    if self.G.nodes[node]['reduced']>0:
        CreePointerReduced(self, node)
    else:
        CreeLineAndPointer(self, node)
        
def creeReducBox(self,node):
    xLTitle = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]-(self.line_height/2-2)
    xRTitle = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+(self.line_height/2-2)
    yTTitle = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-(self.line_height/2-2)
    yDTitle = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+(self.line_height/2-2)
    self.canvas.create_rectangle(xLTitle, yTTitle, xRTitle, yDTitle,fill='white', outline='black', tags=node)
    
    if self.G.nodes[node]['reduced']>0:
        self.canvas.create_text(self.G.nodes[node]['pos'][0]+self.G.nodes[node]['reduc'][0], self.G.nodes[node]['pos'][1]+self.G.nodes[node]['reduc'][1], text="+", fill='black', anchor='center', tags=node)
    else:
        self.canvas.create_text(self.G.nodes[node]['pos'][0]+self.G.nodes[node]['reduc'][0], self.G.nodes[node]['pos'][1]+self.G.nodes[node]['reduc'][1], text="-", fill='black', anchor='center', tags=node)


def CreeLineAndPointer(self,node):
    text_lines=self.G.nodes[node]['contenue'].split('\n')
    bbox = self.G.nodes[node]['taille']
    for i, line in enumerate(text_lines):
        y_line = bbox[1] + 2 + (i * self.line_height)
        if i==0:
            continue
        else:
            # Draw line and pointer square
            self.canvas.create_line(self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][0], self.G.nodes[node]['pos'][1] + y_line, self.G.nodes[node]['pos'][0] + self.G.nodes[node]['taille'][2], self.G.nodes[node]['pos'][1] + y_line, fill='black', tags=node)

            for pointeurNode in range(len(self.G.nodes[node]['pointeur'])):
                if line == self.G.nodes[node]['pointeur'][pointeurNode]['name']:
                    self.G.nodes[node]['pointeur'][pointeurNode]['pSize'] = (bbox[2]-self.line_height-2, y_line+2, bbox[2]-6, y_line+self.line_height-2)
                    DrawPointeur(self, node, pointeurNode, self.G.nodes[node]['pointeur'][pointeurNode]['visible'])
                                
def CreePointerReduced(self,node):
    if len(self.G.nodes[node]['pointeur'])<1:
        return
    xLeft = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height-(self.line_height/2)+2
    xRigh = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['reduc'][0]+self.line_height+(self.line_height/2)-2
    yTop = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]-(self.line_height/2)+2
    yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['reduc'][1]+(self.line_height/2)-2
    if self.G.nodes[node]['reduced']==2:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='orange', outline='black', tags=node)
    elif self.G.nodes[node]['reduced']==3:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='green', outline='black', tags=node)
    else:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='red', outline='black', tags=node)
                            
def line(self,node1,node2,pB):
    start_pos = None
    if self.G.nodes[node1]['reduced']==0:
        start_pos = (self.G.nodes[node1]['pos'][0] + (self.G.nodes[node1]['pointeur'][pB]['pSize'][0] + self.G.nodes[node1]['pointeur'][pB]['pSize'][2])/2, self.G.nodes[node1]['pos'][1] + (self.G.nodes[node1]['pointeur'][pB]['pSize'][1]+self.G.nodes[node1]['pointeur'][pB]['pSize'][3])/2) 
    else:
        start_pos = (self.G.nodes[node1]['pos'][0] + self.G.nodes[node1]['reduc'][0] + self.line_height, self.G.nodes[node1]['pos'][1])                 
    end_pos = (self.G.nodes[node2]['pos'][0] + self.G.nodes[node2]['taille'][0], self.G.nodes[node2]['pos'][1])
    self.canvas.create_line(start_pos, end_pos, arrow=tk.LAST, arrowshape=(10, 12, 5), width=2)


def DrawPointeur(self, node, pB, open):
    xLeft = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][0]
    xRigh = self.G.nodes[node]['pos'][0] + self.G.nodes[node]['pointeur'][pB]['pSize'][2]
    yTop  = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][1]
    yDown = self.G.nodes[node]['pos'][1] + self.G.nodes[node]['pointeur'][pB]['pSize'][3]
    if open == True:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='green', outline='black', tags=node)
    else:
        self.canvas.create_oval(xLeft, yTop, xRigh, yDown,fill='red', outline='black', tags=node)
        
def getX(self, x):
    return self.canvas.canvasx(x)

def getY(self, y):
    return self.canvas.canvasy(y)