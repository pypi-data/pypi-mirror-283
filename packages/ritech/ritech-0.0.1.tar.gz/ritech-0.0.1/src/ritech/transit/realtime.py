from enum import Enum

import requests as r

"""
protobuf api usage
https://googleapis.dev/python/protobuf/latest/

https://protobuf.dev/getting-started/pythontutorial/#compiling-protocol-buffers
Protobuf Buffers now require stubs to fully be generated with --pyi_out
"""
from google.protobuf.message import (
    Message,
    DecodeError
)
import ritech.proto.gtfs_realtime_pb2 as gtfs

class GTFS(Enum):
    REALTIME =  "https://passio3.com/ritech/passioTransit/gtfs/realtime"
    VEHCILE_POSITION = "https://passio3.com/ritech/passioTransit/gtfs/realtime/vehiclePositions"
    TRIP_UPDATES = "https://passio3.com/ritech/passioTransit/gtfs/realtime/tripUpdates"
    SERVICE_ALERTS = "https://passio3.com/ritech/passioTransit/gtfs/realtime/serviceAlerts"

class GeneralTransitFeedParser():

    media_type = 'application/protobuf'
    
    def parse(self, endpoint: GTFS, stream: bytes, media_type=None):
        match endpoint:
            case GTFS.REALTIME:
                return self._message(gtfs.FeedMessage(), stream)
            case GTFS.VEHCILE_POSITION:
                return self._message(gtfs.VehiclePosition(), stream)
            case GTFS.TRIP_UPDATES:
                return self._message(gtfs.TripUpdate(), stream)
            
    def _message(self, feed: Message, stream: bytes) -> Message:
        try:
            feed.ParseFromString(stream)
            return feed
        except DecodeError:
            raise DecodeError
        
class PassioRequestHandler:

    def __init__(self):
        self.parser = GeneralTransitFeedParser()

    def get(self, endpoint: GTFS):

        return self.parser.parse(endpoint, stream=r.get(endpoint.value).content) # requests bytes(protobuf not a text based protocol
