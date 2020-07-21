"""Generate animation of a 48-hour period."""

# Needs 48 hours of readings prior to initial point as well.


import os, sys
from pathlib import Path

import utils.analysis_utils as a_utils
from utils import plot_utils, plot_utils_mpl

# Will store a number of specific data files here, and then act on data_file.
usgs_data_file = 'animation_input_files/current_data_usgs.txt'
kramer_data_file = 'animation_input_files/reading_dump_08192015.pkl'

data_file = usgs_data_file
readings_per_hour = 4
file_extension = Path(data_file).suffix

if file_extension == '.txt':
    readings = a_utils.process_usgs_data(data_file)
elif file_extension == '.pkl':
    with open(data_file, 'rb') as f:
        readings = pickle.load(f)
else:
    print("Data file extension not recognized:", file_extension)

# Make sure readings are sorted.
prev_reading = readings[0]
for reading in readings:
    if reading.dt_reading < prev_reading.dt_reading:
        print(f"Out of order!")
    prev_reading = reading

# sys.exit()

# --- This remains the same, regardless of what the data source was. ---

# # Focus on most recent readings, not an entire week.
# recent_readings = a_utils.get_recent_readings(readings, 48)
# critical_points = a_utils.get_critical_points(recent_readings)

# # Static forecast plot, extended.
# plot_utils_mpl.plot_critical_forecast_mpl_extended(recent_readings,
#                                                       critical_points,
#                                                       filename='test_animation.png')





# Modify plot_cfme() to generate an animation instead of static plot.
#  May take 48*4*20 sec to run???

# Get rid of any existing animation files.
os.system('rm -rf animation_frames')
os.system('mkdir animation_frames')

# Loop over a set of readings, and send successive sets of readings
#  and numbered filenames to pcfme()
first_index = 0
while first_index < len(readings) - 48*readings_per_hour+1:
    # ffmpeg will use images in alphabetical order, so zero-pad frame numbers.
    alph_frame_str = f"{first_index:04}"
    frame_filename = f"animation_frames/animation_frame_{alph_frame_str}.png"
    end_index = first_index + 48*readings_per_hour
    frame_readings = readings[first_index:end_index]
    critical_points = a_utils.get_critical_points(frame_readings)

    plot_utils_mpl.plot_critical_forecast_mpl_extended(
            frame_readings,
            critical_points,
            filename=frame_filename)

    first_index += 1

    # if first_index > 10:
    #     break

os.system("cd animation_frames && ffmpeg -framerate 5 -pattern_type glob -i '*.png'   -c:v libx264 -pix_fmt yuv420p animation_file_out.mp4")
os.system("cp animation_frames/animation_file_out.mp4 animation_output/animation_file_out.mp4")