import plotly.plotly as py 
import plotly.tools as tls 
from plotly.graph_objs import *
import numpy as np
py.sign_in("lisa.joelle.hachmann", "i6095yjs5o")


data = Data([
    Bar(
        x=['SpaceX', 'Tetris', 'Hitler', 'Witch', 'Cat'],
        y=[24,26,5,43, 33]
    )
])
plot_url = py.plot(data, filename='basic-bar')