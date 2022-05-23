import numpy as np
from bokeh.plotting import figure, output_file, show, save
from bokeh.io import export_png
from bokeh.layouts import layout, gridplot
from bokeh.models import LinearAxis
from bokeh.models import Range1d
from bokeh.models.widgets import Panel
from bokeh.plotting import figure
from programTools import bandPassFilter, moving_average
import matplotlib.pyplot as plt

import numpy
import pandas as pd

TOOLTIPS = [
    ("(x,y)", "($x, $y)"),
]
width = 1500
height = 400
renderer = 'canvas'
graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

paths = [
    "./1oring",
    "./none",
    "./mangueira",
]

for path in paths:

    df = pd.read_csv(path + '.csv', ',', names=['x', 'y', 'z', 'gx', 'gy', 'gz', 't', 'none'])

    time = pd.to_numeric(df['t']) / 1000  # 2.773.880 max
    x_axis = pd.to_numeric(df['x'])
    y_axis = pd.to_numeric(df['y'])
    z_axis = pd.to_numeric(df['z'])

    #gx_axis = pd.to_numeric(df['gx']) --0.30
    #gy_axis = pd.to_numeric(df['gy']) --0.15
    #gz_axis = pd.to_numeric(df['gz']) --0.06

    but = 1000
    top = int(len(z_axis) - 1000)
    media_movel_size = 50000

    # Pitch
    angleY = -(numpy.arctan2(x_axis, numpy.sqrt(pow(y_axis, 2) + pow(z_axis, 2))) * 180) / 3.14
    # Roll
    angleX = (numpy.arctan2(y_axis, numpy.sqrt(pow(x_axis, 2) + pow(z_axis, 2))) * 180) / 3.14

    angleY_filter = bandPassFilter(angleY, cutf=2, order=2)

    #gx_axis = bandPassFilter(gx_axis, cutf=20, order=3)
    #gy_axis = bandPassFilter(gy_axis, cutf=20, order=3)
    #gz_axis = bandPassFilter(gz_axis, cutf=20, order=3)
    #gy_filter = moving_average(gy_axis, media_movel_size)

    speed = numpy.zeros(top - but * 2)
    for i in range(but * 2, top-5000):
        speed[i - but * 2] = ((angleY_filter[i + 5000] - angleY_filter[i-but]) / (time[i + 5000] - time[i-but])) * 60 * (23 * 60 + 55)

    speed_filter = bandPassFilter(speed, cutf=2, order=2)
    speed_filter = bandPassFilter(speed_filter, cutf=1, order=1)
    speed_filter = moving_average(speed_filter, media_movel_size)


    fig, axs = plt.subplots(3, figsize=(16, 9), sharex='all')

    axs[0].plot(time[but:top], x_axis[but:top], color='blue', label='X axis')
    axs[0].plot(time[but:top], y_axis[but:top], color='red', label='y axis')
    axs[0].plot(time[but:top], z_axis[but:top], color='green', label='z axis')
    axs[0].set(xlabel='time', ylabel='G')
    axs[0].legend(loc="upper right")


    axs[1].plot(time[but:top], angleX[but:top], color='orange', label='Roll')
    axs[1].plot(time[but:top], angleY[but:top], color='cyan', label='Pitch')
    axs[1].plot(time[but:top], angleY_filter[but:top], color='grey', label='Pitch (Low Pass Filter)')
    axs[1].set(xlabel='time', ylabel='Angle(deg)')
    axs[1].legend(loc="upper right")

    axs[2].plot(time[(2 * but + media_movel_size):(top + 1)], speed_filter, color='black', label='Angle(deg)/dia')
    axs[2].axhline(360, color = 'gray', label = 'target')
    #axs[2].plot(time, gx_axis * 60 * (23 * 60 + 55), color='blue', label='Angle(deg)/dia')
    #axs[2].plot(time[(2 * but + media_movel_size):(top + 1)], gy_filter[2 * but:-1000] * 60 * (23 * 60 + 55), color='red', label='Angle(deg)/dia')
    #axs[2].plot(time, gz_axis * 60 * (23 * 60 + 55), color='green', label='Angle(deg)/dia')
    axs[2].set(xlabel='time', ylabel='Angle(deg)/dia')
    axs[2].legend(loc="upper right")

    fig.suptitle(path)
    plt.savefig(path + '.pdf', bbox_inches='tight')
    plt.close()


    #
    #
    #output_file(path + ".html")
    #p_1 = figure(x_axis_label='time(s)',
    #              y_axis_label='G',
    #              plot_width=width, plot_height=height,
    #              toolbar_location="below",
    #              tooltips=TOOLTIPS,
    #              # output_backend=renderer,
    #              tools=graphTools, )
    #
    # p_2 = figure(x_axis_label='time(s)',
    #              y_axis_label='Angle(deg)',
    #              plot_width=width, plot_height=height,
    #              toolbar_location="below",
    #              tooltips=TOOLTIPS,
    #              output_backend=renderer,
    #              tools=graphTools, )
    #
    # p_3 = figure(x_axis_label='time(s)',
    #              y_axis_label='Angle(deg)',
    #              plot_width=width, plot_height=height,
    #              toolbar_location="below",
    #              tooltips=TOOLTIPS,
    #              output_backend=renderer,
    #              tools=graphTools, )
    #
    # p_4 = figure(x_axis_label='time(s)',
    #              y_axis_label='Angle(deg)/dia',
    #              plot_width=width, plot_height=height,
    #              toolbar_location="below",
    #              tooltips=TOOLTIPS,
    #              output_backend=renderer,
    #              tools=graphTools, )
    #
    # # add a line renderer
    # p_1.line(time[but:top], x_axis[but:top], line_width=2, color='blue', legend_label='X axis')
    # p_1.line(time[but:top], y_axis[but:top], line_width=2, color='red', legend_label='Y axis')
    # p_1.line(time[but:top], z_axis[but:top], line_width=2, color='green', legend_label='Z axis')
    #
    # p_2.line(time[but:top], angleX[but:top], line_width=2, color='orange', legend_label='Roll')
    # p_2.line(time[but:top], angleY[but:top], line_width=2, color='cyan', legend_label='Pitch')
    #
    # p_3.line(time[but:top], angleY_filter[but:top], line_width=3, color='cyan', legend_label='Pitch (Low Pass Filter)')
    # p_4.line(time[(2 * but + media_movel_size):(top + 1)], speed_filter, line_width=2, color='black',
    #          legend_label='Angle(deg)/dia')
    #
    # p_1.toolbar.logo = None
    # p_1.legend.location = "top_left"
    # p_1.legend.click_policy = "hide"
    # p_1.legend.label_text_font_size = '14pt'
    # p_2.toolbar.logo = None
    # p_2.legend.location = "top_left"
    # p_2.legend.click_policy = "hide"
    # p_2.legend.label_text_font_size = '14pt'
    # p_3.toolbar.logo = None
    # p_3.legend.location = "top_left"
    # p_3.legend.click_policy = "hide"
    # p_3.legend.label_text_font_size = '14pt'
    # p_4.toolbar.logo = None
    # p_4.legend.location = "top_left"
    # p_4.legend.click_policy = "hide"
    # p_4.legend.label_text_font_size = '14pt'
    #
    # # p_1.x_range = Range1d(100, 10000)
    # # p_2.x_range = Range1d(100, 10000)
    # # p_3.x_range = Range1d(100, 10000)
    # # p_4.x_range = Range1d(100, 10000)
    #
    # p_1.y_range = Range1d(-1.2, 1.2)
    # p_2.y_range = Range1d(-5, 60)
    # p_3.y_range = Range1d(-5, 60)
    # p_4.y_range = Range1d(300, 400)
    #
    # gd = [
    #     [p_1],
    #     [p_2],
    #     [p_3],
    #     [p_4]]
    #
    # grid = gridplot(gd, plot_width=width, plot_height=height, merge_tools=True, toolbar_location='left',
    #                 sizing_mode='scale_width')
    #
    # l = layout(grid)
    # save(l)
