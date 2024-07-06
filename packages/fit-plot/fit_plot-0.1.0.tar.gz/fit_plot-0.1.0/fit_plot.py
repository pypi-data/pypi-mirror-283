import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from matplotlib.lines import Line2D
import os
import base64
import pickle

#todos:
# Format output numbers sensibly.

# keep a list of objects and names. Expect a unique name in each
# different cell this is used!

objs = []
names = []


def get_file_name(fname):
    # fname = "".join(i if i.isalnum() else "_" for i in fname)
    # create safe filename.
    fname = base64.urlsafe_b64encode(bytes(fname,'utf-8')).decode('utf-8')
    base, name = os.path.split(os.environ['JPY_SESSION_NAME'])

    if len(name)>6:
        if name[-6:] == '.ipynb':
            name = name[0:-6]
    name = '.' + name
    newname = name+'-'+fname
    newname = os.path.join(base,newname)
    return newname


class generic_fit_with_background:
    """Generic Class for creating fit objects

    Parameters:
    name: a unique name that is used as a plot title as well as for tagging the fit parameters
    xdata: x values of the data
    ydata: y values
    yerr: uncertainties in y values
    use_background: a boolean, if false we just do a linear fit, if true the function is
            np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
    """
    def __init__ (self, name, xdata, ydata, yerr, use_background):
        global objs, names
        plt.ioff()
        found_old = False
       
        # look for our object in the current module's list of objects:
        for i in range(len(objs)):
            if name == names[i]:
                self = objs[i]
                found_old = True
                self.message = "Used fit values from previous invocation"
        if found_old == False:
            # we're creating a new object:
            self.use_background = use_background
            self.message = ""
            self.filename = get_file_name(name)  
            self.xdata = xdata
            self.ydata = ydata
            self.yerr = yerr
            # self.name = name # not needed
            objs.append(self)
            names.append(name)
            self.xp=[0,0] # xp yp are end points of selected line.
            self.yp=[0,0]
            
            self.yoff = -4e9
            self.yp[0] = np.average(ydata)
            self.yp[1] = self.yp[0]
            self.xp[0] = np.min(xdata)
            self.xp[1] = np.max(xdata)
            # here we should see if there is a file that has it. If so,
            # load xp, yp and yoff from it
            self.message = "Creating new object"
            try:
                ff = open(self.filename, 'rb')
                self.xp, self.yp, self.yoff = pickle.load(ff)
                ff.close()
                self.message = "Loaded fit values from file"
            except:
                pass
            
        self.slope = (self.yp[1]-self.yp[0])/(self.xp[1]-self.xp[0])
        self.intercept = self.yp[1]-self.slope*self.xp[1]

        if self.use_background:
            self.cxp = np.linspace(np.min(xdata), np.max(xdata),100)
            self.cyp = np.zeros(100) # cxp, cyp are points for fitted curve
        else:
            self.cxp = np.array((np.min(xdata), np.max(xdata)))
            self.cyp = np.zeros(2)
                                
        
        if self.use_background:
            self.residuals = self.ydata - np.log(np.exp(self.intercept)*np.exp(self.xdata*self.slope)+np.exp(self.yoff))
            self.cyp = np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
        else:
            self.residuals = self.ydata - self.intercept-self.xdata*self.slope
            self.cyp = self.intercept+self.cxp*self.slope
        #fig = plt.figure("myfig2",figsize=(6,8))
        plt.close(name)
        self.fig = plt.figure(name)
        # make y axes about 30% bigger than default:
        self.fig.set_figheight(self.fig.get_figheight()*1.3)
        self.fig.tight_layout()
        self.fig.canvas.toolbar_visible = False
        self.fig.canvas.header_visible = False
        self.ax = self.fig.subplots(2, sharex=True, height_ratios=[1, 2])

        self.ax[0].errorbar(xdata,self.residuals,yerr, fmt='bo')
        self.ax[0].plot((np.min(xdata),np.max(xdata)),(0,0),'k-')
        self.fig.canvas.mpl_connect("button_press_event", self.onclick) # could do motion_notify_event, on_move(onmove?)
        self.line = Line2D(self.cxp,self.cyp)
        self.line2 = Line2D(self.xp,self.yp,marker='o',linestyle='',markersize=2)
        self.ax[0].title.set_text('Residuals')
        self.ax[1].title.set_text(name)
        self.ax[1].errorbar(xdata,ydata,yerr, fmt='ro')
        self.ax[1].add_line(self.line)
        self.ax[1].add_line(self.line2)
        self.out = widgets.Output()
        self.button = widgets.RadioButtons(options=["Line","Offset"]) # we look up its value later even if it doesn't appear.
        if self.use_background:
            app = widgets.AppLayout(
                header=self.fig.canvas,
                left_sidebar=self.button,            
                right_sidebar=self.out,
                pane_heights=[12, 1, 0],grid_gap="1px",align_items='center',
                pane_widths=[1,0,20])
        else:
            app = widgets.AppLayout(
                header=self.fig.canvas,
                left_sidebar=self.out,
                pane_heights=[12, 1, 0],grid_gap="1px",align_items='center',
                pane_widths=[20,0,1])
        
        display(app)
         
        with self.out:
            print(self.message)
            if self.use_background:
                if self.slope != 0:
                    # print("R0:",np.exp(self.intercept),"Decay Const:",-1/self.slope, "Background:",np.exp(self.yoff))
                    print("R0: %.*g, Decay Const: %.*g, Background: %.*g"%(6, np.exp(self.intercept), 6, -1/self.slope, 6, np.exp(self.yoff)))
            else:
                # print("slope:", self.slope,"intercept:", self.intercept)
                print("slope: %.*g, intercept: %.*g"%(6, self.slope, 6, self.intercept))
        plt.sca(self.ax[1])


    def onclick(self, event):

        # print(os.environ['JPY_SESSION_NAME']) - this gets me my current file name.
        # save state in same path but .FILENAME-PLOTNAME.fitstate
            
        # button.index tells the state of the radio buttons.
        with self.out:
            # print(event.xdata,event.ydata)
            # print(event)
            if event.inaxes == self.ax[0]:
                print("Don't click in residuals")
                return
    
        # if you click outside the axes bad things happen Should never happen now?
        if not isinstance(event.xdata, float):
            return
        if not isinstance(event.ydata, float):
            return
        
        if event.button == 1 and (self.button.index == 0 or self.use_background == False):  # LEFT
            # find limits
            # xl = ax[1].get_xlim()
            # yl = ax[1].get_ylim()
            #ax[1].set_xlim(xl)
            #ax[1].set_ylim(yl)
            # which point?       
            d0 = (event.xdata-self.xp[0])*(event.xdata-self.xp[0]) +\
                        (event.ydata-self.yp[0])*(event.ydata-self.yp[0])
            d1 = (event.xdata-self.xp[1])*(event.xdata-self.xp[1]) +\
                        (event.ydata-self.yp[1])*(event.ydata-self.yp[1])
            if (d0 < d1):
                self.xp[0] = event.xdata
                self.yp[0] = event.ydata
            else:
                self.xp[1] = event.xdata
                self.yp[1] = event.ydata
        elif event.button == 1 and self.button.index == 1:
            self.yoff = event.ydata
        self.slope = (self.yp[1]-self.yp[0])/(self.xp[1]-self.xp[0])
        self.intercept = self.yp[1]-self.slope*self.xp[1]
        if self.use_background:
            self.residuals = self.ydata - np.log(np.exp(self.intercept)*np.exp(self.xdata*self.slope)+np.exp(self.yoff))
            self.cyp = np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
        else:
            self.residuals = self.ydata - self.intercept-self.xdata*self.slope
            self.cyp = self.intercept+self.cxp*self.slope
        self.line.set_data(self.cxp, self.cyp) 
        self.line2.set_data(self.xp, self.yp)
         
        self.ax[0].cla()
        self.ax[0].errorbar(self.xdata,self.residuals,self.yerr, fmt='bo')
        self.ax[0].plot((np.min(self.xdata),np.max(self.xdata)),(0,0),'k-')
        self.ax[0].title.set_text('Residuals')
        
        self.fig.canvas.draw_idle()
        
        self.out.clear_output()
        with self.out:
            if self.use_background:
                if self.slope != 0:
                    # print("R0:",np.exp(self.intercept),"Decay Const:",-1/self.slope, "Background:",np.exp(self.yoff))
                    print("R0: %.*g, Decay Const: %.*g, Background: %.*g"%(6, np.exp(self.intercept), 6, -1/self.slope, 6, np.exp(self.yoff)))
            else:
                # print("slope:", self.slope,"intercept:", self.intercept)
                print("slope: %.*g, intercept: %.*g"%(6, self.slope, 6, self.intercept))
        # save state:
        try:
            ff = open(self.filename, 'wb') 
            pickle.dump((self.xp, self.yp, self.yoff), ff)
            ff.close()
            # with self.out:
            #    print("saving to:",self.filename)
        except:
           with self.out:
               print("Back-up file saving failed?")
        
class line(generic_fit_with_background):
    """Class for creating fit objects for straight line fit.

    Parameters:
    name: a unique name that is used as a plot title as well as for tagging the fit parameters
    xdata: x values of the data
    ydata: y values
    yerr: uncertainties in y values
    use_background: a boolean, if false we just do a linear fit, if true the function is
            np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
    """
    def __init__(self, name, xdata, ydata, yerr):
        super().__init__(name, xdata, ydata, yerr, False)

class with_background(generic_fit_with_background):
    """Class for creating fit objects for radiation experiment with background

    Parameters:
    name: a unique name that is used as a plot title as well as for tagging the fit parameters
    xdata: x values of the data
    ydata: y values
    yerr: uncertainties in y values
    use_background: a boolean, if false we just do a linear fit, if true the function is
            np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
    """
    def __init__(self, name, xdata, ydata, yerr):
        super().__init__(name, xdata, ydata, yerr, True)
    
    
