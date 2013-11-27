#TODO: Fix labels updating slowly, integrate scrollbar in big plot, test w real data
from numpy import arange, sin, pi, float, size

import matplotlib
#matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import wx

class MyFrame(wx.Frame):
    
    def __init__(self, parent, id):
        
        #Specify electrode numbers and electrodes that are missed
        #In this specific implementation we have    
        #8x8 set of electrodes, with corners missing (0,7,56,63)
        self.empty=[0,7,56,63]        
        self.electrodeX=8;
        self.electrodeY=8;

        #Adjust Display Size            
        tmp = wx.DisplaySize()
        tmp2=(tmp[0],tmp[1]-100)
        wx.Frame.__init__(self,parent, id, 'LSCE - Overall Plot',(0,0),
                tmp2)
        self.panel = wx.Panel(self, -1)
        self.dimensions = self.GetSize()        
        self.xoffset = 50
        self.yoffset = 100 
        self.labelwidth = 140
        
        #canvas, graphs, scrollbar
        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvasWxAgg(self.panel, -1, self.fig)
        self.scroll_range = 400
        self.canvas.SetScrollbar(wx.HORIZONTAL, 0, 5,
                                 self.scroll_range)
        self.graphs = []                                 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, -1, wx.EXPAND)
        #print "beforefit"+self.GetSize().__repr__()
        self.panel.SetSizer(sizer)
        self.panel.Fit()
     
        self.init_data()
        self.init_plot()
        self.Layout()
        
        self.canvas.Bind(wx.EVT_SCROLLWIN, self.OnScrollEvt)
        self.canvas.mpl_connect('button_press_event',self.onclick)   

    def init_data(self):

        # Generate some data to plot:
        self.dt = 0.01
        self.t = arange(0,5,self.dt)
        self.x = sin(2*pi*self.t)

        # Extents of data sequence: 
        self.i_min = 0
        self.i_max = len(self.t)
        
        # Size of plot window:       
        self.i_window = 100

        # Indices of data interval to be plotted:
        self.i_start = 0
        self.i_end = self.i_start + self.i_window

    def init_plot(self):
        
        #Start Time End Time Label Positioning
        self.label1x=self.xoffset
        self.labely=self.dimensions[1]-self.yoffset
        self.label2x=self.dimensions[0]-self.xoffset-self.labelwidth       
        
        #Start Time End Time Labels        
        self.startTime = wx.TextCtrl(self.panel, value="Start Time: "+
            self.i_start.__repr__(), pos=(self.label1x, self.labely), size=(self.labelwidth,-1))
        self.endTime = wx.TextCtrl(self.panel, value="End Time: "+
            self.i_end.__repr__(), pos=(self.label2x, self.labely), size=(self.labelwidth,-1))        
        
        #creating each sub plot
        self.axes=[]
        self.graphs = []
        for j in range (64):
            if j not in self.empty:
                self.axes.append(self.fig.add_subplot(self.electrodeX,self.electrodeY,j+1))
          
                self.axes[j].yaxis.set_major_locator(matplotlib.ticker.NullLocator())
                self.axes[j].xaxis.set_major_locator(matplotlib.ticker.NullLocator())
                
                self.graphs.append(
                      self.axes[j].plot(self.t[self.i_start:self.i_end],
                                 self.x[self.i_start:self.i_end])[0])
            else:
                self.axes.append(0)
                self.graphs.append(0)
        self.canvas.draw()        
            
            
    def draw_plot(self):
        
        # Adjust plot limits:
        for i in range (64):
            if i not in self.empty:
            # Update data in plot:
                self.graphs[i].set_xdata(self.t[self.i_start:self.i_end])
                self.graphs[i].set_ydata(self.x[self.i_start:self.i_end])
                self.axes[i].set_xlim((min(self.t[self.i_start:self.i_end]),
                           max(self.t[self.i_start:self.i_end])))
                self.axes[i].set_ylim((min(self.x[self.i_start:self.i_end]),
                            max(self.x[self.i_start:self.i_end])))
        
        # Redraw:     
                  
        self.startTime.ChangeValue("Start Time: " + self.i_start.__repr__())
        self.endTime.ChangeValue("End Time: " + self.i_end.__repr__())
        self.canvas.draw()
   
    def OnScrollEvt(self, event):
                
        self.canvas.SetScrollPos(wx.HORIZONTAL, event.GetPosition(), True)
        
        # Update the indices of the plot:
        self.i_start = self.i_min + event.GetPosition()
        self.i_end = self.i_min + self.i_window + event.GetPosition()
        self.draw_plot()
    
    def onclick(self, event):
        #print "clicked"
        i=0
        while i < 64:
            if i not in self.empty:
                if event.inaxes == self.axes[i]:
                    fig2 = plt.figure()
                    ax_single = fig2.add_subplot(111)
                    #input in data ....
                    
                    #Plot Naming According to Electrode Position
                    if (i+1)%self.electrodeX != 0 :
                        rowno = ((i+1)/self.electrodeX)+1
                    else:
                        rowno=(i+1)/self.electrodeX
                    if (i+1)%self.electrodeX ==0 :
                        colno=self.electrodeX
                    else:
                        colno= (i+1)%self.electrodeX
                    fig2.canvas.set_window_title('Plot '+ rowno.__repr__() + 
                        " x "+colno.__repr__())
                    fig2.show()
                    
                    break                
            i+=1

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None,id=-1)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
