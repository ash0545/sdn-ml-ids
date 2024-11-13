# Ryu Controller

This section provides the details for the Ryu Controller used for collecting the dataset, as well as usage instructions. A (legacy) [partially working IDS](./IDS/) is also provided in its correspondingly named subdirectory.

## Table of Contents

- [Ryu Controller](#ryu-controller)
  - [Table of Contents](#table-of-contents)
  - [Collector Controller](#collector-controller)
  - [`ofctl_rest` Endpoints Accessed](#ofctl_rest-endpoints-accessed)
  - [Usage Instructions](#usage-instructions)

## Collector Controller

The controller used for collection of the dataset is a modification of the SimpleMonitor13 application provided by the Ryu Framework as a sample application. This inherits from SimpleSwitch13 (another sample application), which was [modified to make it a layer 3 switch](https://github.com/knetsolutions/learn-sdn-with-ryu/blob/master/ryu_part3.md).

The 2 key methods within the SimpleMonitor13 class are:

1. `get_ofctl_combined_stats`: sends requests to the `ofctl_rest` API's endpoints, matches and combines the data of a particular flow and returnes the 27 combined features.
2. `_monitor`: calls the `get_ofctl_combined_stats` method and writes the retrieved content to a CSV file, every second.

## `ofctl_rest` Endpoints Accessed

Three endpoints of the `ofctl_rest` API were accessed, and the results combined, for collecting the 27 features present in our dataset. They are:

- **_/stats/flow/id_ (Flow Statistics)**: Captures data on each network flow, including source and destination IP addresses, packet counts, byte counts, and flow duration. These attributes help in identifying anomalies in traffic patterns, such as unusual packet volumes or flows directed toward particular IPs, which are often indicative of Distributed Denial of Service (DDoS) attacks.
- **_/stats/port/id_ (Port Statistics)**: Provides information on packet counts and bytes transmitted and received per port, along with error counts. Attack patterns, such as port scanning or excessive packet drops, may generate distinct port statistics that are valuable for classification.
- **_/stats/table/id_ (Table Statistics)**: Gives data on table lookups and matches, offering insights into how frequently certain routing paths are utilized. High lookup rates and mismatches may signal unusual routing activities or attempts to exploit the controller’s decision-making processes.

## Usage Instructions

1. Run the Ryu controller Python file in conjunction with the `ofctl_rest` application through ryu-manager: `ryu-manager <file.py> ryu.app.ofctl_rest`
2. Setup your topology, ensuring it is properly configured to use your controller.
3. Once flows start being generated in the topology, the controller will create a new file within the same directory, and start appending flows to it.
4. After collecting the required amount of flows, the controller can be stopped, and the CSV file renamed to whichever flow you have collected.

> [!WARNING]
> Be sure to rename / move the generated CSV file after collection of a particular kind of traffic. If not done, the controller will continue to append flows to the same file.
