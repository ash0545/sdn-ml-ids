import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
import pickle


class MachineLearningAlgo:
    def __init__(self):
        model_filename = "test_model.sav"
        self.model = pickle.load(open(model_filename, "rb"))
        print("Using model from ", model_filename)

        pca_filename = "test_pca.sav"
        self.pca = pickle.load(open(pca_filename, "rb"))
        print("Using PCA object from ", pca_filename)

    def preprocess_flow_data(self, flow_data):
        ip_bytes_sec = flow_data[3] / flow_data[5] if flow_data[5] != 0 else np.nan
        ip_packets_sec = flow_data[4] / flow_data[5] if flow_data[5] != 0 else np.nan
        ip_bytes_packet = flow_data[3] / flow_data[4] if flow_data[4] != 0 else np.nan
        port_bytes_sec = flow_data[7] / flow_data[5] if flow_data[5] != 0 else np.nan
        port_packet_sec = flow_data[8] / flow_data[5] if flow_data[5] != 0 else np.nan
        port_byte_packet = flow_data[7] / flow_data[8] if flow_data[8] != 0 else np.nan
        port_flow_count_sec = (
            flow_data[9] / flow_data[5] if flow_data[5] != 0 else np.nan
        )
        table_matched_lookup = (
            flow_data[12] / flow_data[11] if flow_data[11] != 0 else np.nan
        )
        table_active_lookup = (
            flow_data[10] / flow_data[11] if flow_data[11] != 0 else np.nan
        )
        port_rx_packets_sec = (
            flow_data[13] / flow_data[25] if flow_data[25] != 0 else np.nan
        )
        port_tx_packets_sec = (
            flow_data[14] / flow_data[25] if flow_data[25] != 0 else np.nan
        )
        port_rx_bytes_sec = (
            flow_data[15] / flow_data[25] if flow_data[25] != 0 else np.nan
        )
        port_tx_bytes_sec = (
            flow_data[16] / flow_data[25] if flow_data[25] != 0 else np.nan
        )
        dataframe = pd.Series(
            [
                ip_bytes_sec,  # 1 ip_bytes_sec
                ip_packets_sec,  # 2 ip_packets_sec
                ip_bytes_packet,  # 3 ip_bytes_packet
                port_bytes_sec,  # 4 port_bytes_sec
                port_packet_sec,  # 5 port_packet_sec
                port_byte_packet,  # 6 port_byte_packet
                port_flow_count_sec,  # 7 port_flow_count_sec
                table_matched_lookup,  # 8 table_matched_lookup
                table_active_lookup,  # 9 table_active_lookup
                port_rx_packets_sec,  # 10 port_rx_packets_sec
                port_tx_packets_sec,  # 11 port_tx_packets_sec
                port_rx_bytes_sec,  # 12 port_rx_bytes_sec
                port_tx_bytes_sec,  # 13 port_tx_bytes_sec
            ]
        ).to_frame()
        return dataframe

    def classify(self, flow_data):
        scaler = RobustScaler()
        dataframe = self.preprocess_flow_data(flow_data)
        dataframe = pd.DataFrame(scaler.fit_transform(dataframe))
        dataframe = dataframe.fillna(0)
        final_data = pd.DataFrame(self.pca.transform(dataframe))

        prediction = self.model.predict(final_data)[0]
        return prediction
