import zipfile, yaml
import numpy as np

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

def give_delivery_info(delivery):
    for ball, ball_info in delivery.items():
        over_info = [ball] + [ball_info["runs"]["batsman"]] + \
                        [ball_info["runs"]["extras"]] + \
                        [ball_info["runs"]["total"]]
        try:
            if ball_info["wicket"]:
                over_info += [1]
        except KeyError:
            over_info += [0]
        return over_info

def handle_ind_innings(ind_innings):
    delivery_info_list = []
    for k, v in ind_innings.items():
        deliveries = v["deliveries"]
        for delivery in deliveries:
            delivery_info_list.append(give_delivery_info(delivery))
    return delivery_info_list

def get_all_overs_data(filename):
    deliveries = []
    both_innings = read_file_in_zip(filename)["innings"]
    for ind_innings in both_innings:
        deliveries += handle_ind_innings(ind_innings)
    return deliveries

def get_all_cricket_cities():
    return [get_city(filename) for filename in get_all_matches_yaml_list()]

def print_city_names():
    for filename in get_all_matches_yaml_list()[2500:3500]: # there are around 3200 fields
        print(get_city(filename))


if __name__ == "__main__":
        print(get_all_overs_data("913629.yaml"))
