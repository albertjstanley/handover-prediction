from handover.model import AccessPointManager, AccessPointSelector
from handover.data import AccessPointData
import pandas as pd

class Simulator:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.cur_timestamp = None
        self.ap_manager = AccessPointManager()
        self.ap_selector = AccessPointSelector()
        self.timetamp_to_registered_pci = {}

    def _evaluate_last_timestep(self, access_points):
        registered_pci = self.timetamp_to_registered_pci[self.cur_timestamp]
        print(f"Registered: {registered_pci}", access_points)

        self.ap_selector.choose(access_points)
        

    def run(self):
        self.df = self.load_data()

        access_points = set()

        for i, row in self.df.iterrows():
            # Keep different timestamp sections in chunks
            if self.cur_timestamp != None and self.cur_timestamp != row.mTimeStamp: 
                self._evaluate_last_timestep(access_points)
                access_points = set()
            self.cur_timestamp = row.mTimeStamp

            # Set registered pci
            if row.mRegistered == "YES":
                self.timetamp_to_registered_pci[row.mTimeStamp] = row.mPci

            ap = self.ap_manager.get_access_point(row.mPci)
            ap.add_data(row.mTimeStamp, AccessPointData(row.ss, row.rsrp, row.rsrq))
            access_points.add(ap)

        self._evaluate_last_timestep(access_points)


    def load_data(self):
        df = pd.read_csv(self.csv_path)
        df = df.drop_duplicates()
        df = df[df['mPci'] > 0]
        df = df.sort_values(by=['mTimeStamp'])
        return df