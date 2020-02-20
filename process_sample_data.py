"""Pulls in sample data, processes it, and prepares the site to serve this
sample data.
"""

import pickle

import utils.analysis_utils as a_utils
from utils import plot_utils, plot_utils_mpl


filename = 'sample_data/reading_dump_09212019.pkl'

with open(filename, 'rb') as f:
    recent_readings = pickle.load(f)


# current_data = a_utils.fetch_current_data(fresh=False)

# readings = a_utils.process_xml_data(current_data)

# recent_readings = a_utils.get_recent_readings(readings, 48)
# critical_points = a_utils.get_critical_points(recent_readings)

plot_utils.plot_current_data_html(recent_readings)

plot_utils.plot_current_data_cone(recent_readings[:86])

plot_utils_mpl.plot_critical_forecast_mpl(recent_readings[:86])