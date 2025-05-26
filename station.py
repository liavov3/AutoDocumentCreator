import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

class Station:
    def __init__(self, df, station):
        self.df = df
        self.station = station
        self.time = df['ComputerTime'].to_numpy()
        self.time_in_seconds = []
        self.time_temp = []
        self.is_data = True

        if df.empty:
            self.is_data = False
        else:
            if station == 'karnatz':
                    self.azimuth = df['TargetAzimuth'].to_numpy()
                    self.elevation = df['TargetElevation'].to_numpy()
                    self.easting = df['Easting'].to_numpy()[1]
                    self.northing = df['Northing'].to_numpy()[1]
                    self.height = df['Height'].to_numpy()[1]
                    self.fovH = df['FovH'].to_numpy()
                    self.fovV = df['FovV'].to_numpy()
            else:
                self.azimuth = []
                self.elevation = []
                self.easting = df['Target.Easting'].to_numpy()
                self.northing = df['Target.Northing'].to_numpy()
                self.height = df['Target.Height'].to_numpy()

    def get_real_time(self): #the time is in a format of hours:minuts:seconds - the function return it in seconds from zero
        real_time = np.zeros(len(self.time))
        for i, time_str in enumerate(self.time):
            hours, minutes, seconds = map(float, time_str.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            real_time[i] = total_seconds
        self.time_in_seconds, self.time_temp = [real_time] * 2
        return real_time

    def az_el_projection(self, station_position):
        easting = self.easting
        northing = self.northing
        altitude = self.height

        delta_e = easting - station_position[0]
        delta_n = northing - station_position[1]
        delta_alt = altitude - station_position[2]
        r = np.sqrt(delta_e ** 2 + delta_alt ** 2 + delta_n ** 2)

        elevation = np.zeros(len(easting))
        azimuth = np.zeros(len(easting))
        for i in range(len(easting)):
            elevation[i] = 180 / np.pi * np.arcsin(delta_alt[i] / r[i])
            if (delta_n[i] < 0) & (delta_e[i] < 0):
                azimuth[i] = np.mod(180 + 180 / np.pi * np.arctan(delta_e[i] / (delta_n[i])), 360)
            else:
                azimuth[i] = np.mod(180 / np.pi * np.arctan(delta_e[i] / (delta_n[i])), 360)
            if azimuth[i] < 180:
                azimuth[i] += 360

        self.azimuth, self.elevation = azimuth, elevation

    def filter_junk_ele_azi(self):
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

class StationKarnatz:
    def __init__(self, df, name):
        self.df = df
        self.name = name
        if df.empty:
            self.is_data = False
        else:
            self.time = df['ComputerTime'].to_list()
            self.azimuth = df['TargetAzimuth'].to_numpy()
            self.elevation = df['TargetElevation'].to_numpy()
            self.easting = df['Easting'].to_numpy()[1]
            self.northing = df['Northing'].to_numpy()[1]
            self.height = df['Height'].to_numpy()[1]
            self.is_data = True

    def get_real_time(self):  # the time is in a format of hours:minuts:seconds - the function return it in seconds from zero
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
        return real_time
