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

    # next -> Get more features through modification
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

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
                # flow stats
                url = "http://127.0.0.1:8080/stats/flowdesc/{}".format(dp.id)
                response = requests.get(url)
                if response.status_code == 200:
                    flow_stats = response.json()
                else:
                    self.logger.error(
                        "Failed to retrieve port stats: "
                        + str(response.status_code)
                        + " - "
                        + response.text
                    )
                    return []
                print(flow_stats)

                # port stats
                url = "http://127.0.0.1:8080/stats/port/{}".format(dp.id)
                response = requests.get(url)
                if response.status_code == 200:
                    port_stats = response.json()
                else:
                    self.logger.error(
                        "Failed to retrieve port stats: "
                        + str(response.status_code)
                        + " - "
                        + response.text
                    )
                    return []
                print(port_stats)

                # table stats
                url = "http://127.0.0.1:8080/stats/table/{}".format(dp.id)
                response = requests.get(url)
                if response.status_code == 200:
                    table_stats = response.json()
                else:
                    self.logger.error(
                        "Failed to retrieve port stats: "
                        + str(response.status_code)
                        + " - "
                        + response.text
                    )
                    return []
                print(table_stats)
                # Get port details from ofctl_rest
                ofctl_port_stats = self.get_ofctl_port_stats(dp)
                with open("ofctl_details.csv", "a", buffering=1) as csvfile:
                    writer = csv.writer(csvfile)
                    if csvfile.tell() == 0:
                        writer.writerow(
                            [
                                "datapath_id",
                                "port_no",
                                "rx_packets",
                                "tx_packets",
                                "rx_bytes",
                                "tx_bytes",
                                "rx_errors",
                                "tx_errors",
                            ]
                        )

                    for dpid, port_stats_list in ofctl_port_stats.items():
                        for port_stat in port_stats_list:
                            writer.writerow(
                                [
                                    dpid,
                                    port_stat["port_no"],
                                    port_stat["rx_packets"],
                                    port_stat["tx_packets"],
                                    port_stat["rx_bytes"],
                                    port_stat["tx_bytes"],
                                    port_stat["rx_errors"],
                                    port_stat["tx_errors"],
                                ]
                            )
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
        with open("flow_stats.csv", "a", buffering=1) as csvfile:
            writ = csv.writer(csvfile, delimiter=",")
            if csvfile.tell() == 0:
                # Write the header row if the file is empty
                writ.writerow(
                    [
                        "datapath_id",
                        "in_port",
                        "eth_dst",
                        "out_port",
                        "packet_count",
                        "byte_count",
                    ]
                )

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
                writ.writerow(
                    [
                        ev.msg.datapath.id,
                        stat.match["in_port"],
                        stat.match["eth_dst"],
                        stat.instructions[0].actions[0].port,
                        stat.packet_count,
                        stat.byte_count,
                    ]
                )

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

        with open("port_stats.csv", "a", buffering=1) as csvfile:
            writ = csv.writer(csvfile, delimiter=",")
            if csvfile.tell() == 0:
                # Write the header row if the file is empty
                writ.writerow(
                    [
                        "datapath",
                        "port",
                        "rx-pkts",
                        "rx-bytes",
                        "rx-error",
                        "tx-pkts",
                        "tx-bytes",
                        "tx-error",
                    ]
                )

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
                writ.writerow(
                    [
                        ev.msg.datapath.id,
                        stat.port_no,
                        stat.rx_packets,
                        stat.rx_bytes,
                        stat.rx_errors,
                        stat.tx_packets,
                        stat.tx_bytes,
                        stat.tx_errors,
                    ]
                )

