#!/usr/bin/env python
# Copyright: This document has been placed in the public domain.

"""
Taylor diagram (Taylor, 2001) test implementation.

http://www-pcmdi.llnl.gov/about/staff/Taylor/CV/Taylor_diagram_primer.htm
"""

__version__ = "Time-stamp: <2012-02-17 20:59:35 ycopin>"
__author__ = "Yannick Copin <yannick.copin@laposte.net>"

import numpy as NP
import matplotlib.pyplot as PLT

class TaylorDiagram(object):
    """Taylor diagram: plot model standard deviation and correlation
    to reference (data) sample in a single-quadrant polar plot, with
    r=stddev and theta=arccos(correlation).
    """

    def __init__(self, refstd, fig=None, rect=111, label='_'):
        """Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using mpl_toolkits.axisartist.floating_axes. refstd is
        the reference standard deviation to be compared to.
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist as axisartist
        import mpl_toolkits.axisartist.grid_finder as GF

        self.refstd = refstd            # Reference standard deviation

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = NP.concatenate((NP.arange(10)/10.,[0.,0.99]))
#       rlocs = NP.concatenate((NP.arange(10)/10.,[0.95,0.99]))
        tlocs = NP.arccos(rlocs)        # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)    # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))

        # Standard deviation axis extent
        self.smin = 0.6
        self.smax = 1.4*self.refstd
        #self.smin = 0
        #self.smax = 1.6*self.refstd

        gl2=GF.MaxNLocator(10) #[0, 0.2,0.4,0.6, 0.8,1.0,1.2,1.4]
        ghelper = FA.GridHelperCurveLinear(tr,
#                                          extremes=(0,NP.pi/2.0, # 1st quadrant
                                           extremes=(0,NP.pi/2.0, # 1st quadrant
                                                     self.smin,self.smax),
                                           grid_locator1=gl1,
                                           grid_locator2=gl2,
                                           tick_formatter1=tf1,
                                           tick_formatter2=None,
                                           )
        ghelper.grid_finder.grid_locator2._nbins = 4

        if fig is None:
            fig = PLT.figure()

        ax = FA.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)
#        ax.set_xticks([1,2,3])
        """
        #ax.set_xticks(major_ticks)
        #ax.set_xticklabels(major_ticks)
        """

        # Adjust axes
        PLT.setp(ax.spines.values(), visible=False)
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")
        ax.axis["top"].label.set_fontsize(9)
        ax.axis[:].major_ticklabels.set_fontsize(12)

        ax.axis["left"].set_axis_direction("right") # "X axis"
        ax.axis["left"].toggle(ticklabels=True, label=True)
        ax.axis["left"].toggle(ticklabels=False, label=False)
        ticks_font=10
        ax.axis["left"].label.set_text("Normalized std.")
        ax.axis["left"].label.set_fontsize(9)
        #ax.axis["left"].major_ticklabels.set_major_locator(ticker.FixedLocator((pos_list)))

        ax.axis["right"].set_axis_direction("top")   # "Y axis"
        ax.axis["right"].toggle(ticklabels=True, label=True)
#        ax.axis["right"].major_ticks.set_ticksize(ticks_font) # "Y axis"
        ax.axis["right"].major_ticklabels.set_axis_direction("left")
        ax.axis["right"].label.set_fontsize(9)

        ax.axis["bottom"].set_visible(False)         # Useless
        
        # Contours along standard deviations
        ax.grid(False)

        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates

        # Add reference point and stddev contour
        print "Reference std:", self.refstd
        l, = self.ax.plot([0], self.refstd, color='lime',marker='*',
                          ls='', ms=10, label=label)
        PLT.setp(l,  'linewidth', 0.1)
        #PLT.setp(l,  'linewidth', 0.01)
        t = NP.linspace(0, NP.pi/2.0)
        r = NP.zeros_like(t) + self.refstd
        lines=self.ax.plot(t,r, color='darkgray',ls='--', label='_')
        r = NP.zeros_like(t) + self.smin
        lines=self.ax.plot(t,r, color='darkgray', label='_')
        PLT.setp(lines,  'linewidth', 0.01)
        #PLT.setp(lines,  'linewidth', 0.01)

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]

    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """Add sample (stddev,corrcoeff) to the Taylor diagram. args
        and kwargs are directly propagated to the Figure.plot
        command."""

        l, = self.ax.plot(NP.arccos(corrcoef), stddev,
                          *args, **kwargs) # (theta,radius)
        self.samplePoints.append(l)

        return l

    def add_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours."""

        rs,ts = NP.meshgrid(NP.linspace(self.smin,self.smax),
                            NP.linspace(0,NP.pi/2.0))
        # Compute centered RMS difference
        rms = NP.sqrt(self.refstd**2 + rs**2 - 2*self.refstd*rs*NP.cos(ts))
        
        contours = self.ax.contour(ts, rs, rms, levels,linewidths=0.1, **kwargs)
        #contours = self.ax.contour(ts, rs, rms, levels,linewidths=0.01, **kwargs)

        return contours


if __name__=='__main__':

    # Reference dataset
    x = NP.linspace(0,4*NP.pi,100)
    data = NP.sin(x)
    refstd = data.std(ddof=1)           # Reference standard deviation

    # Models
    m1 = data + 0.2*NP.random.randn(len(x))    # Model 1
    m2 = 0.8*data + .1*NP.random.randn(len(x)) # Model 2
    m3 = NP.sin(x-NP.pi/10)                    # Model 3

    # Compute stddev and correlation coefficient of models
    samples = NP.array([ [m.std(ddof=1), NP.corrcoef(data, m)[0,1]]
                         for m in (m1,m2,m3)])

    fig = PLT.figure(figsize=(10,4))
    
    ax1 = fig.add_subplot(1,2,1, xlabel='X', ylabel='Y')
    # Taylor diagram
    dia = TaylorDiagram(refstd, fig=fig, rect=122, label="Reference")

    colors = PLT.matplotlib.cm.jet(NP.linspace(0,1,len(samples)))

    ax1.plot(x,data,'ko', label='Data')
    for i,m in enumerate([m1,m2,m3]):
        ax1.plot(x,m, c=colors[i], label='Model %d' % (i+1))
    ax1.legend(numpoints=1, prop=dict(size='small'), loc='best')

    # Add samples to Taylor diagram
    for i,(stddev,corrcoef) in enumerate(samples):
        dia.add_sample(stddev, corrcoef, marker='s', markersize=6,ls='', c=colors[i],
                       label="Model %d" % (i+1))

    # Add RMS contours, and label them
    contours = dia.add_contours(colors='0.5')
    PLT.clabel(contours, inline=0.1, fontsize=3)

    # Add a figure legend
    fig.legend(dia.samplePoints,
               [ p.get_label() for p in dia.samplePoints ],
               numpoints=1, prop=dict(size='small'), loc='upper right')


    PLT.show()

