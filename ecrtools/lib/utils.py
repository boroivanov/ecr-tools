def convert_bytes(n, units='B'):
    if units == 'GB':
        return {'value': n / 1000 / 1000 / 1000, 'units': 'GB'}
    elif units == 'MB':
        return {'value': n / 1000 / 1000, 'units': 'MB'}
    else:
        return {'value': n, 'units': 'B'}


def split_list(list_to_split, chunk_size=100):
    n = chunk_size
    lst = list_to_split
    return [lst[i * n:(i + 1) * n] for i in range((len(lst) + n - 1) // n)]
