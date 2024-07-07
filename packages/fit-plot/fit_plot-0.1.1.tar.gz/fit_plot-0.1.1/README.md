 # fit_plot

- Fit data with a straight line chosen by clicking points on a plot.

Requires: ipympl

To use:

      import fit_plot
      %matplotlib widget
      
      fit_plots.line(unique_name, xdata, ydata, yerr)

      or

      fit_plots.with_background(unique_name, xdata, ydata, yerr)

where xdata, ydata and yerr are numpy arrays.

Click in the data portion of the figure to set a point for the fit line.
Whichever point you click closer to will move to the new position.

For with_background(), a background value can be set: choose the
background radio button, then click at the desired level of background.

Caveats:

1) if you change the unique name, the fit parameters will be lost.

2) fit parameters are stored in hidden files and won't travel if the
   notebook is renamed or moved to another directory.

3) any plots made after using one of these functions should start with
   plt.figure()

