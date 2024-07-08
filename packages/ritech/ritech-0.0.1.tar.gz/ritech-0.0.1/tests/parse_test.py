from ritech.transit.realtime import (
    PassioRequestHandler, 
    GTFS, # Enum
    gtfs as realtime # types
)

def parse_test():
    """
    use the enum GTFS.REALTIME for full feedMessage
    """
    r = PassioRequestHandler()

    feed: realtime.FeedMessage = r.get(GTFS.REALTIME)

    print(feed)

parse_test()