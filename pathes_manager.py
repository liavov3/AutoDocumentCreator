import os
import json
import pandas as pd
from stations import GroupStation, StationClient


def days_and_scenerios(path: str):
    '''
    return the path to the server data with all the relevant scenarios 
    '''
    path_to_sky_control_data = get_to_SkyControl_server(path)
    scenerios = next(os.walk(path_to_sky_control_data))[1]

    for scenerio in scenerios.copy():
        if 'lavan' in scenerio.lower():
            scenerios.remove(scenerio)
            
    return path_to_sky_control_data, scenerios


def get_to_SkyControl_server(path: str):
    '''
    get the path to srver data 
    '''
    main_folder_list: list[str] = next(os.walk(path))[1]
    for folder_name in main_folder_list:
        if 'server' in folder_name.lower():
            return f"{path}/{folder_name}"
    raise FileExistsError('There is no server, be sure u have selected the right file')


def get_all_pathes(path: str, scenarios: list):
    pathes_to_clients_data = []
    pathes_to_tracking_groups_data = []

    for scenario in scenarios:
        scenario_folders_list = next(os.walk(f"{path}/{scenario}"))[1]
        for folder_name in scenario_folders_list:
            if "client" in folder_name.lower():
                pathes_to_clients_data.append(f"{path}/{scenario}/{folder_name}")
            if "group" in folder_name.lower():
                pathes_to_tracking_groups_data.append(f"{path}/{scenario}/{folder_name}")

    return pathes_to_clients_data, pathes_to_tracking_groups_data


def get_clients_data(path_to_clients_data: str):
    clients_list = next(os.walk(path_to_clients_data))[2]
    clients_json_pathes, clients_csv_pathes, clients_data  = [], [], []

    for client in clients_list:
        if 'json' in client.lower():
            clients_json_pathes.append(f'{path_to_clients_data}/{client}')
        if 'csv' in client.lower():
            clients_csv_pathes.append(f'{path_to_clients_data}/{client}')

    for i in range(len(clients_csv_pathes)): # This for loop create every object of clients stations.
        with open(clients_json_pathes[i], 'r', encoding='utf-8') as file:  # Both lists have the same length
            json_data = json.load(file)
        
        client_type = json_data['ClientType']
        client_location = json_data['Location']
        client_name = json_data['Name']
        client_df = pd.read_csv(clients_csv_pathes[i], on_bad_lines='skip')

        client_data = StationClient(df=client_df[client_df['Validity'] == True], type=client_type, name=client_name, location=client_location)
        if client_data.is_data:
            clients_data.append(client_data)

    return clients_data


def get_groups_data(path_to_tracking_groups_data: str):
    groups_list = next(os.walk(path_to_tracking_groups_data))[2]
    groups_json_pathes, groups_csv_pathes, groups_data  = [], [], []

    for group in groups_list:
        if group[0] == '.':
            group = group[1::]
        if 'json' in group.lower():
            groups_json_pathes.append(f'{path_to_tracking_groups_data}/{group}')
        if 'csv' in group.lower():
            groups_csv_pathes.append(f'{path_to_tracking_groups_data}/{group}')

    for i in range(len(groups_csv_pathes)): # This for loop create every object of clients stations.        
        group_name = groups_csv_pathes[i].split('/')[-1][0:-5]
        group_df = pd.read_csv(groups_csv_pathes[i], on_bad_lines='skip')

        group_data = GroupStation(df=group_df[group_df['IsTracked'] == True], name=group_name)
        
        if group_data.is_data:
            group_data.filter_by_velocity()
            group_data.filter_junk_points()

        if group_data.is_data:
            groups_data.append(group_data)

    return groups_data

def set_valids():
    pass

