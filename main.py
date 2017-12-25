from netconflib.netconf import NetConf

ncl = NetConf("config.ini")

ncl.enableIPForwarding()
