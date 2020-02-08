from numpy import linspace
import plotly.io as pio
import os
import webbrowser
from random import randint


def generate_figure_with_dict_objects(num_points):
    # Create the figure, the subplot and set the appearance at once:
    fig = {
        'data': [],
        'layout': {'xaxis': {'anchor': 'y', 'domain': [0., 0.45], 'gridcolor': '#EBF0F8', 'linecolor': '#EBF0F8',
                             'zerolinecolor': '#EBF0F8', 'automargin': True,
                             'title': {'text': r'$\alpha$'}},
                   'xaxis2': {'anchor': 'y2', 'domain': [0.55, 1.], 'gridcolor': '#EBF0F8', 'linecolor': '#EBF0F8',
                              'zerolinecolor': '#EBF0F8', 'automargin': True, 'title': {'text': 'x'}},
                   'yaxis': {'anchor': 'x', 'domain': [0., 1.], 'gridcolor': '#EBF0F8', 'linecolor': '#EBF0F8',
                             'zerolinecolor': '#EBF0F8', 'automargin': True,
                             'title': {'text': r'$\beta$'}},
                   'yaxis2': {'anchor': 'x2', 'domain': [0., 1.], 'gridcolor': '#EBF0F8', 'linecolor': '#EBF0F8',
                              'zerolinecolor': '#EBF0F8', 'automargin': True, 'title': {'text': 'y'}},
                   'annotations': [{'font': {'size': 16}, 'showarrow': False, 'text': 'Data selection', 'x': 0.225,
                                    'xanchor': 'center', 'xref': 'paper', 'y': 1.0, 'yanchor': 'bottom',
                                    'yref': 'paper'},
                                   {'font': {'size': 16}, 'showarrow': False,
                                    'text': 'Curve plot: x<sup>&#945;</sup> - x<sup>&#946;</sup>', 'x': 0.775,
                                    'xanchor': 'center', 'xref': 'paper', 'y': 1.0, 'yanchor': 'bottom',
                                    'yref': 'paper'}],
                   'plot_bgcolor': 'white',
                   'title': {'text': 'Figure with dictionary objects'}}
    }

    # Create the grid of points for subplot 1
    x0 = []
    y0 = []
    for i in range(num_points):
        for j in range(num_points):
            x0.append(i)
            y0.append(j)

    # choose a default selected point:
    default = randint(0, len(x0)-1)

    # plot the grid of points:
    points_color = ['blue'] * len(x0)
    points_color[default] = 'red'
    customdata = ['point' + str(i) for i in range(num_points**2)]
    hovertext = ['x<sup>{}</sup> - x<sup>{}</sup>'.format(i, j) for i, j in zip(x0, y0)]
    fig['data'].append({'type': 'scatter', 'mode': 'markers', 'x': x0, 'y': y0, 'customdata': customdata,
                        'marker': {'color': points_color, 'size': 10},
                        'hovertext': hovertext, 'hoverinfo': 'text',
                        'name': 'data selector', 'xaxis': 'x', 'yaxis': 'y'})

    # set the data of subplot 2
    x = linspace(-10, 10, 101)
    for i in range(len(x0)):
        # do whatever you want to do with the points' info here
        y2 = x**x0[i] - x**y0[i]
        if i == default:
            fig['data'].append(
                {'type': 'scatter', 'mode': 'lines', 'x': x, 'y': y2,
                 'name': '$y = x^{{{}}} - x^{{{}}}$'.format(x0[i], y0[i]),
                 'customdata': ['point' + str(i)], 'visible': True, 'line': {'color': 'red'},
                 'xaxis': 'x2', 'yaxis': 'y2'})
        else:
            fig['data'].append(
                {'type': 'scatter', 'mode': 'lines', 'x': x, 'y': y2,
                 'name': '$y = x^{{{}}} - x^{{{}}}$'.format(x0[i], y0[i]),
                 'customdata': ['point' + str(i)], 'visible': False, 'line': {'color': 'red'},
                 'xaxis': 'x2', 'yaxis': 'y2'})

    # get the html figure to include some javascript
    html_str = pio.to_html(fig, include_plotlyjs='cdn', include_mathjax='cdn',
                           config={'scrollZoom': True})

    # get the div id (required for the javascript code) and set the js code
    div_id = html_str.split('document.getElementById("')[1].split('"')[0]
    js_code = """                myDiv = document.getElementById('{div}')
                myDiv.on('plotly_click', function(data){{
                    // get the custom data of the point that was clicked
                    traceId=data["points"]["0"]["customdata"];
                    allData = myDiv["data"];
                    // color in red the selected point and in blue the former selected point
                    pointnumber = data["points"][0]["pointIndex"];
                    for(i=0;i<allData[0]["marker"]["color"].length;i++){{
                        if(i==pointnumber){{
                            allData[0]["marker"]["color"][i] = "red";
                        }} else if (allData[0]["marker"]["color"][i] == "red"){{
                            allData[0]["marker"]["color"][i] = "blue";
                        }}
                    }}
                    // set the selected trace visible and every other invisible
                    for(i=0;i<allData.length;i++){{
                        if(allData[i]["xaxis"]=="x2" && allData[i]["customdata"][0]==traceId){{
                            // set the trace visible if on subplot 2 and share the same customdata
                            allData[i]["visible"] = true;
                        }}
                        else if (allData[i]["xaxis"]=="x2" && allData[i]["visible"]) {{
                            // set the trace invisible if on subplot 1 or doesn't share the same customdata
                            allData[i]["visible"] = false
                        }}
                    }}
                    // update the plot
                    Plotly.react('{div}', allData, myDiv["layout"], myDiv["config"])
                }});
    """.format(div=div_id)

    # index of the plot in the html string
    ind = html_str.find('if (document.getElementById("')
    # must count 8 '\n' before inserting our js code
    for i in range(8):
        ind = html_str.find('\n', ind) + 1
    html_str = html_str[:ind] + js_code + html_str[ind:]

    # save the figure in the current folder
    path = os.path.abspath('dict_fig.html')
    with open(path, 'w') as f:
        f.write(html_str)

    # show the figure
    webbrowser.open(path)
