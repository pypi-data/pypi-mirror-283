from .efa import EFA

supported = ('vrr', 'vrn', 'ding')


class VRR(EFA):
    def __init__(self):
        super().__init__()
        self.efa_triprequest_url = 'https://efa.vrr.de/vrr/XSLT_TRIP_REQUEST2'


class VRN(EFA):
    def __init__(self):
        super().__init__()
        self.efa_triprequest_url = 'https://fahrplanauskunft.vrn.de/vrn/XSLT_TRIP_REQUEST2'


class DING(EFA):
    def __init__(self):
        super().__init__()
        self.efa_triprequest_url = 'https://www.ding.eu/ding/XSLT_TRIP_REQUEST2'


def network(net):
    global supported
    if net not in supported:
        return None
    return globals()[net.upper()]()
