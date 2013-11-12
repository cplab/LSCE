#TODO: Fix labels initial position & hiding after scrolling
from numpy import arange, sin, pi, float, size

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import wx

class MyFrame(wx.Frame):
    
    def __init__(self, parent, id):
        self.empty=[0,7,56,63]        
        self.electrodeX=8;
        self.electrodeY=8;
        wx.Frame.__init__(self,parent, id, 'scrollable plot',
                style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
                size=(800, 400))
        self.panel = wx.Panel(self, -1)

        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvasWxAgg(self.panel, -1, self.fig)
        self.scroll_range = 400
        self.canvas.SetScrollbar(wx.HORIZONTAL, 0, 5,
                                 self.scroll_range)
        self.graphs = []                                 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, -1, wx.EXPAND)

        self.panel.SetSizer(sizer)
        self.panel.Fit()

        self.init_data()
        self.init_plot()

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
        
        #Start Time End Time Labels        
        self.dimensions = self.canvas.get_width_height() 
        self.label1x=self.dimensions[0]/4
        self.labely=(self.dimensions[1]-50)
        self.label2x=3*(self.dimensions[0]/4)        
        
        #Start Time End Time Label Positioning        
        self.startTime = wx.TextCtrl(self.panel, value="Start Time: "+
            self.i_start.__repr__(), pos=(self.label1x, self.labely), size=(140,-1))
        self.endTime = wx.TextCtrl(self.panel, value="End Time: "+
            self.i_end.__repr__(), pos=(self.label2x, self.labely), size=(140,-1))    
            
    def draw_plot(self):
        
        #Start End Labels position scaled according to window size
        self.dimensions = self.canvas.get_width_height() 
        self.label1x=self.dimensions[0]/4
        self.labely=self.dimensions[1]-50
        self.label2x=3*(self.dimensions[0]/4)
        
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
        
        #Update Start/End Labels                   
        self.startTime.value="Start Time: " + self.i_start.__repr__()
        self.endTime.value="End Time: " + self.i_end.__repr__()
        
        # Redraw:                  
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
                    fig2.canvas.set_window_title('Plot %d' %(i+1))
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
