import json
class Bus:
    def __init__(self, bus_id, stop_id, stop_name, next_stop, stop_type, a_time):
        self.bus_id = bus_id

        self.stop_id = stop_id

        self.stop_name = stop_name

        self.next_stop = next_stop

        self.stop_type = stop_type

        self.a_time = a_time

        self.stop_type_counter = 0
    def special_stops(self, start, transfer, finish):
        self.start = start
        self.transfer = transfer
        self.finish = finish


    def check_stop_type(self):
        if self.stop_type == "":
            pass
        elif self.stop_type == "S" or self.stop_type == "O" or self.stop_type == "F":
            pass
        else:
            self.stop_type_counter += 1



def initiate_list(bus_list_string):
    bus_list = []
    i = 0
    while i < len(bus_list_string):
        bus_element = ""
        if bus_list_string[i] == "{":
            while bus_list_string[i] != "}":
                bus_element += bus_list_string[i]
                i += 1
            bus_element += bus_list_string[i]
            bus_list.append(bus_element)
        i+=1
    return bus_list


def create_better_json(bus_ids, data_json):
    json_string="{"
    for id in bus_ids:
        json_string += f"{str(id)}:"
        json_string += "["
        for item in data_json:
            if str(item["bus_id"]) == id:
                json_string += f"{str(item)}"
                json_string += ", "
        json_string = json_string[:-2]
        json_string +="], "
    json_string = json_string[:-2]
    json_string += "}"
    new_json_obj = json.dumps(json_string)
    return(new_json_obj)


def init_class_get_ids(bus_list, data_json):
    index = 1
    bus_id_list=[]
    for bus in bus_list:
        bus_dict = eval(bus)
        globals()[f"bus{index}"] = Bus(bus_dict.get("bus_id"),bus_dict.get("stop_id"),bus_dict.get("stop_name"),bus_dict.get("next_stop"),bus_dict.get("stop_type"),bus_dict.get("a_time"))
        bus_id_list.append(globals()[f"bus{index}"].bus_id)

    bus_ids = ""
    for id in bus_id_list:
        if bus_ids.find(str(id)) == (-1):
            bus_ids += f"{str(id)} "
    bus_ids = bus_ids[:-1]
    bus_ids = bus_ids.split(" ")
    return bus_ids

def alpha_sort(list):
    return sorted(list)

def check_bus_lines(new_json_obj, get_transfer):
    start_stops = []
    street_dict = {"Sesame Street":set(), "Fifth Avenue":set(), "Sunset Boulevard":set(), "Elm Street":set(), "Bourbon Street":set(), "Prospekt Avenue":set(), "Pilotow Street":set(), "Abbey Road":set(), "Santa Monica Boulevard":set(), "Beale Street":set(), "Startowa Street":set(), "Lombard Street":set(), "Orchard Road":set(), "Khao San Road":set(), "Michigan Avenue":set(), "Arlington Road":set(), "Parizska Street":set(), "Niebajka Avenue":set(), "Jakis Street":set(), "Jakas Avenue":set(), "Karlikowska Avenue":set()}
    transfer_stops = []
    finish_stops = []
    loaded = json.loads(new_json_obj)
    loaded = eval(loaded)
    failure = False
    failure_line = 0
    for bus_id in loaded:
        S_counter = 0
        F_counter = 0
        for stop_instance in loaded[bus_id]:
            stop_name = stop_instance["stop_name"]
            if stop_instance["bus_id"] not in street_dict[stop_name]:
                (street_dict[stop_name]).add(stop_instance["bus_id"])
            if stop_instance["stop_type"] == "S":
                S_counter += 1
                exist = False
                for element in start_stops:
                    if element == stop_name:
                        exist = True
                if(exist == False):
                    start_stops.append(stop_name)
            elif stop_instance["stop_type"] == "F":
                F_counter += 1
                exist = False
                for element in finish_stops:
                    if element == stop_name:
                        exist = True
                if(exist == False):
                    finish_stops.append(stop_name)

        if (S_counter>1 or F_counter>1) or (S_counter == 0 or F_counter == 0):
            failure = True
            failure_line = bus_id
            break

    for street in street_dict:
        if len(street_dict[street]) > 1:
            transfer_stops.append(street)
    start_stops = alpha_sort(start_stops)
    transfer_stops = alpha_sort(transfer_stops)
    finish_stops = alpha_sort(finish_stops)
    """if failure == True:
        print(f"There is no start or end stop for the line: {failure_line}.")
    else:
        print(f"Start stops: {len(start_stops)} {start_stops}")
        print(f"Transfer stops: {len(transfer_stops)} {transfer_stops}")
        print(f"Finish stops: {len(finish_stops)} {finish_stops}")"""
    if get_transfer == True:
        return transfer_stops



def check_arrival_times(new_json_obj):
    print("Arrival time test:")
    loaded = json.loads(new_json_obj)
    loaded = eval(loaded)
    total_fails = 0
    for bus_id in loaded:
        failure = False
        cached = "None"
        for stop_instance in loaded[bus_id]:
            if cached == "None":
                pass
                cached = stop_instance["a_time"]
            elif cached!="None" and failure==False:
                current_time = stop_instance["a_time"]
                current_hour = int(current_time[0:2])
                current_minute = int(current_time[3:])
                cached_hour = int(cached[0:2])
                cached_minute = int(cached[3:])
                if current_hour > cached_hour:
                    pass
                elif current_hour < cached_hour:
                    failure = True
                    failure_id = bus_id
                    failure_stop = stop_instance["stop_name"]
                    total_fails += 1
                elif (current_hour == cached_hour) and (current_minute > cached_minute):
                    pass
                elif (current_hour == cached_hour) and (current_minute < cached_minute):
                    failure = True
                    failure_id = bus_id
                    failure_stop = stop_instance["stop_name"]
                    total_fails += 1
                cached = current_time
            elif failure == True:
                pass
        if failure == True:
            print(f"bus_id line {failure_id}: wrong time on {failure_stop}")
    if total_fails == 0:
        print("OK")

def intersect_list(list1, list2):
    intersect = set()
    for element_one in list1:
        for element_two in list2:
            if element_two == element_one:
                if (element_one in intersect) == False:
                    intersect.add(element_one)


    return intersect


def check_on_demand(new_json_obj, transfer_stops):
    print("On demand stops test:")
    loaded = json.loads(new_json_obj)
    loaded = eval(loaded)
    on_demand_stops = []
    for bus_id in loaded:
        for stop_instance in loaded[bus_id]:
            if stop_instance["stop_type"] == "O":
                on_demand_stops.append(stop_instance["stop_name"])
    fail_list = list(intersect_list(transfer_stops, on_demand_stops))
    if len(fail_list) == 0:
        print("OK")
    else:
        final_str = "Wrong stop type: ["
        for element in fail_list:
            final_str += f"'{element}', "
        final_str = final_str[:-2]
        final_str += "]"
        print(final_str)



#MAIN PROGRAM
data_raw = input()
data_json = json.loads(data_raw)
bus_list = initiate_list(data_raw)
bus_ids_list = init_class_get_ids(bus_list, data_json)
new_json_obj = create_better_json(bus_ids_list, data_json)
transfer_stops = check_bus_lines(new_json_obj, True)
check_on_demand(new_json_obj, transfer_stops)
