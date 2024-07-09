import datetime
import json
import re

from bs4 import BeautifulSoup

from .classes import TripPointCompatible, EmptyTripPoint, TripPointCompatibleUnclear, Station, Address, Point, Mot, \
    TripResult
from .exceptions import SetupException, NotImplementedException
from .tools import coords


class TripRequest:
    mots = ['zug', 's-bahn', 'u-bahn', 'stadtbahn', 'tram', 'stadtbus', 'regionalbus', 'schnellbus', 'seilbahn',
            'schiff', 'ast', 'sonstige']

    def __init__(self):
        self.efa_triprequest_url = None  # Overridden by efa

    def submit(self, url: str, post_data: dict, outputtype: str):
        """Is overridden by efa"""
        pass

    def tripRequest(self, origin, destination, via=None, time=None, timetype='dep', exclude=None, max_interchanges=9,
                    select_interchange_by='speed', use_near_stops=False, train_type='local', walk_speed='normal',
                    with_bike=False, use_realtime=True, apitype='both'):
        if exclude is None:
            exclude = []
        now = datetime.datetime.now()

        # Parametervalidierung
        if not isinstance(origin, TripPointCompatible):
            origin = TripPointCompatible.fromanything(origin)
            if origin is None:
                raise SetupException('origin', origin, 'Valid Station Description')

        if not isinstance(destination, TripPointCompatible):
            destination = TripPointCompatible.fromanything(destination)
            if destination is None:
                raise SetupException('destination', destination, 'Valid Station Description')

        if via is None:
            via = EmptyTripPoint()
        elif not isinstance(via, TripPointCompatible):
            via = TripPointCompatible.fromanything(via)
            if via is None:
                raise SetupException('via', via, 'Valid Station Description')

        if time is not None and not isinstance(time, datetime.datetime):
            raise SetupException('time', time, 'datetime.datetime')

        if timetype not in ['dep', 'arr']:
            raise SetupException('timetype', timetype, '(dep|arr)')

        if not isinstance(exclude, list) or len(set(exclude) - set(self.mots)):
            raise SetupException('exclude', exclude,
                                 'list with (zug|s-bahn|u-bahn|stadtbahn|tram|stadtbus|regionalbus|schnellbus|seilbahn|schiff|ast|sonstige)')

        if not isinstance(max_interchanges, int) or max_interchanges < 0:
            raise SetupException('max_interchanges', max_interchanges, 'int>=0')

        if select_interchange_by not in ['speed', 'waittime', 'distance']:
            raise SetupException('select_interchange_by', select_interchange_by, '(speed|waittime|distance)')

        if not isinstance(use_near_stops, bool):
            raise SetupException('use_near_stops', use_near_stops, 'bool')

        if train_type not in ['local', 'ic', 'ice']:
            raise SetupException('train_type', train_type, '(local|ic|ice)')

        if walk_speed not in ['normal', 'fast', 'slow']:
            raise SetupException('walk_speed', walk_speed, '(normal|fast|slow)')

        if not isinstance(with_bike, bool):
            raise SetupException('with_bike', with_bike, 'bool')

        if not isinstance(use_realtime, bool):
            raise SetupException('use_realtime', use_realtime, 'bool')

        if apitype not in ['json', 'xml', 'both']:
            raise SetupException('apitype', apitype, '(json|xml|both)')

        # Post-Request bauen
        post = {
            'changeSpeed': walk_speed,
            'command': '',
            'imparedOptionsActive': 1,
            'inclMOT_0': 'on',
            'inclMOT_1': 'on',
            'inclMOT_2': 'on',
            'inclMOT_3': 'on',
            'inclMOT_4': 'on',
            'inclMOT_5': 'on',
            'inclMOT_6': 'on',
            'inclMOT_7': 'on',
            'inclMOT_8': 'on',
            'inclMOT_9': 'on',
            'inclMOT_10': 'on',
            'inclMOT_11': 'on',
            'includedMeans': 'checkbox',
            'itOptionsActive': 1,
            'itdDateDay': (now if time is None else time).day,
            'itdDateMonth': (now if time is None else time).month,
            'itdDateYear': (now if time is None else time).year,
            'itdTimeHour': (now if time is None else time).hour,
            'itdTimeMinute': (now if time is None else time).minute,
            'itdTripDateTimeDepArr': timetype,
            'language': 'de',
            'lineRestriction': {'local': 403, 'ic': 401, 'ice': 400}[train_type],
            'locationServerActive': 1,
            'maxChanges': max_interchanges,
            # 'name_destination': destination.name.encode('iso-8859-1'),
            # 'name_origin': origin.name.encode('iso-8859-1'),
            # 'name_via': via.name.encode('iso-8859-1'),
            'name_destination': destination.name.encode('utf-8'),
            'name_origin': origin.name.encode('utf-8'),
            'name_via': via.name.encode('utf-8'),
            'nextDepsPerLeg': 1,
            # 'place_destination': destination.place.encode('iso-8859-1'),
            # 'place_origin': origin.place.encode('iso-8859-1'),
            # 'place_via': via.place.encode('iso-8859-1'),
            'place_destination': destination.place.encode('utf-8'),
            'place_origin': origin.place.encode('utf-8'),
            'place_via': via.place.encode('utf-8'),
            'ptOptionsActive': 1,
            'requestID': 0,
            'routeType': {'speed': 'LEASTTIME', 'waittime': 'LEASTINTERCHANGE', 'distance': 'LEASTWALKING'}[
                select_interchange_by],
            'sessionID': 0,
            'text': 1993,
            'type_destination': destination.ptype,
            'type_origin': origin.ptype,
            'type_via': via.ptype
        }

        if use_realtime:
            post['useRealtime'] = 1
        if use_near_stops:
            post['useProxFootSearch'] = 1
        if with_bike:
            post['bikeTakeAlong'] = 1
        for item in exclude:
            post.pop('inclMOT_%d' % self.mots.index(item))

        settings = locals()
        settings.pop('self')

        result = TripResult(settings)
        result.time = (now if time is None else time)

        if apitype in ['xml', 'both']:
            rawdata = self.submit(self.efa_triprequest_url, post, 'XML')
            result = self.parseTripXML(rawdata, result)

        if apitype in ['json', 'both']:
            rawdata = self.submit(self.efa_triprequest_url, post, 'JSON')
            result = self.parseTripJSON(rawdata, result)

        return result

    # XML
    def parseTripXML(self, xmldata, result):
        soup = BeautifulSoup(xmldata, 'xml')

        # Metadaten
        result.sessionid = soup.itdRequest.sessionID
        result.serverid = soup.itdRequest.serverID
        result.xmlsessionid = soup.itdRequest.sessionID
        result.xmlserverid = soup.itdRequest.serverID

        # Stationen
        odvs = soup.itdRequest.itdTripRequest('itdOdv')

        for odv in odvs:
            if odv['usage'] in ['origin', 'destination', 'via']:
                myodv = self.parseOdvXML(odv)
                if isinstance(myodv, TripPointCompatibleUnclear):
                    result.unclear = True
                setattr(result, odv['usage'], myodv)

        # Routen parsen
        if soup.itdRequest.itdTripRequest.itdItinerary.itdRouteList is not None:
            routes_xml = soup.itdRequest.itdTripRequest.itdItinerary.itdRouteList('itdRoute')
            i = 0
            for routeXML in routes_xml:
                newroute = result.addroute(i)
                newroute.duration = self.parseHourMinutes(routeXML['publicDuration'])
                newroute.vehicletime = routeXML['vehicleTime']
                # newroute.units_adult = routeXML.itdFare.itdSingleTicket['unitsAdult']
                # newroute.fare_adult  = routeXML.itdFare.itdSingleTicket['fareAdult']
                # newroute.fare_child  = routeXML.itdFare.itdSingleTicket['fareChild']

                if routeXML.itdInfoTextList is not None:
                    for infotext in routeXML.itdInfoTextList('infoTextListElem'):
                        newroute.infotext.append(infotext.getText().strip())

                parts_xml = routeXML.itdPartialRouteList('itdPartialRoute')
                j = 0
                for partXML in parts_xml:
                    newpart = newroute.addpart(j)
                    newpart.origin = Point()
                    newpart.origin = self.parsePointXML(partXML('itdPoint')[0], newpart.origin)
                    newpart.destination = Point()
                    newpart.destination = self.parsePointXML(partXML('itdPoint')[1], newpart.destination)
                    newpart.mot = self.parseMotXML(partXML.itdMeansOfTransport, Mot())

                    if newpart.mot.walk:
                        newpart.origin.departure_live = None
                        newpart.origin.departure_delay = None
                        newpart.destination.arrival_live = None
                        newpart.destination.arrival_delay = None

                    newpart.duration = int(partXML['timeMinute'])
                    if partXML.has_attr('distance'):
                        newpart.distance = int(partXML['distance'])
                    j += 1
                i += 1
        return result

    def parseOdvXML(self, xmldata):
        if xmldata.itdOdvPlace['state'] == 'empty':
            return EmptyTripPoint()

        if 'list' in [xmldata.itdOdvPlace['state'], xmldata.itdOdvName['state']]:
            result = TripPointCompatibleUnclear()
            result.place = [elem.getText().strip() for elem in xmldata.itdOdvPlace('odvPlaceElem')]
            result.name = [elem.getText().strip() for elem in xmldata.itdOdvName('odvNameElem')]
        else:
            odvtype = xmldata['type']
            if odvtype == 'any': odvtype = xmldata.itdOdvName.odvNameElem['anyType']
            if odvtype == 'stop':
                result = Station()
                result.place = xmldata.itdOdvPlace.odvPlaceElem.getText().strip()
                result.name = xmldata.itdOdvName.odvNameElem.getText().strip()
                if xmldata.itdOdvName.odvNameElem.has_attr('stopID'):
                    result.stopid = xmldata.itdOdvName.odvNameElem['stopID']
                else:
                    result.stopid = xmldata.itdOdvName.odvNameElem['id']

                if xmldata.itdOdvName.odvNameElem.has_attr('x'):
                    result.coords = coords(xmldata.itdOdvName.odvNameElem['x'], xmldata.itdOdvName.odvNameElem['y'])
            elif odvtype == 'address':
                result = Address()
                result.place = xmldata.itdOdvPlace.odvPlaceElem.getText().strip()
                result.name = xmldata.itdOdvName.odvNameElem.getText().strip()
                result.streetname = xmldata.itdOdvName.odvNameElem['streetName']
                result.housenumber = xmldata.itdOdvName.odvNameElem['houseNumber']
                if xmldata.itdOdvName.odvNameElem.has_attr('x'): result.coords = coords(
                    xmldata.itdOdvName.odvNameElem['x'], xmldata.itdOdvName.odvNameElem['y'])
            else:
                raise NotImplementedException('unknown type of odv: "%s"' % xmldata['type'])
        return result

    def parsePointXML(self, xmldata, result):
        result.place = xmldata['locality'].strip()
        result.name = xmldata['nameWO'].strip() if xmldata['locality'] != '' or xmldata[
            'nameWO'] != '' else xmldata['name'].strip()
        result.stopid = xmldata['stopID']
        result.platformname = xmldata['platformName'].replace('Gleis', '').replace('Bstg.', '').strip()
        if xmldata('x'):
            result.coords = coords(xmldata['x'], xmldata['y'])

        times = []
        if xmldata('itdDateTimeTarget'):
            times.append(self.parseDateTimeXML(xmldata.itdDateTimeTarget))
        if xmldata('itdDateTime'):
            times.append(self.parseDateTimeXML(xmldata.itdDateTime))
        if len(times) > 0:
            setattr(result, '%s' % xmldata['usage'], times[0])
        if len(times) == 2:
            setattr(result, '%s_live' % xmldata['usage'], times[1])
            setattr(result, '%s_delay' % xmldata['usage'], int((times[1] - times[0]).total_seconds()) / 60)
        return result

    def parseMotXML(self, xmldata, result):
        if not xmldata.has_attr('motType'):
            result.name = 'Fußweg'
            result.destination = ''
            result.walk = True
            return result

        result.mottype = int(xmldata['motType'])

        if result.mottype == 0 and xmldata.has_attr('trainName'):
            result.name = xmldata['trainName'].strip()
            result.abbr = xmldata['trainType'].strip()
            result.number = (xmldata['symbol'] if xmldata.has_attr('symbol') else xmldata['shortname']).strip()
            result.line = result.abbr + result.number
        else:
            result.name = xmldata['productName'].strip()
            result.abbr = re.sub('[0-9 -]', '', xmldata['shortname']).strip()
            result.number = re.sub('[^0-9]', '', xmldata['shortname']).strip()
            result.line = (xmldata['symbol'] if xmldata.has_attr('symbol') else xmldata['shortname']).strip()

        # print xmldata
        result.destination = Station()
        result.destination.stopid = xmldata['destID']
        result.destination.name = xmldata['destination'].strip()
        return result

    def parseDateTimeXML(self, xmldata):
        hour = int(xmldata.itdTime['hour'])
        if hour != 24:
            return datetime.datetime(int(xmldata.itdDate['year']), int(xmldata.itdDate['month']),
                                     int(xmldata.itdDate['day']), hour, int(xmldata.itdTime['minute']))
        else:
            return datetime.datetime(int(xmldata.itdDate['year']), int(xmldata.itdDate['month']),
                                     int(xmldata.itdDate['day']), 0,
                                     int(xmldata.itdTime['minute'])) + datetime.timedelta(1)

    def parseHourMinutes(self, data):
        data = data.split(':')
        return int(data[0]) * 60 + int(data[1])

    # JSON
    def parseTripJSON(self, rawdata, result):
        jsondata = json.loads(rawdata)

        # Metadaten
        for param in jsondata['parameters']:
            if param['name'] in ('sessionID', 'serverID'):
                setattr(result, param['name'].lower(), param['value'])
                setattr(result, 'json%s' % param['name'].lower(), param['value'])

        # Stationen
        # Gibts nicht! Naja…

        # Routen parsen
        routesJSON = jsondata['trips']
        i = 0
        for routeJSONfoo in routesJSON:
            routeJSON = routeJSONfoo['trip']

            newroute = result.addroute(i)
            newroute.duration = self.parseHourMinutes(routeJSON['duration'])

            partsJSON = routeJSON['legs']
            j = 0
            for partJSON in partsJSON:
                newpart = newroute.addpart(j)
                if newpart.origin is None: newpart.origin = Point()
                if newpart.destination is None: newpart.destination = Point()
                newpart.origin = self.parsePointJSON(partJSON['points'][0], newpart.origin)
                newpart.destination = self.parsePointJSON(partJSON['points'][1], newpart.destination)
                newpart.mot = self.parseMotJSON(partJSON['mode'], Mot())

                newpart.via = []
                newpart.via_all = []

                if 'path' in partJSON: newpart.path = [coords(*c.split(',')) for c in
                                                       partJSON['path'].strip().split(' ')]

                stopsJSON = partJSON['stopSeq'] if 'stopSeq' in partJSON else []

                k = 0
                for stopJSON in stopsJSON:
                    newstop = self.parseStopJSON(stopJSON, Point())
                    newpart.via.append(newstop)
                    newstop.k = k
                    k += 1

                # So, und jetzt müssen wir dinge kompliziert machen, um bugs der EFA zu Workarounden
                # Zunächst mal original origin und destination durch die detaillierteren versionen aus der Stopliste ersetzen
                for k in range(len(newpart.via)):
                    via = newpart.via[k]
                    if via.stopid == newpart.origin.stopid and via.get_maybelive_time(
                            'departure') == newpart.origin.departure and via.coords == newpart.origin.coords:
                        newpart.origin = via
                        newpart.via.pop(k)
                        break
                for k in range(len(newpart.via)):
                    via = newpart.via[len(newpart.via) - 1 - k]
                    if via.stopid == newpart.destination.stopid and via.get_maybelive_time(
                            'arrival') == newpart.destination.arrival and via.coords == newpart.destination.coords:
                        newpart.destination = via
                        newpart.via.pop(len(newpart.via) - 1 - k)
                        break

                # Gefilterte liste ohne durchfahren erstellen
                newpart.via_all = newpart.via
                newpart.via = []
                for via in newpart.via_all:
                    if not via.nostop:
                        newpart.via.append(via)

                newpart.duration = int((newpart.destination.arrival - newpart.origin.departure).total_seconds()) / 60
                if 'turnInst' in partJSON:
                    newpart.distance = sum([int(inst['dis']) for inst in partJSON['turnInst']])

                j += 1
            i += 1

        if len(result.routes) > 0:
            result.origin = result.routes[0].parts[0].origin
            result.destination = result.routes[0].parts[-1].destination

        return result

    def parseJSONcoords(self, data):
        if data.strip() in ('', ','): return None
        return [int(float(a)) for a in
                data.split(',')]  # Ja, int(float(a))! Das muss so, damit sowohl '123.0000' als auch '123' okay geht!

    def parsePointJSON(self, jsondata, result):
        if result.place is None or result.place == '':
            result.place = jsondata['place'].encode('utf8').strip()
        if result.name is None or result.name == '':
            result.name = (jsondata['name'] if not jsondata['name'].startswith(jsondata['place']) else jsondata['name'][
                                                                                                       len(jsondata[
                                                                                                               'place']):]).encode(
                'utf8').strip()
        result.stopid = jsondata['ref']['id']
        if result.platformname is None:
            result.platformname = jsondata['ref']['platform'].encode('utf8').strip()
        c = self.parseJSONcoords(jsondata['ref']['coords'])
        if c is not None: result.coords = coords(c[0], c[1])

        if jsondata['dateTime']['time'] != '24:00':
            datetimeObject = datetime.datetime.strptime(
                '%s %s' % (jsondata['dateTime']['date'], jsondata['dateTime']['time']), '%d.%m.%Y %H:%M')
        else:
            datetimeObject = datetime.datetime.strptime('%s' % (jsondata['dateTime']['date']),
                                                        '%d.%m.%Y') + datetime.timedelta(1)
        setattr(result, jsondata['usage'], datetimeObject)
        return result

    def parseMotJSON(self, jsondata, result):
        if jsondata['code'] == '-1':
            result.name = 'Fußweg'
            result.destination = ''
            result.walk = True
            return result

        result.mottype = int(jsondata['code'])

        tmpnumber = re.sub('\([^\)]+\)', '', jsondata['number'].encode('utf8'))
        result.number = re.sub('[^0-9]', '', tmpnumber).strip()
        result.abbr = re.sub('[0-9 -]', '', tmpnumber).strip()
        result.line = tmpnumber.strip()

        tmpname = jsondata['name'].encode('utf8')
        if result.number in tmpname:
            if result.abbr == '' and result.number != '':
                tmpabbr = tmpname.split(result.number)[0].replace('-', '').strip()
                if len(tmpabbr) <= 3: result.abbr = tmpname.split(result.number)[0].replace('-', '').strip()
                result.name = tmpname.split(result.number)[1].strip()
                result.line = result.abbr + result.number

            if result.name is None and result.number != '':
                tmpname.split(result.number)[0].strip()

        if result.destination is None:
            result.destination = Station()
            result.destination.stopid = jsondata['destID']
            result.destination.name = jsondata['destination'].encode('utf8').strip()
        return result

    def parseStopJSON(self, jsondata, result):
        result.name = jsondata['nameWO'].encode('utf8').strip()
        result.place = jsondata['name'].encode('utf8').strip()
        result.place = ' '.join(result.place.split(' ')[0:0 - len(result.name.split(' '))])
        result.stopid = jsondata['ref']['id']
        result.platformname = jsondata['platformName'].encode('utf8').replace('Gleis', '').replace('Bstg.', '').strip()

        if 'arrDateTime' in jsondata['ref']:
            result.arrival = datetime.datetime.strptime(jsondata['ref']['arrDateTime'].replace('24:', '00:'),
                                                        '%Y%m%d %H:%M')
            if 'arrDelay' in jsondata['ref'] and int(jsondata['ref']['arrDelay']) >= 0:
                result.arrival_delay = int(jsondata['ref']['arrDelay'])
                result.arrival_live = result.arrival + datetime.timedelta(minutes=result.arrival_delay)
            else:
                result.arrival_delay = None
                result.arrival_live = None

        if 'depDateTime' in jsondata['ref']:
            result.departure = datetime.datetime.strptime(jsondata['ref']['depDateTime'].replace('24:', '00:'),
                                                          '%Y%m%d %H:%M')
            if 'depDelay' in jsondata['ref'] and int(jsondata['ref']['depDelay']) >= 0:
                result.departure_delay = int(jsondata['ref']['depDelay'])
                result.departure_live = result.departure + datetime.timedelta(minutes=result.departure_delay)
            else:
                result.departure_delay = None
                result.departure_live = None

        if 'arrDateTime' not in jsondata['ref'] and 'depDateTime' not in jsondata['ref']:
            result.nostop = True

        c = self.parseJSONcoords(jsondata['ref']['coords'])
        if c is not None: result.coords = coords(c[0], c[1])
        return result
