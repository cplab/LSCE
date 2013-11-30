#TODO: integrate scrollbar in big plot, implement real data, customize graph window
from numpy import arange, sin, pi, float, size
import datetime
import math
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import wx

class MyFrame(wx.Frame):
    
    """
    Creates a GUI class that displays data for an 8x8 set of electrodes
    with the corners missing. 
    Main View: Scrollable data for each electrode is displayed according
    to the placement of electrodes in the 8x8 arrangement
    Zoom in View: Scrollable data for a single electrode is displayed
    with MatPlotLib options such as saving data 
    """
    def __init__(self, parent, id, data, time, samprate):
        
        #Specify electrode numbers and electrodes that are missed
        #In this specific implementation we have    
        #8x8 set of electrodes, with corners missing (0,7,56,63)
        self.empty=[0,7,56,63]        
        self.electrodeX=8
        self.electrodeY=8
        
        """
        if len(data)!=(self.electrodeX*self.electrodeY-len(self.empty)):
            print "You do not have enough data for electrodes."
            print "There should be data for 64 electrodes"
            raise ValueError
        """    
        #Data Variables        
        self.data=data
        self.time=time
        self.samprate=samprate
        
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
        self.scroll_range = len(data[0])-time*samprate + 1
        print self.scroll_range
        self.canvas.SetScrollbar(wx.HORIZONTAL, 0, max(1,self.scroll_range/20),
                                 self.scroll_range)
        self.graphs = []                                 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, -1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.panel.Fit()
        self.lastupdate=datetime.datetime.utcnow()
        self.init_data()
        self.init_plot()
        self.Layout()
        
        #Bind Events, Scrollbar & Button Press
        self.canvas.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.OnScrollEvt)
        self.canvas.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.OnScrollStop)
        self.canvas.mpl_connect('button_press_event',self.onclick)   

    """
    Parses data to be fed into visualization. 
    """
    def init_data(self):

        # Generate x axis limits and data intervals:
        self.dt = 1.0/self.samprate
        self.t = arange(0,float(len(self.data[0]))/self.samprate,self.dt)
        print "There are "+self.t.__repr__()+" time series, and "+self.data[0].__repr__()+" data entries."
        # Extents of data sequence: 
        self.i_min = 0
        self.i_max = len(self.t)
        
        # Size of plot window:       
        self.i_window = self.time*self.samprate
        print "Window size is "+self.i_window.__repr__()+" entries."
        # Indices of data interval to be plotted:
        self.i_start = 0
        self.i_end = self.i_start + self.i_window

    """
    Creates 8x8 Data Plots
    """
    def init_plot(self):
        
        #Start Time End Time Label Positioning
        self.label1x=self.xoffset
        self.labely=self.dimensions[1]-self.yoffset
        self.label2x=self.dimensions[0]-self.xoffset-self.labelwidth       
        
        #Start Time End Time Labels        
        self.startTime = wx.TextCtrl(self.panel, value="Start Time: "+
            (float(self.i_start)/self.samprate).__repr__(), pos=(self.label1x, self.labely), size=(self.labelwidth,-1))
        self.endTime = wx.TextCtrl(self.panel, value="End Time: "+
            (float(self.i_end)/self.samprate).__repr__(), pos=(self.label2x, self.labely), size=(self.labelwidth,-1))        
        
        #creating each sub plot
        self.axes=[]
        self.graphs = []
        arrayoffset=0
        for j in range (self.electrodeX * self.electrodeY):
            if j not in self.empty:
                self.axes.append(self.fig.add_subplot(self.electrodeX,self.electrodeY,j+1))
          
                self.axes[j].yaxis.set_major_locator(matplotlib.ticker.NullLocator())
                self.axes[j].xaxis.set_major_locator(matplotlib.ticker.NullLocator())
                
                self.dataCurrent = self.data[0]
                self.graphs.append(
                      self.axes[j].plot(self.t[self.i_start:self.i_end],
                                 self.data[0][self.i_start:self.i_end])[0])
            else:
                self.axes.append(0)
                self.graphs.append(0)
                arrayoffset=arrayoffset+1
        self.canvas.draw()        
            
    """
    Updates the section of data displayed according to scrolling event
    """
    def draw_plot(self):
        
        # Adjust plot limits:
        for i in range (self.electrodeX*self.electrodeY):
            if i not in self.empty:
            # Update data in plot:
                self.graphs[i].set_xdata(self.t[self.i_start:self.i_end])
                self.graphs[i].set_ydata(self.data[0][self.i_start:self.i_end])
                self.axes[i].set_xlim((min(self.t[self.i_start:self.i_end]),
                           max(self.t[self.i_start:self.i_end])))
                self.axes[i].set_ylim((min(self.data[0][self.i_start:self.i_end]),
                            max(self.data[0][self.i_start:self.i_end])))
        
        # Redraw:
        self.canvas.draw()
        self.startTime.Refresh()
        self.endTime.Refresh()
        
    """
    Handles Graph Scrolling
    """
    def OnScrollEvt(self, event):
        
        if((datetime.datetime.utcnow()-self.lastupdate).microseconds>250000):
            self.draw_plot()
            self.lastupdate = datetime.datetime.utcnow()
        
        # Update the indices of the plot:
        self.i_start = self.i_min + event.GetPosition()
        self.i_end = self.i_min + self.i_window + event.GetPosition()        
        
        #Update Scrollbar & labels
        self.canvas.SetScrollPos(wx.HORIZONTAL, event.GetPosition(), True)
        self.startTime.ChangeValue("Start Time: " + (float(self.i_start)/self.samprate).__repr__())
        self.endTime.ChangeValue("End Time: " + (float(self.i_end)/self.samprate).__repr__())
        
       
    
    """
    Handles Graph Scrolling
    """
    def OnScrollStop(self, event):
        self.draw_plot()
    
    """
    When a graph is clicked on, handles the creation of a zoomed in 
    view of that graph (Zoom in View) 
    """
    def onclick(self, event):
        
        #loop through all plots to check which one was clicked
        i=0
        while i < self.electrodeX*self.electrodeY:
            if i not in self.empty:
                if event.inaxes == self.axes[i]:
                    fig2 = plt.figure()
                    ax_single = fig2.add_subplot(111)
                    
                    #input in data and graph section/ limits
                    ax_single.plot(self.t, self.data[0], 'yo-')
                    ax_single.set_xlim([0,self.time])
                    ax_single.set_autoscale_on(False)
                    
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
       return True
       
"""
Function which produces a visualization of 8x8 electrode data with a main
view (graph of each electrode's data, arranged together according to the 
electrode positions) and zoom in view (graph of single electrode data). 
Data = 2D Array of y values to be plotted
Time (in seconds) = the amount of time the graph should span in each window
                    should be passed in as an integer
Samprate = sampling rate, ie how many data samples per second
          should be passed in as an integer
"""
def analyze8x8data(data, time=1, samprate=2):
   
   if not (type(time) is int):
       print "Your 'time' variable is incorrect. Time should be an integer"
       raise ValueError 
   if not(type(samprate) is int):
       print "Your 'samprate' variable is incorrect. Samprate should be an integer"
       raise ValueError
       
   app = MyApp()
   frame = MyFrame(parent=None,id=-1, data=data, time=time, samprate=samprate)
   frame.Show()
   app.SetTopWindow(frame)
   app.MainLoop()

"""
Function which produces visualization of single electrode data. 
Data = Array of y values to be plotted
Time (in seconds) = the amount of time the graph should span in each window
                    should be passed in as an integer
Samprate = sampling rate, ie how many data samples per second
        should be passed in as an integer
"""   
def analyzesingle(data, time, samprate):
    
    if not (type(time) is int):
       print "Your 'time' variable is incorrect. Time should be an integer"
       raise ValueError
    if not(type(samprate) is int):
       print "Your 'samprate' variable is incorrect. Samprate should be an integer"
       raise ValueError
    
    dt = 1.0/samprate
    t = arange(0,float(len(data))/samprate,dt)        
    fig2 = plt.figure()
    ax_single = fig2.add_subplot(111)
    ax_single.plot(t, data, 'yo-')
    ax_single.set_xlim([0,time])
    ax_single.set_autoscale_on(False)

if __name__ == '__main__':
   analyze8x8data([[1,2,1,4],[2,3,4,5]])
   analyzesingle([1,2,1,4],1,2)
