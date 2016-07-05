import zipfile, yaml

def get_all_matches_yaml_list():
    zf = zipfile.ZipFile('all.zip', 'r')
    return zf.namelist()

def read_file_in_zip(filename):
    zf = zipfile.ZipFile('all.zip', 'r')
    if filename in ("README.txt"):
        data = zf.read(filename)
        return data
    else:
        try:
            data = yaml.safe_load(zf.read(filename))
            return data
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
        else:
            print(filename, ':')
            print(repr(data))
        print

def get_city(filename):
    try:
        return read_file_in_zip(filename)["info"]["city"]
    except:
        pass

def get_all_cricket_cities():
    return [get_city(filename) for filename in get_all_matches_yaml_list()]

def print_city_names():
    for filename in get_all_matches_yaml_list()[2500:3500]: # there are around 3200 fields
        print(get_city(filename))


def create_xdata_ydata():
    for file in get_all_matches_yaml_list():
        data = read_file_in_zip(file)
        """
        do voodoo and magic
        i m kidding of course
        write the necassary code
        """
        yield data_vector

if __name__ == "__main__":
    print_city_names()
