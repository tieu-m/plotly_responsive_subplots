# requirements: plotly and numpy
# pip install pl
#
# This script create a plotly figure with two subplots:
# A grid of points is plotted on the first subplot; on a click on one point (xp, yp)
# the curve y = x^xp - x^yp is plotted on the second subplot

import time
from DemoSubplots.plotly_objects import generate_figure_with_plotly_objects
from DemoSubplots.dict_objects import generate_figure_with_dict_objects


if __name__ == '__main__':
    t_start = time.time()
    generate_figure_with_plotly_objects(10)
    print('Time spent with plotly objects: {:.2f} s'.format(time.time() - t_start))
    t_start = time.time()
    generate_figure_with_dict_objects(10)
    print('Time spent with dictionary objects: {:.2f} s'.format(time.time() - t_start))
