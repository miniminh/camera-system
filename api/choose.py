camera_choice = ['male', 'female']

def make_choice(gender):
    if gender['m'] > gender['f']:
        return camera_choice[0]
    else: 
        return camera_choice[1]