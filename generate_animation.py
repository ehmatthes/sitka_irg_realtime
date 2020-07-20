"""Generate animation of a 48-hour period."""

# Needs 48 hours of readings prior to initial point as well.


import os, sys

import utils.analysis_utils as a_utils
from utils import plot_utils, plot_utils_mpl


usgs_data_file = 'current_data/current_data_usgs.txt'
readings = a_utils.process_usgs_data(usgs_data_file)

# --- This remains the same, regardless of what the data source was. ---

# Focus on most recent readings, not an entire week.
recent_readings = a_utils.get_recent_readings(readings, 48)
critical_points = a_utils.get_critical_points(recent_readings)

# Static forecast plot, extended.
plot_utils_mpl.plot_critical_forecast_mpl_extended(recent_readings,
                                                      critical_points,
                                                      filename='test_animation.png')
