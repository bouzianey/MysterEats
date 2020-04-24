#google search

import urllib.request, json
from random import randrange
from googlemaps import Client
from MysterEats_App.decorators import *
import time

# #flask mail
# from flask_mail import Message
# from .decorators import async_
# from flask_mail import Mail
# from config import ADMINS


class RestaurantDirections:

    def __init__(self, att1, att2, att3):
        self.distance = att1
        self.duration = att2
        self.steps = att3

    def get_distance(self):
        return self.distance

    def get_duration(self):
        return self.duration

    def get_steps(self):
        return self.steps


class SearchRestaurant:

    def __init__(self, att1, att2, att3):
        self.location = att1
        self.preference = att2
        self.radius = att3

    def get_location(self):
        return self.location

    def get_preference(self):
        return self.preference

    def get_radius(self):
        return self.radius

    def get_current_location(self):

        gmaps = Client(key='AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk')
        origin = gmaps.geolocate()
        return str(origin['location']['lat'])+','+str(origin['location']['lng'])

    def get_best_restaurant(self):

        gmaps = Client(key = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk')
        endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'

        #assign inputs
        api_key = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk'
        type='restaurant'

        # TODO Implementation
        # if DisplayForm.data == 'vegan':
        #     preference = str('vegan').replace(' ', '+')
        # if DisplayForm.data == 'bar-restaurants':
        #     preference = str('bar-restaurants').replace(' ', '+')
        # if DisplayForm.data == 'group':
        #     preference = str('group').replace(' ', '+')
        # if DisplayForm.data == 'family':
        #     preference = str('family').replace(' ', '+')
        # # preference = str(preference).replace(' ','+')
        # location = str(location).replace(' ', '')
        # preference = preference + "+in+" + location

        # TODO Implementation
        # # Building the URL for the request
        # if DisplayForm.data == 'maxprice1':
        #     nav_request = 'query={}&location={}&radius={}&type={}&maxprice=1&key={}'.format(preference, location,
        #                                                                                     radius, type, api_key)
        # elif DisplayForm.data == 'maxprice2':
        #     nav_request = 'query={}&location={}&radius={}&type={}&maxprice=2&key={}'.format(preference, location,
        #                                                                                     radius, type, api_key)
        # elif DisplayForm.data == 'maxprice3':
        #     nav_request = 'query={}&location={}&radius={}&type={}&maxprice=3&key={}'.format(preference, location,
        #                                                                                     radius, type, api_key)
        # elif DisplayForm.data == 'maxprice4':
        #     nav_request = 'query={}&location={}&radius={}&type={}&maxprice=4&key={}'.format(preference, location,
        #                                                                                     radius, type, api_key)
        # else:
        #     nav_request = 'query={}&location={}&radius={}&type={}&key={}'.format(preference, location, radius, type,
        #                                                                          api_key)
        # request = endpoint + nav_request

        preference = str(self.preference).replace(' ','+')
        location =  str(self.location).replace(' ','')
        preference = preference +"+in+"+ location
        radius = self.radius

        #Building the URL for the request
        nav_request = 'query={}&location={}&radius={}&type={}&key={}'.format(preference,location,radius,type,api_key)
        request = endpoint + nav_request
        #Sends the request and reads the response.
        response = urllib.request.urlopen(request).read()
        #Loads response as JSON
        places_result = json.loads(response)

        print(places_result.keys())
        print(len(places_result['results']))

        stored_results = []
        counter=0
        while counter < 3:

            # loops through the api and appends restaurants to a list
            for x in range(20):
                my_place_id = places_result['results'][x]['place_id']
                # define the fields you would liked return. Formatted as a list.
                my_fields = ['name','formatted_address','geometry']
                # make a request for the details.
                places_details  = gmaps.place(place_id= my_place_id , fields= my_fields)
                # store the results in a list object.
                stored_results.append(places_details['result'])

            if counter < 2:
                # required
                time.sleep(1)
                token=places_result['next_page_token']
                #nav_request
                nav_request = 'key={}&pagetoken={}'.format(api_key,token)
                request = endpoint + nav_request
                #Sends the request and reads the response.
                response = urllib.request.urlopen(request).read()
                #Loads response as JSON
                places_result = json.loads(response)
                # final page, breaks the loop.
            counter=counter+1

        random_number=randrange (1,60,1)
        #store in database
        return stored_results[random_number]


class Directions:

    def __init__(self, att1, att2):
        self.origin = att1
        self.destination = att2

    def get_origin(self):

        API_KEY = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk'
        # Define the Client
        gmaps = Client(key = API_KEY)
        location = gmaps.geolocate()
        return str(location['location']['lat'])+','+ str(location['location']['lng'])

    def get_destination(self):
        return self.destination

    def get_directions(self):

        self.origin = self.get_origin()
        # Google MapsDdirections API endpoint
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        api_key = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk'

        # Building the URL for the request
        nav_request = 'origin={}&destination={}&key={}'.format(self.origin, self.destination, api_key)
        request = endpoint + nav_request
        # Sends the request and reads the response.
        response = urllib.request.urlopen(request).read()
        # Loads response as JSON
        directions = json.loads(response)
        routes = directions['routes']
        rt = routes[0].keys()
        # dict_keys(['bounds', 'copyrights', 'legs', 'overview_polyline', 'summary', 'warnings', 'waypoint_order'])
        # we're only concerned to use legs object since it has the most of the information we're looking for.
        legs = routes[0]['legs']
        # retrieve the distance toward the destination
        distance = legs[0]['distance']['text']
        # retrieve the duration toward the destination
        duration = legs[0]['duration']['text']
        # it shows each step we need to follow to get to our destination.
        steps = legs[0]['steps']

        for each_step in steps:
            each_step['html_instructions'] = each_step['html_instructions'].replace('<b>',' ')
            each_step['html_instructions'] = each_step['html_instructions'].replace('</b>',' ')
            each_step['html_instructions'] = each_step['html_instructions'].replace('<div style="font-size:0.9em">',' ')
            each_step['html_instructions'] = each_step['html_instructions'].replace('</div>',' ')
            each_step['html_instructions'] = each_step['html_instructions'].replace('< /<wbr/>',' ')

        return RestaurantDirections(distance,duration,steps)


class Uber:

    def __init__(self, att1,att2,att5,att3,att4,att6):

        self.pickup_lat = att1
        self.pickup_lng = att2
        self.dropoff_lat = att3
        self.dropoff_lng = att4
        self.pickup_address = att5
        self.dropoff_address = att6

    def get_origin_latlng(self):

        API_KEY = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk'
        # Define the Client
        gmaps = Client(key = API_KEY)
        origin = gmaps.geolocate()
        self.pickup_lat = str(origin['location']['lat'])
        self.pickup_lng = str(origin['location']['lng'])

    def get_origin_address(self):

        API_KEY = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk'
        # Define the Client
        gmaps = Client(key = API_KEY)
        location = self.pickup_lat +','+ self.pickup_lng
        pickup_location = gmaps.reverse_geocode(latlng=location)
        self.pickup_address = pickup_location[0]['formatted_address']

    def get_uber_link(self):

        self.get_origin_latlng()
        self.get_origin_address()

        uber_link = "https://m.uber.com/?client_id=%3cM9yCaX27ONKk3AxK4YkQZ5MiESVvKT1f%3e"
        uber_link = uber_link + "&action=setPickup"
        uber_link = uber_link + "&pickup%5blatitude%5d=" + str(self.pickup_lat)
        uber_link = uber_link + "&pickup%5blongitude%5d=" + str(self.pickup_lng)
        uber_link = uber_link + "&pickup%5bnickname%5d=Current%20Location"
        self.pickup_address = str(self.pickup_address).replace(" ","%20")
        self.pickup_address = str(self.pickup_address).replace(",","%2C")
        uber_link = uber_link + "&pickup%5bformatted_address%5d=" + self.pickup_address
        uber_link = uber_link + "&dropoff%5blatitude%5d=" + str(self.dropoff_lat)
        uber_link = uber_link + "&dropoff%5blongitude%5d=" + str(self.dropoff_lng)
        uber_link = uber_link + "&dropoff%5bnickname%5d=Secret"
        self.dropoff_address = str(self.dropoff_address).replace(" ","%20")
        self.dropoff_address = str(self.dropoff_address).replace(",","%2C")
        uber_link = uber_link + "&dropoff%5bformatted_address%5d=" + self.dropoff_address

        return uber_link


# class Email:
#     @async_
#     def send_async_email(app, msg):
#         with app.app_context():
#             mail.send(msg)
#
#     def send_email(sender, recipients):
#         subject = 'Invitation to join a meeting'
#         msg = Message(subject, sender=sender, recipients=recipients)
#         send_async_email(app, msg)
