from utils_refactor import *
from stations import StationClient, GroupStation
from progress_bar import ProgressBar

groups_df: list[GroupStation] = []
clients_df: list[StationClient] = []
day_index, adom_index = 0, 0

save_path = None  # the path the user want to save to
document = Document()
style = document.styles['Normal']
font = style.font
font.rtl = True
cmap = plt.cm.tab10

def main(path: str, path_to_save: str):
    global document, save_path

    save_path = path_to_save
    path_to_server_data, scenarios = days_and_scenerios(path)
    pathes_to_clients_data, pathes_to_tracking_groups_data = get_all_pathes(path_to_server_data, scenarios)
    graphs_editor(pathes_to_clients_data, pathes_to_tracking_groups_data, scenarios)


def set_t0():
    '''
    sets all the stations t0 as the same
    :return: t0, False if there is no valid
    '''
    global groups_df
    
    first_seconds_li = []

    for i, group_station in enumerate(groups_df):
        first_seconds_li.append(group_station.time[0])

    first_seconds = min(first_seconds_li)

    for i, group_station in enumerate(groups_df):
        groups_df[i].time = [second - first_seconds for second in group_station.time]

    for i, client_station in enumerate(clients_df):
        clients_df[i].time = [second - first_seconds for second in client_station.time.copy()]
        if client_station.type != 'OpticClient':
            if  clients_df[i].time[0] < 0:
                clients_df[i].time += abs(clients_df[i].time[0])
            
    return first_seconds


def graphs_editor(pathes_to_clients_data: list, pathes_to_tracking_groups_data: list, scenarios: list):
    '''
    :param pathes_to_clients_data: list of all the pathes where client data are exits
    :param pathes_to_tracking_groups_data: list of all the pathes where tracking group data are exits
    :param scenerios: list of the scenerios to iterate over
    :return: the complete document
    '''
    global document, groups_df, clients_df, save_path, day_index, adom_index
    
    for i in range(len(scenarios)):
        scenario = scenarios[i].split('-')[0:2]
        day_and_adom_indexes = list(map(int, re.findall(r'\d+', f'{scenario[0] + scenario[1]}')))
        day_index, adom_index = day_and_adom_indexes[0], day_and_adom_indexes[1]
        clients_df = get_clients_data(pathes_to_clients_data[i])
        groups_df = get_groups_data(pathes_to_tracking_groups_data[i])

        if len(groups_df) > 0:

            add_title(document, f'{day_fire} {day_index} - {scenrio_fire} {adom_index} ')
            first_seconds = set_t0()
            easting_northing()
            time_altitude()
            spatial_comparison()
            set_azi_ele()
            validation_graph()
            print(f'Day {day_index}, scenario {adom_index} Done!')

    document.save(f'{save_path}/summery.docx')
    print("ALL DONE!")


def easting_northing():
    '''
    makes top view graph
    '''
    global document, groups_df, cmap, day_index, adom_index

    file_name = 'Easting-Northing'

    for i, group_station in enumerate(groups_df):
        plt.scatter(group_station.E, group_station.N, label=group_station.name, s=0.5, color=cmap(i))

    path = f'{save_path}/day{day_index}-scenerio{adom_index}-{file_name}.png'

    # Apply ScalarFormatter to current axes
    plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    # Disable scientific notation (like +1e6 offset)
    plt.ticklabel_format(style='plain', axis='both')

    plt.axis('equal')
    plt.legend(loc='best', markerscale=4)
    plt.title(label='Missile Trajectory - Top View \n'
                    '   Local UTM')
    plt.xlabel(xlabel='Easting[m]')
    plt.ylabel(ylabel='Northing[m]')
    plt.grid()
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()

    p = add_p(document, "Hebrew")
    add_text(p, experiment_top_view_text)
    add_image(p, path)
    document.add_page_break()


def time_altitude():
    '''
    makes altitude as a function of time graph
    '''
    global document, groups_df, save_path, cmap, day_index, adom_index

    file_name = 'Altitude-Time'
    for i, group_station in enumerate(groups_df):
        plt.scatter(group_station.time, group_station.alt, label=group_station.name, s=0.5, color=cmap(i))

    path = f'{save_path}/day{day_index}-scenerio{adom_index}-{file_name}.png'
    plt.legend(loc='best', markerscale=4)
    plt.title(label='Altitude as a function of Time \n'
                    'Local UTM')
    plt.xlabel(xlabel='Time[sec]')
    plt.ylabel(ylabel='Altitude[m]')
    plt.grid()
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()

    p = add_p(document, "Hebrew")
    add_text(p, experiment_alt_time_text)
    add_image(p, path)
    document.add_page_break()


def spatial_comparison():
    '''
    Calculate the spatial comparison between the group stations
    :return: list of errors and the names by the same order
    '''
    global groups_df

    errors = []  # contains all the errors for the stations
    times = [] # contains all the time for the stations
    names = [] # contains all the names for the stations 
    for i in range(len(groups_df)):
        for j in range(i+1, len(groups_df)):
            errors_i_to_j = []  # the errors between one station to another
            if i < j:
                coords_i_to_j = [(groups_df[i].E, groups_df[j].E),
                                    (groups_df[i].N, groups_df[j].N),
                                    (groups_df[i].alt, groups_df[j].alt)]
                time_i_to_j = groups_df[i].time if len(groups_df[i].time) > len(groups_df[j].time) else groups_df[j].time
                if np.array_equal(groups_df[i].time, groups_df[j].time):
                    errors_i_to_j = [coord[0] - coord[1] for coord in coords_i_to_j]
                else:
                    time_step = 0.1
                    min_time = np.maximum(groups_df[i].time[0], groups_df[j].time[0])
                    max_time = np.minimum(groups_df[i].time[-1], groups_df[j].time[-1])
                    time_i_to_j = np.arange(min_time, max_time + time_step,
                                                time_step)  # from min_time to max_time, INCLUDED
                    for coord in coords_i_to_j:
                        interp1 = np.interp(time_i_to_j, groups_df[i].time, coord[0])
                        interp2 = np.interp(time_i_to_j, groups_df[j].time, coord[1])
                        errors_i_to_j.append(interp1 - interp2)
                errors.append(errors_i_to_j)
                times.append(time_i_to_j)
                names.append([groups_df[i].name, groups_df[j].name])
    
    spatial_comparison_graph(errors, times, names)


def spatial_comparison_graph(errors: np.array, times: list, names:list):
    '''
    create the spatial_comparison graph
    param errors: list of lists of errors - y axis
    param times: list of lists of time errors - x axis
    names: list of lists, each list contain 2 names of groups
    :return:
    '''
    global save_path, document, groups_df, day_index, adom_index 

    if len(errors) > 0:
        p = add_p(document, "Hebrew")
        add_text(p, experiment_traj_text)

    legend_labels = [r"$\mu_{{dE}}$ = [m]" + "\n" + r"$\sigma_{{dE}}$ = [m]",
                     r"$\mu_{{dN}}$ = [m]" + "\n" + r"$\sigma_{{dN}}$ = [m]",
                     r"$\mu_{{dH}}$ = [m]" + "\n" + r"$\sigma_{{dAlt}}$ =  [m]"]

    file_name = 'spatial_comparison'
    path = f'{save_path}/day{day_index}-scenerio{adom_index}-{file_name}'

    for i in range(len(errors)):
        error_average_tot = 0
        standart_deviation_tot = 0
        for index_column, column in enumerate(errors[i]):
            error_average = np.average(errors[i][index_column])
            standart_deviation = np.std(errors[i][index_column])
            error_average_tot += np.square(error_average)
            standart_deviation_tot += np.square(standart_deviation)
            legend_label = legend_labels[index_column][:14] + f'{error_average:.2f}' + \
                            legend_labels[index_column][14:-3] + f'{standart_deviation:.2f}' + '[m]'
            plt.scatter(times[i], column, s=0.5, label=legend_label)

        error_average_tot = np.sqrt(error_average_tot)
        standart_deviation_tot = np.sqrt(standart_deviation_tot)

        plt.legend(loc='best', markerscale=4)
        plt.title(label='Spatial Comparison \n'
                        f'{names[i][0]} compared to {names[i][1]}')
        plt.xlabel(xlabel='Time[sec]')
        plt.ylabel(ylabel='Difference[m]')
        plt.grid()
        plt.savefig(f'{path} {names[i][0]} {names[i][1]}.png', dpi=200, bbox_inches='tight')
        plt.close()

        add_image(p, f'{path} {names[i][0]} {names[i][1]}.png')
        add_text(p, f'{error_average_tot:.2f}, {standart_devision_text} {standart_deviation_tot:.2f}')
        # todo: make the right errors and chnage the text vaeibales a little
        document.add_page_break()


def set_azi_ele():
    '''
    set all the stations by the right azimuth and elevation by every tracking group to calculate the errors
    '''
    global document, clients_df, groups_df
    for i in range(len(groups_df)):
        if 'opt' not in groups_df[i].name.lower():
            for client in clients_df:
                if client.type == 'OpticClient':
                    groups_df[i].az_el_projection([client.easting, client.northing, client.height, client.time])
                    groups_df[i].filter_junk_ele_azi()
                    graph_azi_ele(client, groups_df[i])
                    azimuth_elevation_errors(client, groups_df[i])


def graph_azi_ele(karnatz: StationClient, group: GroupStation):
    '''
    crete the azimuth and elevation graph
    '''
    global document, save_path, day_index, adom_index

    file_name = f'azi {karnatz.name}_{group.name}'
    path = f'{save_path}/day{day_index + 1}-scenerio{adom_index + 1}-{file_name}.png'

    first_seconds = min(karnatz.time[0], group.time[0])
    karnatz.time = [second - first_seconds for second in karnatz.time.copy()]
    group.time_temp = [second - first_seconds for second in group.time.copy()]

    azimuth0 = karnatz.azimuth[0]
    # set the azimuth to 0-360
    for i, azi in enumerate(group.azimuth):
        if azi > azimuth0 + 180:
            group.azimuth[i] = azi - 360
        elif azi < azimuth0 - 180:
            group.azimuth[i] = azi + 360
    for i, azi in enumerate(karnatz.azimuth):
        if azi > azimuth0 + 180:
            karnatz.azimuth[i] = azi - 360
        elif azi < azimuth0 - 180:
            karnatz.azimuth[i] = azi + 360

    plt.scatter(karnatz.time, karnatz.azimuth, s=0.5, label=karnatz.name)
    plt.scatter(group.time_in_seconds, group.azimuth, s=0.5, label=group.name)
    plt.xlabel(xlabel='Time[sec]')
    plt.ylabel(ylabel='Azimuth[deg]')
    plt.title(f'{karnatz.name} Azimuth')
    plt.grid()
    plt.legend(loc='best', markerscale=4)
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()

    p = add_p(document, "Hebrew")
    add_text(p, f'{angle_accuracies_generic_text} {karnatz.name}')
    add_image(p, path)

    file_name = f'ele {karnatz.name}_{group.name}'
    path = f'{save_path}/day{day_index + 1}-scenerio{adom_index + 1}-{file_name}.png'

    plt.scatter(karnatz.time, karnatz.elevation, s=0.5, label=karnatz.name)
    plt.scatter(group.time_in_seconds, group.elevation, s=0.5, label=group.name)
    plt.xlabel(xlabel='Time[sec]')
    plt.ylabel(ylabel='Elevation[deg]')
    plt.title(f'{karnatz.name} Elevation')
    plt.grid()
    plt.legend(loc='best', markerscale=4)
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()

    add_image(p, path)
    document.add_page_break()


def azimuth_elevation_errors(karnatz: StationClient, group_station: GroupStation):
    '''
    calculate the angles arrors and make graph of them. 
    '''
    global document, save_path, day_index, adom_index

    min_time = np.maximum(karnatz.time[0], group_station.time_in_seconds[0])
    max_time = np.minimum(karnatz.time[-1], group_station.time_in_seconds[-1])
    time = karnatz.time
    time_index = (time > min_time) & (time < max_time)
    reference_azimuth = np.interp(karnatz.time, group_station.time_in_seconds, group_station.azimuth)
    reference_elevation = np.interp(karnatz.time, group_station.time_in_seconds, group_station.elevation)

    azimuth_errors = (karnatz.azimuth - reference_azimuth) * np.pi / 180 * 1000
    azimuth_errors = azimuth_errors[time_index]
    elevation_errors = (karnatz.elevation - reference_elevation) * np.pi / 180 * 1000
    elevation_errors = elevation_errors[time_index]

    error_average_azimuth = np.average(azimuth_errors)
    standart_devision_azimuth = np.std(azimuth_errors)
    error_average_elevation = np.average(elevation_errors)
    standart_devision_elevation = np.std(elevation_errors)

    file_name = f'azi errors {karnatz.name}_{group_station.name}'
    path = f'{save_path}/day{day_index + 1}-scenerio{adom_index + 1}-{file_name}.png'

    plt.scatter(time[0: len(azimuth_errors)], azimuth_errors, s=0.5)
    plt.xlabel(xlabel='Time[sec]')
    plt.ylabel(ylabel='Azimuth errors[mrad]')
    plt.title(f'{karnatz.name, group_station.name} Azimuth errors')
    plt.grid()
    plt.savefig(path)
    plt.close()

    p = add_p(document, "Hebrew")
    add_image(p, path)

    file_name = f'ele errors {karnatz.name}_{group_station.name}'
    path = f'{save_path}/day{day_index + 1}-scenerio{adom_index + 1}-{file_name}.png'

    plt.scatter(time[0: len(elevation_errors)], elevation_errors, s=0.5)
    plt.xlabel(xlabel='Time[sec]')
    plt.ylabel(ylabel='Elevation errors[mrad]')
    plt.title(f'{karnatz.name, group_station.name} Elevation errors')
    plt.grid()
    plt.savefig(path)
    plt.close()

    add_image(p, path)
    add_text(p, angle_errors_distributions_average_text)  # todo: make the right errors and chnage the text vaeibales a little
    add_text(p, f'{spetial_error_azimuth_formula_txt} {error_average_azimuth:.2f}, '
                  f'{standart_devision_text} {standart_devision_azimuth:.2f}')
    add_text(p,
             f'{spetial_error_elevation_formula_txt} {error_average_elevation:.2f}, '
             f'{standart_devision_text} {standart_devision_elevation:.2f}')
    document.add_page_break()


def validation_graph():
    '''
    create valid to time graph
    '''
    global document, day_index, adom_index, clients_df

    file_name = f'validation-time'
    path = f'{save_path}/day{day_index + 1}-scenerio{adom_index + 1}-{file_name}.png'
    max_gap = 0.3
    names = []

    for i, df in enumerate(clients_df):
        times = np.sort(df.time)
        segment_start = times[0]
        names.append(df.name)
        # Combine consecutive time points into segments if needed
        for j in range(1, len(times)):
            if times[j] - times[j - 1] > max_gap:
                plt.hlines(i, segment_start, times[j - 1], color='green', linewidth=5)
                segment_start = times[j]  # Start new segment

        plt.hlines(i, segment_start, times[-1], color='green', linewidth=5)

    plt.yticks(range(len(clients_df)), names)
    plt.xlabel("Time")
    plt.title("Validity Timeline")
    plt.grid()
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()

    p = add_p(document, "Hebrew")
    add_text(p, 'ולידציה לזמן לכל קליינט')
    add_image(p, path)
    document.add_page_break()
