from netCDF4 import Dataset
import numpy as np

def getRain():
    rainc = dataset["RAINC"][:]
    rainnc = dataset["RAINNC"][:]
    return rainc + rainnc

def getRainWithinAnInterval(rain, interval):
    return np.array([rain[t] - rain[t - interval] for t in range(len(rain)-1, 0, -interval)])

if __name__ == "__main__":
    ncfile = "C:/Users/carolvfs/Box/WRF_Carolina/NHAZ_2023/R000/wrfout_d03_2011-01-10_00_00_00"
    dataset = Dataset(ncfile)

    rain = getRain()
    interval = 72
    acc_rain = getRainWithinAnInterval(rain, interval)