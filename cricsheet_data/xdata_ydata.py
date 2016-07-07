import re, json, zipfile

from organise_retrieved_data import get_all_matches_yaml_list, get_city

def get_relevant_data(line):
    date_match=re.search(r'(\d+\-\d+\-\d+)',line)
    if date_match:
        date_match_text = date_match.group(1)
        return date_match_text.replace("-", "")

    float_match=re.search(r'(\d+\.\d+)',line)
    if float_match:
        float_match_text = float_match.group(1)
        return float_match_text

    num_match = re.search(r'(\d+)',line)
    if num_match:
        num_match_text = num_match.group(1)
        return num_match_text

def get_lat_lng(city):
    with open("city_lat_lon.txt") as f:
        data = json.load(f)
        return data[city]


def create_xdata_ydata_per_over(file):
    zf = zipfile.ZipFile('all.zip', 'r')
    f = str(zf.read(file)).split("\\n")
    city_coordinates = get_lat_lng(get_city(file))
    dataset = [x for x in city_coordinates]
    for line in f:
        dataset.append(get_relevant_data(line))
    dataset = [float(x) for x in dataset if x is not None]
    return dataset

def get_dataset():
    for file in get_all_matches_yaml_list()[0:10]:
        if file != "README.txt":
            print(create_xdata_ydata(file))

if __name__ == "__main__":
    get_dataset()
