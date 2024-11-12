import pandas as pd
import numpy as np
import pickle


class MachineLearningAlgo:

    def __init__(self):
        pca_filename = "pca.sav"
        model_filename = "random_forest.sav"
        scaler_filename = "scaler.sav"

        self.model = pickle.load(open(model_filename, "rb"))
        self.pca = pickle.load(open(pca_filename, "rb"))
        self.scaler = pickle.load(open(scaler_filename, "rb"))

        print("Using RandomForest model from ", model_filename)
        print("Using PCA object from ", pca_filename)
        print("Using RobustScaler object from ", scaler_filename)

    def preprocess_flow_data(self, flow_data):
        print(flow_data)
        for i in range(len(flow_data)):
            if isinstance(flow_data[i], (int, float)):
                flow_data[i] += 1

            ip_bytes_sec = flow_data[3] / flow_data[5]
            ip_packets_sec = flow_data[4] / flow_data[5]
            ip_bytes_packet = flow_data[3] / flow_data[4]
            port_bytes_sec = flow_data[7] / flow_data[5]
            port_packet_sec = flow_data[8] / flow_data[5]
            port_byte_packet = flow_data[7] / flow_data[8]
            port_flow_count_sec = flow_data[9] / flow_data[5]
            table_matched_lookup = flow_data[12] / flow_data[11]
            table_active_lookup = flow_data[10] / flow_data[11]
            port_rx_packets_sec = flow_data[13] / flow_data[25]
            port_tx_packets_sec = flow_data[14] / flow_data[25]
            port_rx_bytes_sec = flow_data[15] / flow_data[25]
            port_tx_bytes_sec = flow_data[16] / flow_data[25]

            data = [
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
            ]

            columns = [
                "ip_bytes_sec",
                "ip_packets_sec",
                "ip_bytes_packet",
                "port_bytes_sec",
                "port_packet_sec",
                "port_byte_packet",
                "port_flow_count_sec",
                "table_matched_lookup",
                "table_active_lookup",
                "port_rx_packets_sec",
                "port_tx_packets_sec",
                "port_rx_bytes_sec",
                "port_tx_bytes_sec",
            ]

        dataframe = pd.DataFrame(data, columns=columns)
        return dataframe

    def classify(self, flow_data):
        dataframe = self.preprocess_flow_data(flow_data)
        dataframe = pd.DataFrame(
            self.scaler.transform(dataframe),
            columns=[
                "ip_bytes_sec",
                "ip_packets_sec",
                "ip_bytes_packet",
                "port_bytes_sec",
                "port_packet_sec",
                "port_byte_packet",
                "port_flow_count_sec",
                "table_matched_lookup",
                "table_active_lookup",
                "port_rx_packets_sec",
                "port_tx_packets_sec",
                "port_rx_bytes_sec",
                "port_tx_bytes_sec",
            ],
        )

        final_data = pd.DataFrame(self.pca.transform(dataframe))
        prediction = self.model.predict(final_data)
        return prediction
