"""Refreshes data for the site.
Pulls in new data, processes it, and prepares the site to serve freshly
updated data.
"""

import utils.analysis_utils as a_utils

current_data = a_utils.fetch_current_data(fresh=False)