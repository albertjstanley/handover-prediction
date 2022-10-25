from handover.data import AccessPoint, AccessPointManager
import numpy as np


class AccessPointSelector:
    """
    Holds logic for choosing between different AccessPoints
    """

    def predict_future_quality(self, access_point: AccessPoint, current_timestamp: int, name="rsrq", threshold=-18):
        # predicts the quality of the access point in the next time step
        # Select which column we are using for prediction
        if name == "rsrp":
            extractor = lambda x: x.rsrp
        elif name == "rsrq":
            extractor = lambda x: x.rsrq
        else: 
            raise ValueError(f"Invalid AccessPoint property: {name}")

        # Grab the values in the last five data points
        timestamps = []
        values = []
        for timestamp in access_point.timestamps[-5:]:
            data = access_point.timestamp_to_data[timestamp]
            timestamps.append(timestamp)
            values.append(extractor(data))

        # If not enough data just predict last observed value
        if len(values) == 1:
            return values[0], None

        # Compute average slope
        # If len(values) != len(timestamps), chance to get divide by 0 error
        # We avoid that situation here
        if(len(np.unique(np.array(timestamps))) != len(np.array(values))):
            gradients = np.gradient(np.array(values))
        else:
            gradients = np.gradient(np.array(values), np.array(timestamps))
        avg_gradient = np.mean(gradients)
        predicted_future_quality = values[-1] + (timestamps[-1] - current_timestamp) * avg_gradient
        if(avg_gradient >= 0):
            time_until_threshold = None
        else:
            time_until_threshold = ((threshold - values[-1]) / avg_gradient)
        return (predicted_future_quality, time_until_threshold)

    def choose(self, access_points, current_timestamp):
        best_access_point = None
        best_access_point_time_to_drop = None
        best_value = -100000
        scores = []

        for access_point in access_points: 
            (quality, time_until_threshold) = self.predict_future_quality(access_point, current_timestamp)
            print("Pci: ", access_point.pci, " - Predicted RSRQ: ", quality)
            if quality > best_value: 
                best_value = quality
                best_access_point = access_point
                best_access_point_time_to_drop = time_until_threshold

            scores.append(quality)
        # TODO: log or print score here
        
        return best_access_point, best_access_point_time_to_drop

