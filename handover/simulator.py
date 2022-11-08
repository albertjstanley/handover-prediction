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
        self.prev_chosen_ap = None # AP previously selected
        self.correct_predictions = 0.0
        self.total_predictions = 0.0

    def print_metrics(self):
        print(f"ACCURACY METRICS:")
        print(f"Correctly Predicted: {self.correct_predictions} out of total: {self.total_predictions}")
        print(f"Accuracy: {(self.correct_predictions/self.total_predictions):2.2%}")

    def _evaluate_timestep(self, access_points):
        registered_pci = self.timetamp_to_registered_pci[self.cur_timestamp]

        # Note accuracy if we have prediction from the past step
        if (self.prev_chosen_ap):
            if(registered_pci == self.prev_chosen_ap.pci):
                self.correct_predictions = self.correct_predictions + 1
            self.total_predictions = self.total_predictions + 1

        # Make predictions for the next timestep
        chosen_access_point, time_until_threshold = self.ap_selector.choose(access_points, self.cur_timestamp)
        
        print(f"Currently Registered: {registered_pci}")
        print(f"Choices: {access_points}")
        print(f"Chosen: {chosen_access_point.pci}")
        print(f"Time until Threshold Reached: {time_until_threshold}")
        print("______________________")

        # Setup prev chosen ap for next round
        self.prev_chosen_ap = chosen_access_point

    def run(self):
        """
        Entry point for running predictor on csv file.
        """
        self.df = self.load_data()

        access_points = set()

        for _, row in self.df.iterrows():
            # Keep different timestamp sections in chunks
            if self.cur_timestamp != None and self.cur_timestamp != row.mTimeStamp: 
                self._evaluate_timestep(access_points)
                access_points = set()
            self.cur_timestamp = row.mTimeStamp

            # Set registered pci
            if row.mRegistered == "YES":
                self.timetamp_to_registered_pci[row.mTimeStamp] = row.mPci

            ap = self.ap_manager.get_access_point(row.mPci)
            ap.add_data(row.mTimeStamp, AccessPointData(row.ss, row.rsrp, row.rsrq))
            access_points.add(ap)

        self._evaluate_timestep(access_points)

        self.print_metrics()


    def load_data(self):
        # load the data from the csv path
        df = pd.read_csv(self.csv_path)
        df = df.drop_duplicates()
        df = df[df['mPci'] > 0]
        df = df.sort_values(by=['mTimeStamp'])
        return df