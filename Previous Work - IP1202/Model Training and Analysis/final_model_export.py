import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
import pickle

DATASET_PATH = "../Dataset/Collected Dataset"

# flow data
flow_files = {
    "attack": [
        "icmp_ddos_flood.csv",
        "land_attack.csv",
        "malformed_packets.csv",
        "nestea_attack.csv",
        "nmap_probe_attack.csv",
        "ping_of_death_attack.csv",
        "tcp_ddos_flood.csv",
        "udp_ddos_flood.csv",
    ],
    "normal": ["normal_iperf.csv", "normal_w3m.csv"],
}

dfs = []

for attack_type, files in flow_files.items():
    for file in files:
        try:
            data = pd.read_csv(DATASET_PATH + file)
            data["type"] = attack_type
            dfs.append(data)
        except FileNotFoundError:
            print("Error: File " + file + " not found. Skipping...")

# Concatenate all DataFrames
combined_data = pd.concat(dfs, ignore_index=True)
print("Successfully combined data into a single DataFrame!")

# Randomize data, remove previous indices
combined = combined_data.sample(frac=1).reset_index().drop("index", axis=1)

# Extracting relevant features
combined["ip_bytes_sec"] = combined["ip_bytes"] / combined["ip_duration"]
combined["ip_packets_sec"] = combined["ip_packet"] / combined["ip_duration"]
combined["ip_bytes_packet"] = combined["ip_bytes"] / combined["ip_packet"]
combined["port_bytes_sec"] = combined["port_bytes"] / combined["ip_duration"]
combined["port_packet_sec"] = combined["port_packet"] / combined["ip_duration"]
combined["port_byte_packet"] = combined["port_bytes"] / combined["port_packet"]
combined["port_flow_count_sec"] = combined["port_flow_count"] / combined["ip_duration"]
combined["table_matched_lookup"] = (
    combined["table_matched_count"] / combined["table_lookup_count"]
)
combined["table_active_lookup"] = (
    combined["table_active_count"] / combined["table_lookup_count"]
)
combined["port_rx_packets_sec"] = (
    combined["port_rx_packets"] / combined["port_duration_sec"]
)
combined["port_tx_packets_sec"] = (
    combined["port_tx_packets"] / combined["port_duration_sec"]
)
combined["port_rx_bytes_sec"] = (
    combined["port_rx_bytes"] / combined["port_duration_sec"]
)
combined["port_tx_bytes_sec"] = (
    combined["port_tx_bytes"] / combined["port_duration_sec"]
)

# Removing identifying features
features = combined[
    [
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
        "type",
    ]
].copy()

# Removing inf and NaN values
features.replace([np.inf, -np.inf], np.nan, inplace=True)
features.dropna(inplace=True)
features.describe()

# Splitting into dependent and independent variables
X = features.loc[:, features.columns != "type"]
y = features["type"]

# Splitting into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)

# Scaling data using RS
X_train = pd.DataFrame(
    RobustScaler().fit_transform(X_train),
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

X_test = pd.DataFrame(
    RobustScaler().fit_transform(X_test),
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

from sklearn.decomposition import PCA

pca = PCA(n_components=5)
X_train2 = pd.DataFrame(pca.fit_transform(X_train))

rf = RandomForestClassifier()
rf.fit(X_train2, y_train)

X_test2 = pd.DataFrame(pca.transform(X_test))
y_pred = rf.predict(X_test2)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

filename = "test_model.sav"
pickle.dump(rf, open(filename, "wb"), protocol=2)
filename = "test_pca.sav"
pickle.dump(pca, open(filename, "wb"), protocol=2)
