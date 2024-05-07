# print('are we here?')
# from app.global_enums import *
# from app.database.models import (Event, EventSeeker)
# from main import x

import tensorflow as tf
import os

# Get the current directory
current_directory = os.getcwd()

 
loaded_model = tf.keras.models.load_model(os.path.join(current_directory, 'Recommendation_model'))


def predicting(seeker, events):
    titles = []
    categories = []
    types = []
    descriptions = []
    frequencies = []
    genders = []
    prices = []
    seeker_id = []
    category_lists = []
    organizer_ids = []
    start_dates = []
    end_dates = []
    dobs = []
    event_ids = []
    seeker_id.append(seeker.seeker_id)
    genders.append(seeker.gender)
    dobs.append(int(seeker.dob.toordinal()))
    seeker_id = seeker_id * len(events)
    if seeker.category_list !=[]:
        category_lists.append(seeker.category_list)
    else:
        category_lists.append('sports,automotive,entertainment,agriculture,photography,gaming,adventure,food,music,business,fashion,community,literature,health,arts,education,architecture'.split(','))
        
    category_lists = category_lists * len(events)
    genders = genders * len(events)
    dobs = dobs * len(events)

    for event in events:
        event_ids.append(int(event.event_id))
        titles.append(event.title)
        categories.append(event.category)
        types.append(event.type)
        descriptions.append(event.description)
        frequencies.append(event.frequency)
        start_dates.append(int(event.start_date.toordinal()))
        end_dates.append(int(event.end_date.toordinal()))
        prices.append(float(event.price))
        organizer_ids.append(int(event.organizerId))

    ragged_category_lists = tf.ragged.constant(category_lists)

    samples = {
        'title': titles,
        'category': categories,
        'event_type': types,
        'frequency': frequencies,
        'gender': genders,
        'price': prices,
        'seeker_id': seeker_id,
        'category_list': ragged_category_lists,  # Use the ragged tensor
        'organizer_id': organizer_ids,
        'start_date': start_dates,
        'end_date': end_dates,
        'description': descriptions,
        'dob': dobs
    }
    sample_dataset = tf.data.Dataset.from_tensor_slices(samples).batch(len(titles)).take(1)
    predictions = loaded_model.predict(sample_dataset)
    events_dict = {}
    counter = 0
    set_rate = set()
    for i in predictions:
        set_rate.add(i[0])
        events_dict[i[0]] = events[counter].event_id
        
        counter += 1

    sorted_predictions = sorted(events_dict.keys(), reverse=True)
    events_predicted = [events_dict[x] for x in sorted_predictions]
    
    return events_predicted[:min(len(events), 10)]



