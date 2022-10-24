class AccessPointManager: 
    # Ensures we don't have duplicate AccessPoints
    def __init__(self):
        self.pci_to_access_point = {}

    def get_access_point(self, pci):
        if pci in self.pci_to_access_point: 
            return self.pci_to_access_point[pci]
        new_ap = AccessPoint(pci)
        self.pci_to_access_point[pci] = new_ap
        return new_ap

class AccessPoint: 
    def __init__(self, pci):
        self.timestamps = []
        self.timestamp_to_data = {}
        self.pci = pci
    
    def add_data(self, timestamp, data):
        self.timestamps.append(timestamp)
        self.timestamp_to_data[timestamp] = data

    def predict_future_data(self):
        return 

    def __repr__(self):
        return f"<AccessPoint {self.pci}>"


class AccessPointSelector: 
    def choose(access_points):
        for ap in access_points: 
            pass

