from modified_simple_switch_13 import SimpleSwitch13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import time
import requests
from ml_alg import MachineLearningAlgo


class SimpleMonitor13(SimpleSwitch13):
    def __init__(self, base_url="http://127.0.0.1:8080", *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.ml_obj = MachineLearningAlgo()
        self.base_url = base_url

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info("register datapath: %016x", datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.info("unregister datapath: %016x", datapath.id)
                del self.datapaths[datapath.id]

    def get_stats(self, stat_type, dp_id):
        url = "{0}/stats/{1}/{2}".format(self.base_url, stat_type, dp_id)
        response = requests.get(url)
        if response.status_code == 200:
            stats_dict = response.json()
            stats = []
            for _, stat_list in stats_dict.iteritems():
                stats.extend(stat_list)
            return stats
        else:
            if self.logger:
                self.logger.error(
                    "Failed to retrieve {0} stats: {1} - {2}".format(
                        stat_type, response.status_code, response.text
                    )
                )
            return []

    def get_ofctl_combined_stats(self, dp):
        stat_types = ["flow", "port", "table"]
        stats = dict(
            (stat_type, self.get_stats(stat_type, dp.id)) for stat_type in stat_types
        )
        flow_stats = stats["flow"]
        port_stats = stats["port"]
        table_stats = stats["table"]
        combined_stats = []
        for flow_stat in flow_stats:
            for port_stat in port_stats:
                if "match" in flow_stat and "in_port" in flow_stat["match"]:
                    if flow_stat["match"]["in_port"] == port_stat["port_no"]:
                        table_stat = next(
                            (
                                t
                                for t in table_stats
                                if t["table_id"] == flow_stat["table_id"]
                            ),
                            None,
                        )
                        combined_stat = {
                            "src": flow_stat["match"].get("nw_src", ""),
                            "dst": flow_stat["match"].get("nw_dst", ""),
                            "table_id": flow_stat["table_id"],
                            "ip_bytes": flow_stat["byte_count"],
                            "ip_packet": flow_stat["packet_count"],
                            "ip_duration": flow_stat["duration_sec"],
                            "in_port": flow_stat["match"]["in_port"],
                            # "dl_dst": flow_stat["match"]["dl_dst"],
                            "port_bytes": port_stat["tx_bytes"] + port_stat["rx_bytes"],
                            "port_packet": port_stat["tx_packets"]
                            + port_stat["rx_packets"],
                            "port_flow_count": len(flow_stats),
                            "table_active_count": (
                                table_stat["active_count"] if table_stat else 0
                            ),
                            "table_lookup_count": (
                                table_stat["lookup_count"] if table_stat else 0
                            ),
                            "table_matched_count": (
                                table_stat["matched_count"] if table_stat else 0
                            ),
                            "port_rx_packets": port_stat["rx_packets"],
                            "port_tx_packets": port_stat["tx_packets"],
                            "port_rx_bytes": port_stat["rx_bytes"],
                            "port_tx_bytes": port_stat["tx_bytes"],
                            "port_rx_dropped": port_stat["rx_dropped"],
                            "port_tx_dropped": port_stat["tx_dropped"],
                            "port_rx_errors": port_stat["rx_errors"],
                            "port_tx_errors": port_stat["tx_errors"],
                            "port_rx_frame_err": port_stat["rx_frame_err"],
                            "port_rx_over_err": port_stat["rx_over_err"],
                            "port_rx_crc_err": port_stat["rx_crc_err"],
                            "port_collisions": port_stat["collisions"],
                            "port_duration_sec": port_stat["duration_sec"],
                        }

                        combined_stats.append(combined_stat)

        return combined_stats

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                combined_stats = self.get_ofctl_combined_stats(dp)
                prediction = None
                for combined_stat in combined_stats:
                    data = [
                        combined_stat["src"],
                        combined_stat["dst"],
                        combined_stat["table_id"],
                        combined_stat["ip_bytes"],
                        combined_stat["ip_packet"],
                        combined_stat["ip_duration"],
                        combined_stat["in_port"],
                        combined_stat["port_bytes"],
                        combined_stat["port_packet"],
                        combined_stat["port_flow_count"],
                        combined_stat["table_active_count"],
                        combined_stat["table_lookup_count"],
                        combined_stat["table_matched_count"],
                        combined_stat["port_rx_packets"],
                        combined_stat["port_tx_packets"],
                        combined_stat["port_rx_bytes"],
                        combined_stat["port_tx_bytes"],
                        combined_stat["port_rx_dropped"],
                        combined_stat["port_tx_dropped"],
                        combined_stat["port_rx_errors"],
                        combined_stat["port_tx_errors"],
                        combined_stat["port_rx_frame_err"],
                        combined_stat["port_rx_over_err"],
                        combined_stat["port_rx_crc_err"],
                        combined_stat["port_collisions"],
                        combined_stat["port_duration_sec"],
                    ]
                prediction = self.ml_obj.classify(data)
                self.logger.info("Predicted: %s", str(prediction))
            hub.sleep(10)

