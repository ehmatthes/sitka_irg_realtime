"""Plotting utility functions, using mpl."""

import pytz

import matplotlib.pyplot as plt


aktz = pytz.timezone('US/Alaska')


def plot_critical_forecast_mpl_extended(readings, critical_points=[],
        filename=None):
    """Extends critical forecast back 6 hours as well.
    """
    # DEV: This fn should receive any relevant slides, it shouldn't do any
    #   data processing.

    # Matplotlib accepts datetimes as x values, so it should be handling
    #   timezones appropriately.
    datetimes = [reading.dt_reading.astimezone(aktz) for reading in readings]
    heights = [reading.height for reading in readings]

    critical_datetimes = [reading.dt_reading.astimezone(aktz) for reading in critical_points]
    critical_heights = [reading.height for reading in critical_points]

    min_height = min([reading.height for reading in readings])
    max_height = max([reading.height for reading in readings])

    # Build a set of future readings, once every 15 minutes for the next
    #   6 hours.
    # DEV: May want to only look ahead 4.5 hrs; looking farther ahead
    #   than the critical 5-hour period seems less meaningful.
    # DEV: Doing some imports here, because this will be moved to 
    #   analysis_utils
    import datetime
    from .ir_reading import IRReading

    interval = datetime.timedelta(minutes=15)
    future_readings = []
    new_reading_dt = readings[-1].dt_reading + interval
    for _ in range(18):
        new_reading = IRReading(new_reading_dt, 23.0)
        future_readings.append(new_reading)
        new_reading_dt += interval
    future_datetimes = [r.dt_reading.astimezone(aktz) for r in future_readings]
    future_heights = [r.height for r in future_readings]

    # What are the future critical points?
    #   These are the heights that would result in 5-hour total rise and 
    #     average rate matching critical values.
    #   These are the minimum values needed to become, or remain, critical.
    # DEV: Replace all 0.5 and 2.5 with M_CRITICAL and CRITICAL_RISE
    min_cf_readings = []
    latest_reading = readings[-1]
    for reading in future_readings:
        dt_lookback = reading.dt_reading - datetime.timedelta(hours=5)
        # Get minimum height from last 5 hours of readings, including future readings.
        # print(reading.dt_reading - datetime.timedelta(hours=5))
        relevant_readings = [r for r in readings
            if r.dt_reading >= dt_lookback]
        relevant_readings += min_cf_readings
        critical_height = min([r.height for r in relevant_readings]) + 2.5

        # Make sure critical_height also gives a 5-hour average rise at least
        #   as great as M_CRITICAL. Units are ft/hr.
        m_avg = (critical_height - relevant_readings[0].height) / 5
        if m_avg < 0.5:
            # The critical height satisfies total rise, but not sustained rate
            #   of rise. Bump critical height so it satisfies total rise and
            #   rate of rise.
            critical_height = 5 * 0.5 + relevant_readings[0].height

        new_reading = IRReading(reading.dt_reading, critical_height)
        min_cf_readings.append(new_reading)

    min_cf_datetimes = [r.dt_reading.astimezone(aktz) for r in min_cf_readings]
    min_cf_heights = [r.height for r in min_cf_readings]

    # What would the critical points have been over the last 6 hours?
    #   This shows how close conditions were to being critical over the
    #   previous 6 hours.
    dt_first_min_prev_reading = latest_reading.dt_reading - datetime.timedelta(hours=6)
    min_crit_prev_readings = [IRReading(r.dt_reading, 27.0)
                                for r in readings
                                if r.dt_reading >= dt_first_min_prev_reading]

    for reading in min_crit_prev_readings:
        dt_lookback = reading.dt_reading - datetime.timedelta(hours=5)
        # Get minimum height from last 5 hours of readings.
        relevant_readings = [r for r in readings
            if (r.dt_reading >= dt_lookback) and (r.dt_reading < reading.dt_reading)]
        critical_height = min([r.height for r in relevant_readings]) + 2.5

        # Make sure critical_height also gives a 5-hour average rise at least
        #   as great as M_CRITICAL. Units are ft/hr.
        m_avg = (critical_height - relevant_readings[0].height) / 5
        if m_avg < 0.5:
            # The critical height satisfies total rise, but not sustained rate
            #   of rise. Bump critical height so it satisfies total rise and
            #   rate of rise.
            critical_height = 5 * 0.5 + relevant_readings[0].height

        reading.height = critical_height

    min_crit_prev_datetimes = [r.dt_reading.astimezone(aktz)
                                for r in min_crit_prev_readings]
    min_crit_prev_heights = [r.height for r in min_crit_prev_readings]

    # Want current data to be plotted with a consistent scale on the y axis.
    y_min, y_max = 20.0, 27.5

    # Set date string for chart title.
    dt_title = readings[-1].dt_reading.astimezone(aktz)
    title_date_str = dt_title.strftime('%m/%d/%Y %H:%M')

    # --- Plotting code

    # Build static plot image.
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=128)

    # Always plot on an absolute y scale.
    ax.set_ylim([20.0, 27.5])

    # Add river heights for the current set of readings.
    ax.plot(datetimes, heights, c='blue', alpha=0.8, linewidth=1)

    # Add critical points if relevant.
    if critical_points:
        ax.plot(critical_datetimes, critical_heights, c='red', alpha=0.6,
                linewidth=1)
        ax.scatter(critical_datetimes, critical_heights, c='red', alpha=0.8,
                s=15)
        # cp_label = critical_points[0].dt_reading.astimezone(aktz).strftime(
                # '%m/%d/%Y %H:%M:%S')
        # Labeling doesn't work well on live plot.
        # label_time = critical_points[0].dt_reading.astimezone(aktz)
        # cp_label = label_time.strftime('%m/%d/%Y %H:%M:%S') + '    '
        # ax.text(label_time, critical_heights[0], cp_label,
        #         horizontalalignment='right')

    # Plot minimum future critical readings.
    #   Plot these points, and shade to max y value.
    ax.plot(min_cf_datetimes, min_cf_heights, c='red', alpha=0.4)
    ax.fill_between(min_cf_datetimes, min_cf_heights, 27.5, color='red', alpha=0.2)

    # Plot previous critical readings, and shade to max y value.
    ax.plot(min_crit_prev_datetimes, min_crit_prev_heights, c='red', alpha=0.3)
    ax.fill_between(min_crit_prev_datetimes, min_crit_prev_heights, 27.5,
                                                    color='red', alpha=0.1)

    # Add labels for critical regions.
    ax.text(0.78, 0.98, 'Previous \n6 hrs', verticalalignment='top',
            transform=ax.transAxes, fontsize=12)
    ax.text(0.89, 0.98, 'Next \n4.5 hrs', verticalalignment='top',
            transform=ax.transAxes)

    # Set chart and axes titles, and other formatting.
    title = f"Indian River Gauge Readings - {title_date_str}"
    ax.set_title(title, loc='left')
    ax.set_xlabel('', fontsize=16)
    ax.set_ylabel("River height (ft)")


    # Make major and minor x ticks small.
    ax.tick_params(axis='x', which='both', labelsize=8)

    # DEV: Uncomment this to see interactive plots during dev work,
    #   rather than opening file images.
    # plt.show()

    # Save to file.
    # filename = f"current_ir_plots/ir_plot_{readings[-1].dt_reading.__str__()[:10]}.png"
    if not filename:
        filename = "media/plot_images/irg_critical_forecast_plot_current_extended.png"
    plt.savefig(filename, bbox_inches='tight')

    print(f"  saved: {filename}")

    # Close figure, especially helpful when rendering many frames for animation.
    plt.close('all')