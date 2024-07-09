from colorama import Fore, Back, Style

from .exceptions import SetupException
from .tools import Table, bold


class TripPointCompatible:
    """ Something that can be used as an origin, destination or via point
    Do not use directly! Use EFAStation or EFAAdress instead.

    place  -- city in which the point is located
    name   -- name of the point
    ptype  -- type of point (stop, address oder poi)
    coords -- tuple describing the coordinates of point, can be None if
              not from API
    """

    def __init__(self, **args):
        self.place = None
        self.name = None
        self.ptype = None
        self.coords = None

    def __str__(self):
        return (('%s %s' % (
            self.place, self.name)) if self.place is not None and self.place.strip() != '' else self.name).replace(
            'Hauptbahnhof', 'Hbf').replace('Bahnhof', 'Bf')

    def asdict(self):
        return {'name': self.name, 'place': self.place, 'ptype': self.ptype, 'coords': self.coords}

    @classmethod
    def fromanything(cls, data):
        """ Creates an TripPointCompatible.
        returns Station or Adress or None if data is invalid

        data -- list with two or three items or string describing place,
                name and type. if two items, stop is used for type
                unless name starts with “addr:” or “poi:”. For strings,
                the first word is used for city and the remaining words
                for name.
        """
        if isinstance(data, str):
            data = data.split(' ', 1)
        if len(data) not in (2, 3):
            return None

        if not isinstance(data, list):
            return None
        if len(data) == 2:
            data.append('stop')
        if data[1].startswith('addr:'):
            data[1] = data[1][5:]
            data[2] = 'address'
        elif data[2].startswith('poi:'):
            data[1] = data[1][4:]
            data[2] = 'poi'

        if data[2] not in ('poi', 'stop', 'address'):
            raise SetupException('ptype', data[2], '(stop|address|point)')

        result = Station() if data[2] == 'stop' else Address() if data[2] == 'address' else POI()
        result.place = data[0]
        result.name = data[1]
        return result


class TripPointCompatibleUnclear:
    """ Something that should be an TripPointCompatible but was rejected
    by EFA for not finding an definitive result.

    place  -- city in which the point is located, list of suggestions or
              string if definitive result
    name   -- name of the point, list of suggestions or string if
              definitive result
    ptype  -- type of point (stop, address oder poi)
    """

    def __init__(self):
        self.place = None
        self.name = None
        self.ptype = None

    def __str__(self):
        if not isinstance(self.place, list):
            self.place = [self.place]
        if not isinstance(self.name, list):
            self.name = [self.name]

        placetbl = [['', p] for p in self.place]
        nametbl = [['', p] for p in self.name]
        placetbl[0][0] = 'City:'
        nametbl[0][0] = 'Stop:'

        return str(Table(placetbl + nametbl))


class EmptyTripPoint(TripPointCompatible):
    """ Used as argument for via when no via is requested. """

    def __init__(self):
        TripPointCompatible.__init__(self)
        self.name = ''
        self.place = ''
        self.ptype = 'stop'


class Station(TripPointCompatible):
    """ A station

    place  -- city in which the station is located
    name   -- name of the station
    stopid -- id of station, can be None if not from api
    coords -- tuple describing the coordinates of station, can be None
              if not from api
    """

    def __init__(self):
        TripPointCompatible.__init__(self)
        self.stopid = None
        self.ptype = 'stop'


class Address(TripPointCompatible):
    """ An Adress

    place  -- city in which the address is located
    name   -- name of the adress (streetname and maybe housenumber)
    streetname  -- streetname of the address, can be None if not from
                   api
    housenumber -- housenumber of the address or None if not from api
    coords -- tuple describing the coordinates of address, can be None
              if not from api
    """

    def __init__(self):
        TripPointCompatible.__init__(self)
        self.streetname = None
        self.housenumber = None
        self.ptype = 'address'

    def asdict(self):
        return {'name': self.name, 'place': self.place, 'ptype': self.ptype, 'coords': self.coords,
                'streetname': self.streetname, 'housenumber': self.housenumber}


class POI(TripPointCompatible):
    """ A point of interest

    place  -- city in which the address is located
    name   -- name of the adress (streetname and maybe housenumber)
    coords -- tuple describing the coordinates of address, can be None
              if not from api
    """

    def __init__(self):
        TripPointCompatible.__init__(self)
        self.ptype = 'poi'


class TripResult:
    """ Search Results of a TripRequest

    settings    -- dict of settings used for the triprequest
    origin      -- Point describing the origin
    destination -- Point describing the destination
    via         -- TripPointCompatible describing the via
    unclear		-- True if waypoints were unclearly requested and (if
                   ML-API is used) one or more of origin, destination or
                   via is TripPointCompatibleUnclear. No routes will
                   be available.
    routes      -- list of Route describing routes
    """

    def __init__(self, settings):
        self.settings = settings
        self.origin = EmptyTripPoint()
        self.destination = EmptyTripPoint()
        self.via = EmptyTripPoint()
        self.unclear = False
        self.routes = []

    def addroute(self, i):
        if i < len(self.routes):
            return self.routes[i]
        else:
            new = Route()
            self.routes.append(new)
            return new

    def __str__(self):
        if self.unclear:
            result = ''
            if isinstance(self.origin, TripPointCompatibleUnclear):
                result += bold('Unclear origin:\n') + str(self.origin) + '\n'
            if isinstance(self.destination, TripPointCompatibleUnclear):
                result += bold('Unclear destination:\n') + str(self.destination) + '\n'
            if isinstance(self.via, TripPointCompatibleUnclear):
                result += bold('Unclear via:\n') + str(self.via) + '\n'
        else:
            origin = bold(str(self.origin))
            destination = bold(str(self.destination))
            via = '' if isinstance(self.via, EmptyTripPoint) else (' via %s' % bold(str(self.via)))
            result = f'Route von {origin} nach {destination}{via}:\n'
            exclude = '' if not len(self.settings['exclude']) else ' – ohne ' + ', '.join(
                [s.title() for s in self.settings['exclude']])

            departure_type = bold({'arr': 'Ankunft', 'dep': 'Abfahrt'}[self.settings['timetype']])
            dep_time = self.time.strftime('%d.%m.%Y %H:%M')
            transportation_types = {'local': 'nur Nahverkehr', 'ic': 'alles außer ICE', 'ice': 'alle Zugtypen'}[
                self.settings['train_type']]

            result += f'{departure_type} {dep_time}, {transportation_types}{exclude}\n\n'

            result += '\n'.join([str(route) for route in self.routes])
        return result

    def asdict(self):
        return {
            # 'settings': { },
            'origin': self.origin.asdict(),
            'destination': self.destination.asdict(),
            'via': self.via.asdict(),
            'unclear': self.unclear,
            'routes': list(map(lambda r: r.asdict(), self.routes))
        }


class Route:
    """ A route

    duration -- route duration in minutes
    infotext -- list of strings providing additional information about
                the route
    parts    -- list of RoutePart describing the parts of the route
    """

    def __init__(self):
        self.duration = None
        self.ticket_type = None
        self.fare_adult = None
        self.fare_child = None
        self.vehicle_time = None
        self.infotext = []

        self.parts = []

    def addpart(self, i):
        if i < len(self.parts):
            return self.parts[i]
        else:
            new = RoutePart()
            self.parts.append(new)
            return new

    def __str__(self):
        lines = []
        departure_time = self.parts[0].origin.get_formatted_time('departure')
        arrival_time = self.parts[-1].destination.get_formatted_time('arrival')
        time_line = f'{bold("Abfahrt:")} {departure_time} - {bold("Ankunft:")} {arrival_time} - {bold("Dauer:")} - {self.duration} Minuten'
        lines.append(time_line)

        lines.append('-')
        lastpart = None
        for part in self.parts:
            if lastpart is not None:
                changetime = int((part.origin.get_maybelive_time('departure') - lastpart.destination.get_maybelive_time(
                    'arrival')).total_seconds()) / 60
                if changetime <= 0:
                    if changetime == 0 and (lastpart.mot.walk or part.mot.walk):
                        lines += ['']
                    else:
                        lines += [
                            '%s%d Minuten Umsteigezeit%s' % (Style.BRIGHT + Fore.RED, changetime, Style.RESET_ALL)]
                elif changetime < 3:
                    lines += ['%s%d Minuten Umsteigezeit%s' % (Style.BRIGHT + Fore.YELLOW, changetime, Style.RESET_ALL)]
                else:
                    lines += ['%s%d Minuten Umsteigezeit%s' % (Style.DIM, changetime, Style.RESET_ALL)]
            lines += part.getline()
            lastpart = part
        lines.append('-')

        result = str(Table(lines))
        result += '' if not len(self.infotext) else ('\n'.join(self.infotext) + '\n')
        return result

    def asdict(self):
        return {
            'duration': self.duration,
            'departure_time': self.parts[0].origin.get_datetime('departure'),  # may need different formatting
            'departure_delay': self.parts[0].origin.get_delay('departure'),
            'arrival_time': self.parts[-1].destination.get_datetime('arrival'),
            'arrival_delay': self.parts[-1].destination.get_delay('arrival'),
            'ticket_type': self.ticket_type,
            'fare_adult': self.fare_adult,
            'fare_child': self.fare_child,
            'vehicle_time': self.vehicle_time,
            'infotext': self.infotext,
            'parts': list(map(lambda p: p.asdict(), self.parts))
        }


class RoutePart:
    """ A part of a route

    origin      -- Point describing origin of the route part
    destination -- Point describing destination of the route part
    mot         -- Mot describing the mode of transportation
    distance    -- int describing the distance in meters (only for
                   routeparts by foot)
    duration    -- int describing duration of the route part in minutes
    via         -- list of Point describing points between origin and
                   destination. only available from JSON-API.
    via_all     -- list of Point describing points between origin and
                   destination including points where the MOT does not
                   stop. only available from JSON-API. due to errors in
                   the EFA-API, may be incorrect if routeparts have to
                   big delays.
    coords      -- list of coordinate-tuples describing the exact way of
                   the routepart
    """

    def __init__(self):
        self.origin = None
        self.destination = None
        self.mot = None

        self.distance = None
        self.duration = None

        self.via = None
        self.via_all = None

        self.coords = None

    def getline(self):
        if self.via is None:
            result = [self.origin.getline(False)] + [self.destination.getline(False)]
        else:
            result = [bold(self.origin.getline(True))] + [via.getline(True) for via in self.via] + [
                bold(self.destination.getline(True))]
        result[0][-1] = '%s %s' % (str(self.mot),
                                   str(self.mot.destination) if not self.mot.walk else '%d min. (%dm)' % (
                                       self.duration, self.distance))
        return result

    def asdict(self):
        return {
            'origin': self.origin.asdict(),
            'destination': self.destination.asdict(),
            'mot': self.mot.asdict(),
            'distance': self.distance,
            'duration': self.duration,
            'via': list(map(lambda v: v.asdict(), self.via)) if self.via is not None else None,
            'via_all': list(map(lambda v: v.asdict(), self.via_all)) if self.via_all is not None else None,
            'coords': self.coords
        }


class Point(TripPointCompatible):
    """ point on a route with platform and time properties

    place  -- city in which the point is located
    name   -- name of the point
    ptype  -- stop, address or poi – anything apart from stop should
              only occur at the end or beginning of a route, if at all
    stopid -- id of stop, if its a ptype is stop, else bullshit or None
    nostop -- True if train does not stop here, else False
    coords -- tuple describing the coordinates of the point

    platformname  -- Name of platform, does necessarrily have to
                     numeric
    arrival       -- datetime.datetime describing the arrival time
    arrival_live  -- datetime.datetime describing the expected arrival
                     time or None if (the JSON-API knows that) this mot
                     does not supply real time data
    arrival_delay -- expected arrival delay or None if (the JSON-API
                     knows that) this mot does not supply real time data
    departure       -- datetime.datetime describing the departure time
    departure_live  -- datetime.datetime describing the expected
                       departure time or None if (the JSON-API knows
                       that) this mot does not supply real time data
    departure_delay -- expected departure delay or None if (the
                       JSON-API knows that) this mot does not supply
                       real time data
    """

    def __init__(self):
        TripPointCompatible.__init__(self)
        self.platformname = None
        self.stopid = None
        self.arrival = None
        self.departure = None
        self.arrival_live = None
        self.departure_live = None
        self.arrival_delay = None
        self.departure_delay = None
        self.nostop = False

    def getline(self, hasvia=True, live=True):
        if not hasvia:
            return [str(self),
                    self.get_formatted_time('arrival', live) if self.arrival is not None else self.get_formatted_time(
                        'departure', live), self.platformname, '']
        else:
            return [str(self), self.get_formatted_time('arrival', live), self.get_formatted_time('departure', live),
                    self.platformname, '']

    def get_maybelive_time(self, name):
        result = getattr(self, '%s_live' % name)
        if result is None:
            result = getattr(self, '%s' % name)
        return result

    def get_formatted_time(self, name, live=True):
        time = getattr(self, '%s' % name)
        if time is None:
            return ''
        delay = getattr(self, '%s_delay' % name)
        if live and delay is not None:
            delay = ' %s%s%+d%s' % (Style.BRIGHT, Fore.GREEN if delay <= 0 else Fore.RED, delay, Style.RESET_ALL)
        else:
            delay = ''
        return '%s%s' % (time.strftime('%H:%M'), delay)

    def get_datetime(self, name) -> str:
        time = getattr(self, '%s' % name)
        if time is None:
            return ''
        return time.strftime('%Y-%m-%d %H:%M')

    def get_delay(self, name, live=True) -> float:
        delay = getattr(self, '%s_delay' % name)
        if live and delay is not None:
            return delay
        else:
            return 0.0


class Mot:
    """ mode of transport

    walk        -- True if mot is going by foot
    mottype     -- int describing the type of mot. for a nice name, use
                   .nicename()
    line        -- line name, consisting of abbreviation (if available)
                   and number, e.g. RE2 or S9
    name        -- (long) name describing the mot or line, e.g. S-Bahn
                   or Regional-Express
    abbr        -- line abbreviation, e.g. RE, NE or S. Can be empty.
    number      -- line number
    destination -- Station describing the destination of the mot (not
                   of the routepart)
    """

    def __init__(self):
        self.mottype = None
        self.line = None
        self.name = None
        self.abbr = None
        self.number = None
        self.destination = None
        self.walk = False

    def nicename(self):
        return \
            ['zug', 's-bahn', 'u-bahn', 'stadtbahn', 'tram', 'stadtbus', 'regionalbus', 'schnellbus', 'seilbahn',
             'schiff',
             'ast', 'sonstige'][self.mottype].title()

    def defline(self):
        if self.abbr is None or self.abbr == '':
            return '%s %s' % (self.nicename, self.line)
        else:
            return self.line

    def colorcode(self):
        return \
            [Back.BLACK, Back.GREEN, Back.BLUE, Back.BLUE, Back.RED, Back.MAGENTA, Back.MAGENTA, Back.MAGENTA,
             Back.CYAN,
             Back.CYAN, Back.CYAN, Back.CYAN][self.mottype]

    def __str__(self):
        if self.mottype is None:
            return Style.BRIGHT + self.name + Style.RESET_ALL
        else:
            return Fore.WHITE + self.colorcode() + Style.BRIGHT + self.line + Style.RESET_ALL

    def asdict(self):
        return {
            'mottype': self.mottype,
            'line': self.line,
            'name': self.name,
            'abbr': self.abbr,
            'number': self.number,
            'destination': self.destination.asdict()
        }
