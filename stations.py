import numpy as np
import pandas as pd

class StationClient:
    def __init__(self, df: pd.DataFrame, type: str, name: str, location: dict):
        self.df = df
        self.type = type
        self.name = name
        self.easting = location['Easting']
        self.northing = location['Northing']
        self.height = location['Height']
        self.is_data = False
        if df.shape[0] > 70:
            self.time = df['Computer_Time'].to_list()
            self.azimuth = df['Target Azimuth'].to_numpy()
            self.elevation = df['Target Elevation'].to_numpy()
            self.is_data = True
            self.set_real_time()

    def set_real_time(self):  # the time is in a format of hours:minuts:seconds - the function return it in seconds from zero
        real_time = np.zeros(len(self.time))
        for i, time_str in enumerate(self.time):
            try:
                hours, minutes, seconds = map(float, time_str.split(':'))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                real_time[i] = total_seconds
            except:
                minutes, seconds = map(float, time_str.split(':'))
                total_seconds = minutes * 60 + seconds
                real_time[i] = total_seconds
        self.time = real_time
    
    def get_time(self):
        return self.time


class GroupStation:
    def __init__(self, df, name):
        self.df = df
        self.name = name
        self.is_data = False
        if df.shape[0] > 150:
            self.E = self.df['Target Easting'].to_numpy()
            self.N = self.df['Target Northing'].to_numpy()
            self.alt = self.df['Target Height'].to_numpy()
            self.time = self.df['Computer_Time'].tolist()
            self.time_no_split = self.df['Computer_Time'].tolist()
            self.time_in_seconds = []
            self.time_temp = []
            self.azimuth = []
            self.elevation = []
            self.is_data = True
            self.set_real_time()

    def set_real_time(self):  # the time is in a format of hours:minutes:seconds - the function return it in seconds
        real_time = np.zeros(len(self.time))
        for i, time_str in enumerate(self.time):
            try:
                hours, minutes, seconds = map(float, time_str.split(':'))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                real_time[i] = total_seconds
            except:
                print("מקרה קיצון לא תקין")
                minutes, seconds = map(float, time_str.split(':'))
                total_seconds = 6 * 3600 + minutes * 60 + seconds
                real_time[i] = total_seconds
        self.time = real_time

    def get_time(self):
        return self.time

    def filter_junk_points(self): # Filter unrelevant points by distance
        indexes = []
        for i in range(len(self.alt)):
            if i < len(self.alt) - 2:
                if self.alt[i] != self.alt[i + 1] and abs(self.alt[i] - self.alt[i + 1]) < 400 and \
                        abs(self.E[i] - self.E[i + 1]) < 400:
                    indexes.append(i)

        if len(indexes) < 150:
            self.is_data = False
            return

        # easting, northing, altitude, time = [np.zeros(len(indexes))] * 4

        easting = np.array([self.E.copy()[i] for i in indexes])
        northing = np.array([self.N.copy()[i] for i in indexes])
        altitude = np.array([self.alt.copy()[i] for i in indexes])
        time = np.array([self.time.copy()[i] for i in indexes])

        self.E, self.N, self.alt, self.time = easting, northing, altitude, time

    def filter_by_velocity(self): # Filter unrelevant points by velocity
        indexes = []
        for i in range(len(self.alt)):
            if i < len(self.alt) - 2:
                v = np.linalg.norm([self.E[i] - self.E[i + 1],
                                    self.N[i] - self.N[i + 1],
                                    self.alt[i] - self.alt[i + 1]])
                v /= abs(self.time[i] - self.time[i + 1])
                if v > 30:
                    indexes.append(i)

        if len(indexes) < 150:
            self.is_data = False
            return

        self.E = [self.E.copy()[i] for i in indexes]
        self.N = [self.N.copy()[i] for i in indexes]
        self.alt = [self.alt.copy()[i] for i in indexes]
        self.time = [self.time.copy()[i] for i in indexes]

    def az_el_projection(self, station_position):

        delta_e = self.E - station_position[0]
        delta_n = self.N - station_position[1]
        delta_alt = self.alt - station_position[2]
        r = np.sqrt(delta_e ** 2 + delta_alt ** 2 + delta_n ** 2)

        elevation = np.zeros(len(self.alt))
        azimuth = np.zeros(len(self.alt))
        for i in range(len(self.alt)):
            elevation[i] = 180 / np.pi * np.arcsin(delta_alt[i] / r[i])
            if (delta_n[i] < 0) & (delta_e[i] < 0):
                azimuth[i] = np.mod(180 + 180 / np.pi * np.arctan(delta_e[i] / (delta_n[i])), 360)
            else:
                azimuth[i] = np.mod(180 / np.pi * np.arctan(delta_e[i] / (delta_n[i])), 360)
            if azimuth[i] < 180:
                azimuth[i] += 360

        self.azimuth, self.elevation = azimuth, elevation

    def filter_junk_ele_azi(self):
        self.time_temp = self.time
        filtered_time = []
        filtered_ele = []
        indexes = []

        for i in range(len(self.elevation)):
            if i < len(self.elevation) - 2:
                if self.elevation[i] != self.elevation[i + 1]:
                    if abs(self.elevation[i] - self.elevation[i + 1]) < 3:
                        filtered_time.append(self.time_temp[i])
                        filtered_ele.append(self.elevation[i])
                        indexes.append(i)

        self.time_in_seconds = [t for t in filtered_time]
        self.elevation = filtered_ele

        self.azimuth = [self.azimuth.copy()[i] for i in indexes]
