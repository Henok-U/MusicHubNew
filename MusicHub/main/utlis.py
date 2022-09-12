def trim_spaces_from_data(data):
    for key, value in data.items():
        data[key] = " ".join(value.split())
    return data
