"""Refreshes data for the site.
Pulls in new data, processes it, and prepares the site to serve freshly
updated data.
"""

import utils.analysis_utils as a_utils
from utils import plot_utils

current_data = a_utils.fetch_current_data(fresh=True)

readings = a_utils.process_xml_data(current_data)

recent_readings = a_utils.get_recent_readings(readings, 48)
critical_points = a_utils.get_critical_points(recent_readings)
plot_utils.plot_current_data_html(recent_readings)