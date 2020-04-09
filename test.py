import googlemaps
import pprint
import time
import random

# google places api
google_api = 'AIzaSyBXJT4-6to3js5aUnNsqcCdiSmBkPTb5Tk'

# # define our client
gmaps = googlemaps.Client(key=google_api)


def radius_search(lat, long, radius, type):
    locations = []
    final = {}
    my_fields = ['name', 'formatted_address', 'geometry', 'url']
    location = lat + ',' + long

    results = gmaps.places_nearby(location=location, radius=radius, open_now=False, type=type, keyword='-"fast food" (restaurant)')

#   NOTES:
#       - results['results][x]['price_level] is optional, not all restaurants have one
#       - only 20 results per page, 3 pages total allowed; max = 60 results
#       - we want open_now=True but because of Corona virus we leave that False in the meantime

    while True:
        # counter += len(results['results'])
        try:
            # loops through the api and appends restaurants names to a list
            for x in range(len(results['results']) + 1):
                if x != (len(results['results'])):
                    if results['results'][x]['rating'] >= 3.5:
                        locations.append(
                            {'place_id': results['results'][x]['place_id'],
                             'total_reviews': results['results'][x]['user_ratings_total']})
                        print(results['results'][x]['name'])
                else:
                    # required
                    time.sleep(2.5)
                    results = gmaps.places_nearby(page_token=results['next_page_token'])
        # final page, breaks the loop.
        except:
            break

    # randomly choices a restaurant
    for key, value in random.choice(locations).items():
        final[key] = value

    # detail search of the restaurant
    pprint.pprint(locations)
    place_details = gmaps.place(place_id=final['place_id'], fields=my_fields)

    # loops through the results and appends the items
    for key, value in place_details['result'].items():
        final[key] = value

    return final


lat = '41.0513855'
long = '-73.5441102'
radius = 1000
counter = 0
type_of = 'restaurant'

pprint.pprint(radius_search(lat, long, radius, type_of))
