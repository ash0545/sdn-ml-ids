from operator import attrgetter

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

import requests
import csv
from time import sleep


class SimpleMonitor13(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug("register datapath: %016x", datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug("unregister datapath: %016x", datapath.id)
                del self.datapaths[datapath.id]

    def get_ofctl_port_stats(self, dp):
        ofctl_rest_ip = "127.0.0.1"
        ofctl_rest_port = 8080

        url = "http://{0}:{1}/stats/port/{2}".format(
            ofctl_rest_ip, ofctl_rest_port, dp.id
        )
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(
                "Failed to retrieve port stats: "
                + str(response.status_code)
                + " - "
                + response.text
            )
            return []

    # Attempt to get similar stats to the MCAD dataset
    def get_ofctl_combined_stats(self, dp):
        # flow stats
        url = "http://127.0.0.1:8080/stats/flowdesc/{}".format(dp.id)
        response = requests.get(url)
        if response.status_code == 200:
            flow_stats_dict = response.json()
            flow_stats = []
            for dpid, stats in flow_stats_dict.items():
                flow_stats.extend(stats)
        else:
            self.logger.error(
                "Failed to retrieve port stats: "
                + str(response.status_code)
                + " - "
                + response.text
            )
            flow_stats = []
        print(flow_stats)

        # port stats
        url = "http://127.0.0.1:8080/stats/port/{}".format(dp.id)
        response = requests.get(url)
        if response.status_code == 200:
            port_stats_dict = response.json()
            port_stats = []
            for dpid, stats in port_stats_dict.items():
                port_stats.extend(stats)
        else:
            self.logger.error(
                "Failed to retrieve port stats: "
                + str(response.status_code)
                + " - "
                + response.text
            )
            port_stats = []
        print(port_stats)

        # table stats
        url = "http://127.0.0.1:8080/stats/table/{}".format(dp.id)
        response = requests.get(url)
        if response.status_code == 200:
            table_stats_dict = response.json()
            table_stats = []
            for dpid, stats in table_stats_dict.items():
                table_stats.extend(stats)
        else:
            self.logger.error(
                "Failed to retrieve port stats: "
                + str(response.status_code)
                + " - "
                + response.text
            )
            table_stats = []
        print(table_stats)

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
                        # "dl_dst": flow_stat["match"]["eth_dst"] removed
                        combined_stat = {
                            "src": flow_stat["match"].get("ipv4_src", ""),
                            "dst": flow_stat["match"].get("ipv4_dst", ""),
                            "table_id": flow_stat["table_id"],
                            "ip_bytes": flow_stat["byte_count"],
                            "ip_packet": flow_stat["packet_count"],
                            "ip_duration": flow_stat["duration_sec"],
                            "in_port": flow_stat["match"]["in_port"],
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
                self._request_stats(dp)
                combined_stats = self.get_ofctl_combined_stats(dp)
                print(combined_stats)
                with open("combined.csv", "a", buffering=1) as csvfile:
                    writer = csv.writer(csvfile)
                    if csvfile.tell() == 0:
                        # "dl_dst", removed
                        writer.writerow(
                            [
                                "src",
                                "dst",
                                "table_id",
                                "ip_bytes",
                                "ip_packet",
                                "ip_duration",
                                "in_port",
                                "port_bytes",
                                "port_packet",
                                "port_flow_count",
                                "table_active_count",
                                "table_lookup_count",
                                "table_matched_count",
                                "port_rx_packets",
                                "port_tx_packets",
                                "port_rx_bytes",
                                "port_tx_bytes",
                                "port_rx_dropped",
                                "port_tx_dropped",
                                "port_rx_errors",
                                "port_tx_errors",
                                "port_rx_frame_err",
                                "port_rx_over_err",
                                "port_rx_crc_err",
                                "port_collisions",
                                "port_duration_sec",
                            ]
                        )
                    for combined_stat in combined_stats:
                        writer.writerow(
                            [
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
                        )

                    # for dpid, port_stats_list in ofctl_port_stats.items():
                    #     for port_stat in port_stats_list:
                    #         writer.writerow(
                    #             [
                    #                 dpid,
                    #                 port_stat["port_no"],
                    #                 port_stat["rx_packets"],
                    #                 port_stat["tx_packets"],
                    #                 port_stat["rx_bytes"],
                    #                 port_stat["tx_bytes"],
                    #                 port_stat["rx_errors"],
                    #                 port_stat["tx_errors"],
                    #             ]
                    #         )
            hub.sleep(1)

    def _request_stats(self, datapath):
        self.logger.debug("send stats request: %016x", datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info(
            "datapath         " "in-port  eth-dst           " "out-port packets  bytes"
        )
        self.logger.info(
            "---------------- "
            "-------- ----------------- "
            "-------- -------- --------"
        )
        # with open("flow_stats.csv", "a", buffering=1) as csvfile:
        #     writ = csv.writer(csvfile, delimiter=",")
        #     if csvfile.tell() == 0:
        #         writ.writerow(
        #             [
        #                 "datapath_id",
        #                 "in_port",
        #                 "eth_dst",
        #                 "out_port",
        #                 "packet_count",
        #                 "byte_count",
        #             ]
        #         )

        for stat in sorted(
            [flow for flow in body if flow.priority == 1],
            key=lambda flow: (flow.match["in_port"], flow.match["eth_dst"]),
        ):
            self.logger.info(
                "%016x %8x %17s %8x %8d %8d",
                ev.msg.datapath.id,
                stat.match["in_port"],
                stat.match["eth_dst"],
                stat.instructions[0].actions[0].port,
                stat.packet_count,
                stat.byte_count,
            )
            # writ.writerow(
            #     [
            #         ev.msg.datapath.id,
            #         stat.match["in_port"],
            #         stat.match["eth_dst"],
            #         stat.instructions[0].actions[0].port,
            #         stat.packet_count,
            #         stat.byte_count,
            #     ]
            # )

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info(
            "datapath         port     "
            "rx-pkts  rx-bytes rx-error "
            "tx-pkts  tx-bytes tx-error"
        )
        self.logger.info(
            "---------------- -------- "
            "-------- -------- -------- "
            "-------- -------- --------"
        )

        # with open("port_stats.csv", "a", buffering=1) as csvfile:
        #     writ = csv.writer(csvfile, delimiter=",")
        #     if csvfile.tell() == 0:
        #         writ.writerow(
        #             [
        #                 "datapath",
        #                 "port",
        #                 "rx-pkts",
        #                 "rx-bytes",
        #                 "rx-error",
        #                 "tx-pkts",
        #                 "tx-bytes",
        #                 "tx-error",
        #             ]
        #         )

        for stat in sorted(body, key=attrgetter("port_no")):
            self.logger.info(
                "%016x %8x %8d %8d %8d %8d %8d %8d",
                ev.msg.datapath.id,
                stat.port_no,
                stat.rx_packets,
                stat.rx_bytes,
                stat.rx_errors,
                stat.tx_packets,
                stat.tx_bytes,
                stat.tx_errors,
            )
            # writ.writerow(
            #     [
            #         ev.msg.datapath.id,
            #         stat.port_no,
            #         stat.rx_packets,
            #         stat.rx_bytes,
            #         stat.rx_errors,
            #         stat.tx_packets,
            #         stat.tx_bytes,
            #         stat.tx_errors,
            #     ]
            # )

