def convert_bytes(n, units='B'):
    if units == 'GB':
        return {'value': n / 1000 / 1000 / 1000, 'units': 'GB'}
    elif units == 'MB':
        return {'value': n / 1000 / 1000, 'units': 'MB'}
    else:
        return {'value': n, 'units': 'B'}
