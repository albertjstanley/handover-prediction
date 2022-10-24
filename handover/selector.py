from handover.data import AccessPoint, AccessPointManager
import numpy as np


class AccessPointSelector:
    """
    Holds logic for choosing between different AccessPoints
    """

    def predict_future_quality(self, access_point: AccessPoint, name="rsrq"):
        # predicts the quality of the access point in the next time step
        
        # Select which column we are using for prediction
        if name == "rsrp":
            extractor = lambda x: x.rsrp
        elif name == "rsrq":
            extractor = lambda x: x.rsrq
        else: 
            raise ValueError(f"Invalid AccessPoint property: {name}")

        # Grab the values in the last five data points
        values = []
        for timestamp in access_point.timestamps[-5:]:
            data = access_point.timestamp_to_data[timestamp]
            values.append(extractor(data))

        # If not enough data just predict last observed value
        if len(values) == 1:
            return values[0]

        # Compute average slope
        gradients = np.gradient(np.array(values))
        avg_gradient = np.mean(gradients)
        predicted_future_quality = values[-1] + avg_gradient

        return predicted_future_quality

    def choose(self, access_points):
        best_access_point = None
        min_value = -100000
        scores = []

        for access_point in access_points: 
            quality = self.predict_future_quality(access_point)
            if quality > min_value: 
                best_access_point = access_point

            scores.append(quality)

        # TODO: log or print score here
        
        return best_access_point

