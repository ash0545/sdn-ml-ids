# SDN Emulation and Development of Dataset for ML-Based Intrusion Detection

Project work done for the **IP1302** course of our 5th Semester.

**Reference Paper**: [MCAD: A Machine Learning Based Cyberattacks Detector in Software-Defined Networking (SDN) for Healthcare Systems](https://ieeexplore.ieee.org/document/10101795) <sup>[[1]](#references)</sup>

## Team Members

- Ashwin Santhosh (CS22B1005, GitHub: [ash0545](https://www.github.com/ash0545))
- Aswin Valsaraj (CS22B1006, GitHub: [aswinn03](https://www.github.com/aswinn03))
- Kaustub Pavagada (CS22B1042, GitHub: [Kaustub26Pvgda](https://www.github.com/Kaustub26Pvgda))

## Table of Contents

- [SDN Emulation and Development of Dataset for ML-Based Intrusion Detection](#sdn-emulation-and-development-of-dataset-for-ml-based-intrusion-detection)
  - [Team Members](#team-members)
  - [Table of Contents](#table-of-contents)
  - [Aim](#aim)
  - [Tools / Libraries Used](#tools--libraries-used)
    - [Topology Creation](#topology-creation)
    - [Attack Traffic Generation](#attack-traffic-generation)
    - [Normal Traffic Generation](#normal-traffic-generation)
  - [Proposed Model](#proposed-model)
  - [Implementation](#implementation)
  - [Results](#results)
    - [Collected Dataset](#collected-dataset)
    - [Model Training \& Analysis](#model-training--analysis)
  - [Future Work](#future-work)
  - [Citation](#citation)
  - [References](#references)

## Aim

  Our overall goal was to delve into the creation of complex Software Defined Network (SDN) topologies - through the use of the Ryu SDN Framework, Mininet and VirtualBox Virtual Machines (VMs) - and the collection of flow statistics through Ryu's inbuilt Application Programming Interface (API) - `ofctl_rest`. Through this, we simulated various attack and normal traffic flows within our emulated network to make a dataset, which was used to train and compare Machine Learning (ML) models for an ML-based Intrusion Detection System (IDS).
  
  In short: **To strengthen security in SDNs by creating a dataset and comparing ML models for an ML-based IDS present within the controller.**
  
![image](https://github.com/user-attachments/assets/f9748d0a-cabd-4271-8e29-752d2fdb03f1)

## Tools / Libraries Used

### Topology Creation

- [Ryu SDN Framework](https://ryu-sdn.org/): for the control plane of our simulated network
- [Mininet](http://mininet.org/): creation of virtual network within a VM
- [Oracle VM VirtualBox](https://www.virtualbox.org/): creation and management of VMs
  - [Ubuntu 18.04.6 LTS](https://releases.ubuntu.com/18.04.6/): hosting the Ryu controller, with all traffic flow passing through it
  - [Kali](https://www.kali.org/get-kali/#kali-virtual-machines): intruder machine
  - [Metasploitable 2](https://sourceforge.net/projects/metasploitable/files/Metasploitable2/): victim machine
- [Wireshark](https://www.wireshark.org/): to verify functionality of topology

### Attack Traffic Generation

- [Scapy](https://scapy.net/): packet manipulation python library for simulating attacks
- [Nmap](https://nmap.org/): network discovery tool, to simulate a probe attack
- [Selenium](https://selenium-python.readthedocs.io/installation.html): browser automation for simulating web attacks

### Normal Traffic Generation

- [w3m](https://w3m.sourceforge.net/): text-based web browser for use in terminals, to simulate normal traffic flow
- [iPerf](https://iperf.fr/): for network performance measurement, to simulate normal traffic flow
- [Distributed Internet Traffic Generator (D-ITG)](https://traffic.comics.unina.it/software/ITG/documentation.php): to generate Telnet and Domain Name Server (DNS) traffic

## Proposed Model

![image](https://github.com/user-attachments/assets/9d113424-39fd-4479-a5cb-6365b7c30026)

## Implementation

The project can be divided into 4 major sections: proposing a network topology, data gathering, data processing and training / analysis of ML / DL models. The details and files for implementing each section can be found in their respective subdirectories:

1. [Network Topology](/Network%20Topology/)
   - Creating the Topology in VirtualBox
   - Configuring the Ubuntu VM and Mininet
   - Connecting a Mininet host to the internet
   - Connecting the Kali and Metasploitable VMs - Linux Routing through the Ubuntu VM
   - Configuring the Kali and Metasploitable VMs
2. [Dataset Collection](/Dataset%20Collection/)
   - Ryu Controller
   - Attack traffic generation (11 unique attacks)
     - Distributed Denial of Service (DDoS)
     - Probe Attack
     - Web Attacks
     - Remote-to-Local (R2L)
     - User-to-Root (U2R)
   - Normal traffic generation (5 unique types)
     - iPerf
     - Internet
     - Ping
     - Telnet
     - DNS
   - Collected Dataset
3. [Data Processing](/Data%20Processing/)
   - Preprocessing
     - Cleansing / Shuffling
     - Division Transformation
   - Feature Selection
     - Benjamini–Hochberg False Discovery Rate (FDR)<sup>[[3]](#references)</sup>
     - Stepwise Selection<sup>[[8]](#references)</sup>
     - Boruta<sup>[[6]](#references)</sup>
   - Scaling
   - Dimensionality Reduction
     - Principal Component Analysis (PCA)
     - Linear Discriminant Analysis (LDA)
     - Independent Component Analysis (ICA)
4. [Model Training & Analysis](/Model%20Training%20&%20Analysis/)
   - ML models comparison
   - DL model performance evaluation

## Results

### Collected Dataset

A total of roughly 291k attack flows (spread over 11 classes) and 122k normal flows (spread over 5 classes) were collected as CSV files through the `ofctl_rest` API. This was done by pinging the API endpoints every second while the respective type of flow was being generated.

| Attack Flow Counts                                                                                | Normal Flow Counts                                                                                |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| ![Attack counts](https://github.com/user-attachments/assets/d50813a0-b5ab-4293-b038-34cfa202ac50) | ![Normal counts](https://github.com/user-attachments/assets/bd015221-290b-47a5-86da-07d4484cf748) |

The data is comprised of 27 features collected from 3 of `ofctl_rest`'s endpoints.

<details>

<summary> The 27 collected features (click to expand) </summary>

| No. | Feature name        |
| --- | ------------------- |
| 1   | src                 |
| 2   | dst                 |
| 3   | table_id            |
| 4   | ip_bytes            |
| 5   | ip_packet           |
| 6   | ip_duration         |
| 7   | in_port             |
| 8   | dl_dst              |
| 9   | port_bytes          |
| 10  | port_packet         |
| 11  | port_flow_count     |
| 12  | table_active_count  |
| 13  | table_lookup_count  |
| 14  | table_matched_count |
| 15  | port_rx_packets     |
| 16  | port_tx_packets     |
| 17  | port_rx_bytes       |
| 18  | port_tx_bytes       |
| 19  | port_rx_dropped     |
| 20  | port_tx_dropped     |
| 21  | port_rx_errors      |
| 22  | port_tx_errors      |
| 23  | port_rx_frame_err   |
| 24  | port_rx_over_err    |
| 25  | port_rx_crc_err     |
| 26  | port_collisions     |
| 27  | port_duration_sec   |

</details>

### Model Training & Analysis

We selected an ML model by performing a comprehensive comparison between 6 unique models using multiple evaluation metrics **before performing dimensionality reduction** on the dataset. The models compared were:

- **K-Nearest Neighbors (KNN)**: a simple, instance-based learning algorithm;
- **Support Vector Machine (SVM)**: a powerful classifier that works by finding the optimal hyperplane for separation;
- **Logistic Regression (LR)**: a probabilistic model used for binary classification
- **Decision Tree (DT)**: a model that splits data into homogenous subsets based on feature values;
- **Naive Bayes (NB)**: a probabilistic classifier based on Bayes' theorem with strong independence assumptions;
- **Random Forest (RF)**: an ensemble of decision trees that improves accuracy by averaging multiple models.

<details>

<summary> Comparison of ML models (click to expand) </summary>

![ml_models](https://github.com/user-attachments/assets/56a9fec9-b929-4f16-a577-91d13acbae43)

</details>

RF was chosen over DT as RF demonstrates improved robustness and generalization by combining multiple decision trees, reducing the risk of overfitting. RF achieves 100% accuracy across all attack classes, making it highly reliable for our IDS.

The PCA, LDA and ICA dimensionality reduction techniques were then compared using the RF model.

<details>

<summary> Comparison of Dimensionality Reduction techniques (click to expand) </summary>

![rf_dim_red](https://github.com/user-attachments/assets/63ab75d8-b090-40d6-b55c-8ed5021e49a5)

</details>

To achieve similar results without an extensive pre-processing pipeline, the Feed Forward Neural Network DL model was evaluated. Running the model directly on the dataset's transformed features achieved an accuracy of ~98.7%, with other metrics in a similar range. Performance dropped significantly when the dataset was reduced through feature selection and dimensionality reduction, suggesting that this approach is more suitable for larger datasets.

<details>

<summary> Effect of Dimensionality Reduction techniques on FFNN (click to expand) </summary>

![ffnn_dim_red](https://github.com/user-attachments/assets/5a38afb9-91a0-4dbc-a680-ecda12030d16)

</details>

## Future Work

- Implementation of a _functional_ IDS and Intrusion Prevention System (IPS)

> [!NOTE]
> A legacy (partially working) IDS is provided in the [Ryu Controller subdirectory](/Dataset%20Collection/), It utilizes an RF model trained with an RS PCA preprocessing pipeline. Predictions are a hit or miss.

- Test out more DL models

## Citation

If you use this code for your research, please cite

```bibtex
@article{vadivu2025sdn,
  author    = {Vadivu, D.S. and Santhosh, A. and Rajagopalan, N. and Pavagada, K. and Valsaraj, A.},
  title     = {Enhancing SDN Traffic Analysis Through Machine Learning on Preprocessed Controller Flow Statistics and Packet Analysis Data},
  journal   = {SN Computer Science},
  volume    = {6},
  number    = {412},
  year      = {2025},
  doi       = {10.1007/s42979-025-03930-5}
}
```

## References

[1] Alhilo, A. M. J., & Koyuncu, H. (2024). Enhancing SDN Anomaly Detection: A Hybrid Deep Learning Model with SCA-TSO Optimization. International Journal of Advanced Computer Science and Applications (IJACSA), 15(5).

[2] Alzahrani, A. O., & Alenazi, M. J. F. (2023). ML-IDSDN: Machine learning based intrusion detection system for software-defined network. Concurrency and Computation: Practice and Experience, 35(1), 1–12.

[3] Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. Journal of the Royal Statistical Society: Series B (Methodological), 57, 289–300.

[4] Erfan, A. (2022). DDoS attack detection scheme using hybrid ensemble learning and GA algorithm for Internet of Things. PalArch’s Journal of Archaeology of Egypt/Egyptology, 18(18), 521–546.

[5] Halman, L., & Alenazi, M. (2023). MCAD: A Machine Learning Based Cyberattacks Detector in Software-Defined Networking (SDN) for Healthcare Systems. IEEE Access, 1–1.

[6] Kursa, M. B., & Rudnicki, W. R. (2010). Feature Selection with the Boruta Package. Journal of Statistical Software, 36, 1–13.

[7] Maddu, M., & Rao, Y. N. (2023). Network intrusion detection and mitigation in SDN using deep learning models. International Journal of Information Security, 1–14.

[8] Naser, M. (2021). Mapping functions: A physics-guided, data-driven and algorithm-agnostic machine learning approach to discover causal and descriptive expressions of engineering phenomena. Measurement, 185, 110098.

[9] Reddy, K. V. A., Ambati, S. R., Reddy, Y. S. R., & Reddy, A. N. (2021). AdaBoost for Parkinson’s disease detection using robust scaler and SFS from acoustic features. In Proceedings of the Smart Technologies, Communication and Robotics (STCR), 1–6.
