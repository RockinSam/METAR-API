import math, re


def get_issuance_data(data):
    if re.fullmatch('[0-9]{6}Z', data[2]):
        data = data.pop(2)
        return f'day {data[:2]} of the month at {data[2:4]}:{data[4:6]} GMT'
    return None


def get_observation_data(data):
    if data[2] == 'AUTO' or data[2] == 'COR':
        return data.pop(2)
    return None
        

def get_wind_data(data):

    if not data[2].endswith('KT'):
        return None

    var = None
    wind_dict = dict()
    to_mph = lambda s: math.ceil(int(s) * 1.1508)

    if re.fullmatch('[0-9]{3}V[0-9]{3}', data[3]):
        temp = data.pop(3)
        var = f'{temp[:3]} degrees to {temp[4:7]} degrees'
        
    data = data.pop(2)

    wind_dict['direction'] = f'{data[:3]} degrees'
    wind_dict['speed'] = f'{data[3:5]} knots ({to_mph(data[3:5])} mph)'
    wind_dict['gusts'] = f'{data[6:-2]} knots ({to_mph(data[6:-2])} mph)' if data[5] == 'G' else None
    wind_dict['variation'] = var

    return wind_dict


def get_visibility_data(data):

    if data[2] == 'CAVOK':
        return 'OK'

    to_meter = lambda d: eval(d) * 1600
    to_sm = lambda d: math.ceil(eval(d) / 1600)

    if re.fullmatch('[0-9]{4}|[0-9][/]?[0-9]*SM', data[2]):

        data = data.pop(2)

        if data.endswith('SM'):
            return f'{data[:-2]} statute miles ({to_meter(data[:-2])} meters)'
        else:
            return f'{to_sm(data)} statute miles ({data} meters)'
    else :
        return None


def get_rvr_data(data):

    rvr = list()
    regex = 'R[0-9]{2}[LRC]?[/](([MP]?[0-9]{4})|([0-9]{4}V[0-9]{4}))(FT)?'

    while re.fullmatch(regex, data[2]):

        temp = data.pop(2)
        di = {'R': ' right', 'L': ' left', 'C': ' center'}

        to_meter = lambda d: math.ceil(int(d) / 3.28)
        to_ft = lambda d: math.ceil(int(d) * 3.28)

        runway, vis = temp.split('/')
        di = di.setdefault(runway[-1], '')
        runway = runway[1:3]

        if re.search('[0-9]{4}V[0-9]{4}', vis):

            vis = vis.split('V')

            if vis[1].endswith('FT'):

                vis[1] = vis[1][:-2]
                mt1 = to_meter(vis[0])
                mt2 = to_meter(vis[1])

                item = f"runway {runway}{di}: {vis[0]} ft ({mt1} meters) to {vis[1]} ft ({mt2} meters)"
            else:

                ft1 = to_ft(vis[0])
                ft2 = to_ft(vis[1])

                item = f"runway {runway}{di}: {ft1} ft ({vis[0]} meters) to {ft2} ft ({vis[1]} meters)"
        else:

            lg = {'M': 'less than', 'P': 'greater than'}
            lg = lg.setdefault(vis[0], '')
            
            vis = vis[1:] if lg else vis

            if vis.endswith('FT'):
                vis = vis[:-2]
                item = f"runway {runway}{di}: {lg} {vis} ft ({to_meter(vis)} meters)"
            else:
                item = f"runway {runway}{di}: {lg} {to_ft(vis)} ft ({vis} meters)"

        rvr.append(item)

    return rvr if rvr else None


def get_weather_data(data):

    if data[2] == 'CAVOK':
        return 'OK'

    if not re.fullmatch('[+-]?([A-Z][A-Z])+', data[2]):
        return None

    data = data.pop(2)
    ind = 0

    if data[ind] == '+':
        weather = 'heavy '
        ind += 1
    elif data[ind] == '-':
        weather = 'light '
        ind += 1
    else:
        weather = 'moderate '

    if data[ind:ind+2] == 'VC':
        prox = 'in vicinity'
        ind += 2
    else:
        prox = 'on station'

    table = {
        'BC': 'patches ', 'BL': 'blowing ',  'DR': 'low drifting ', 'FZ': 'freezing ', 'MI': 'shallow ', 
        'PR': 'partial ', 'SH': 'showers ', 'TS': 'thunderstorm ', 'DZ': 'drizzle ', 'GR': 'hail ', 
        'GS': 'small hail ', 'IC': 'ice crystals ', 'PL': 'ice pellets ', 'RA': 'rain ',
        'SG': 'snow grains ', 'SN': 'snow ', 'BR': 'mist ', 'DU': 'dust ', 'FG': 'fog ', 'FU': 'smoke ',
        'HZ': 'haze ', 'PY': 'spray ', 'SA': 'sand ', 'VA': 'volcanic ash ', 'DS': 'dust storm ',
        'FC': 'funnel clouds ', 'PO': 'dust whirls ', 'SQ': 'squalls ',  'SS': 'sand storm '
    }

    for i in range(ind, len(data), 2):
        weather += table.setdefault(data[i:i+2], '')

    weather += prox

    return weather


def get_clouds_data(data):

    if data[2] == 'CAVOK':
        data.pop(2)
        return 'OK'

    clouds = list()
    to_ft = lambda h: int(h) * 100
    ty = {'FEW': 'few', 'SCT': 'scattered', 'BKN': 'broken', 'OVC': 'overcast',
          'NSC': 'no significant clouds', 'SKC': 'sky clear', 'CLR': 'clear', 'NCD': 'no clouds detected'}
    
    regex = '[A-Z]{3}([0-9]{3}([/]{3}|[A-Z]{2,3})?)?|VV[0-9]{3}'

    while re.fullmatch(regex, data[2]):
        
        temp = data.pop(2)

        if len(temp) > 3:
            
            if temp.startswith('VV'):
                clouds.append(f'vertical view of {to_ft(temp[2:])} ft')
            else:

                st = ty[temp[:3]]
                ht = temp[3:]

                if ht.endswith('CB'):
                    st += ' cumulonimbus'
                    ht = to_ft(ht[:-2])
                elif ht.endswith('TCU'):
                    st += ' towering cumulus'
                    ht = to_ft(ht[:-3])
                else:
                    ht = to_ft(ht[:3])

                clouds.append(f'{st} at {ht} ft AGL') 

        else:
            return ty[temp]

    return clouds if clouds else None


def get_temp_and_dewpoint_data(data):

    to_f = lambda t: math.ceil(int(t) * 9/5 + 32)
    
    if re.fullmatch('M?[0-9]{2}/M?[0-9]{2}', data[2]):
        
        tmp, dewp = data.pop(2).split('/')
        
        if tmp[0] == 'M':
            tmp = '-' + tmp[1:]
        
        if dewp[0] == 'M':
            dewp = '-' + dewp[1:]

        tmp = f'{tmp} C ({to_f(tmp)} F)'
        dewp = f'{dewp} C ({to_f(dewp)} F)'

        return f'temperature: {tmp}, dew point: {dewp}'

    return None


def get_air_pressure_data(data):
    
    if re.fullmatch('[AQ][0-9]{4}', data[2]):
        data = data.pop(2)
        if (data[0] == 'A'):
            return f'{data[1:3]}.{data[3:]} inches Hg'
        else:
            return f'{data[1:]} hPa'

    return None


def convert(data):

    metar_dict = dict()

    metar_dict['scode'] = data.pop(2)
    metar_dict['issued_on'] = get_issuance_data(data)
    metar_dict['observation_type'] = get_observation_data(data)
    metar_dict['wind'] = get_wind_data(data)
    metar_dict['visibility'] = get_visibility_data(data)
    metar_dict['runway_visual_range'] = get_rvr_data(data)
    metar_dict['weather'] = get_weather_data(data)
    metar_dict['clouds'] = get_clouds_data(data)
    metar_dict['temp_and_dewpoint'] = get_temp_and_dewpoint_data(data)
    metar_dict['air_pressure'] = get_air_pressure_data(data)
    metar_dict['last_observation'] = f'{data[0]} at {data[1]} GMT'

    return str(metar_dict)