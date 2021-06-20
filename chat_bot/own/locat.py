import json
from geopy.geocoders import Nominatim

class Locations:

    def __init__(self):
        self.dict_data=self.load_data()
        self.geolocator = Nominatim(user_agent="geoapiExercises")


    def load_data(self):
        with open('./resource/data.json') as json_file:
            data = json.load(json_file)
            return data

    def get_town(self, chat_id):
        Latitude=str(self.dict_data[str(chat_id)]["loc"]["latitude"])
        Longitude=str(self.dict_data[str(chat_id)]["loc"]["longitude"])
        location = self.geolocator.reverse(Latitude + "," + Longitude)
        address = location.raw['address']
        city = address.get('city', '')
        village=address.get('village', '')
        flag_village=False
        if city=="":
            flag_village=True
            print(village)
            return village, flag_village
        else:
            print(city)
            return city, flag_village

    def get_town_string(self, chat_id):
        Latitude = str(self.dict_data[str(chat_id)]["loc"]["latitude"])
        Longitude = str(self.dict_data[str(chat_id)]["loc"]["longitude"])
        location = self.geolocator.reverse(Latitude + "," + Longitude)
        address = location.raw['address']
        city = address.get('city', '')
        village = address.get('village', '')
        if city == "":
            return "прекрасной деревне "+village

        else:

            return "прекрасном городе "+city



    def get_ll(self, chat_id):
        Latitude = self.dict_data[str(chat_id)]["latitude"]
        Longitude = self.dict_data[str(chat_id)]["longitude"]
        return Latitude,Longitude



    def check_id(self, chat_id):
        return str(chat_id) in self.dict_data.keys()

    def set_location(self, chat_id, location):
        self.dict_data[str(chat_id)]={}
        self.dict_data[str(chat_id)]["loc"]=location
        self.dict_data[str(chat_id)]["w"]=False
        self.dict_data[str(chat_id)]["d"] = False
        self.dict_data[str(chat_id)]["p"] = False
        self.update()


    def set_w(self, chat_id, f=True):
        self.dict_data[str(chat_id)]["w"] = f
        self.update()

    def set_d(self, chat_id, f=True):
        self.dict_data[str(chat_id)]["d"] = f
        self.update()


    def get_w(self, chat_id):
        return self.dict_data[str(chat_id)]["w"]

    def get_d(self, chat_id):
        return self.dict_data[str(chat_id)]["d"]





    def update(self):
        with open('./resource/data.json', "w") as json_file:
            json.dump(self.dict_data, json_file)


    def print_data(self):
        print(self.dict_data)


if __name__ == "__main__":
    l=Locations()
    loc={'location': {'latitude': 55.960371, 'longitude': 93.017736}}
    print(l.check_id(393627202))
    l.set_location(123, loc['location'])
    l.print_data()
    l.get_town(393627202)

