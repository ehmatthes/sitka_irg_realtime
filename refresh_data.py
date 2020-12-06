"""Refreshes data for the site.
Pulls in new data, processes it, and prepares the site to serve freshly
updated data.
"""
import os, sys

import utils.analysis_utils as a_utils
from utils import plot_utils_mpl

# On deployed site, always use fresh data.
USE_FRESH_DATA = True
if os.environ.get('ENVIRON') == 'DEPLOYED':
    USE_FRESH_DATA = True

# # Fetch current data, which is xml, and convert to readings.
# current_data = a_utils.fetch_current_data(fresh=USE_FRESH_DATA)
# readings = a_utils.process_xml_data(current_data)

# Fetch data directly from USGS, which is a tab-separated file?
usgs_data_file = a_utils.fetch_current_data_usgs(fresh=USE_FRESH_DATA)
readings = a_utils.process_usgs_data(usgs_data_file)

# --- This remains the same, regardless of what the data source was. ---

# Focus on most recent readings, not an entire week.
recent_readings = a_utils.get_recent_readings(readings, 48)
critical_points = a_utils.get_critical_points(recent_readings)

# Static forecast plot, extended.
plot_utils_mpl.plot_critical_forecast_mpl_extended(recent_readings,
                                                      critical_points)
