from handover.selector import AccessPointManager, AccessPointSelector
from handover.data import AccessPointData
import pandas as pd

class Simulator:
    """
    Handles reading csv file and calling selector after each timestep
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.cur_timestamp = None
        self.ap_manager = AccessPointManager()
        self.ap_selector = AccessPointSelector()
        self.timetamp_to_registered_pci = {}

    def _evaluate_last_timestep(self, access_points):
        registered_pci = self.timetamp_to_registered_pci[self.cur_timestamp]
        chosen = self.ap_selector.choose(access_points)
        
        print(f"Currently Registered: {registered_pci}")
        print(f"Choices: {access_points}")
        print(f"Chosen: {chosen.pci}")
        print("______________________")

    def run(self):
        """
        Entry point for running predictor on csv file.
        """
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
        # load the data from the csv path
        df = pd.read_csv(self.csv_path)
        df = df.drop_duplicates()
        df = df[df['mPci'] > 0]
        df = df.sort_values(by=['mTimeStamp'])
        return df