"""Refreshes data for the site.
Pulls in new data, processes it, and prepares the site to serve freshly
updated data.
"""

import utils.analysis_utils as a_utils
from utils import plot_utils, plot_utils_mpl


# Fetch current data, which is xml, and convert to readings.
current_data = a_utils.fetch_current_data(fresh=False)
readings = a_utils.process_xml_data(current_data)

# Focus on most recent readings, not an entire week.
recent_readings = a_utils.get_recent_readings(readings, 48)
critical_points = a_utils.get_critical_points(recent_readings)

# Simple interactive plot of current data.
plot_utils.plot_current_data_html(recent_readings)

# Interactive forecast plot.
plot_utils.plot_interactive_critical_forecast_html(recent_readings)

# Static forecast plot.
plot_utils_mpl.plot_critical_forecast_mpl(recent_readings,
                                                    critical_points)

# Static forecast plot, extended.
plot_utils_mpl.plot_critical_forecast_mpl_extended(recent_readings,
                                                      critical_points)
