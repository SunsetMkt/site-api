# https://this-person-does-not-exist.com/
import time

import requests

BASE_URL = 'https://this-person-does-not-exist.com'

genders = ['all', 'male', 'female']
ages = ['all', '12-18', '19-25', '26-35', '35-50', '50']
etnics = ['all', 'asian', 'black', 'white',
          'indian', 'middle_eastern', 'latino_hispanic']


def new(gender='all', age='all', etnic='all'):
    # Check if parameters are valid
    if gender not in genders or age not in ages or etnic not in etnics:
        raise ValueError(
            'Invalid parameters: gender={}, age={}, etnic={}'.format(
                gender, age, etnic
            )
        )

    params = {
        'time': str(time.time()),
        'gender': gender,
        'age': age,
        'etnic': etnic,
    }

    response = requests.get(BASE_URL + '/new', params=params)

    response.raise_for_status()

    response = response.json()

    if response['generated'] == 'true':
        return BASE_URL + response['src']
    else:
        raise Exception("Remote server returned error.")


def get(gender, age, etnic):
    url = new(gender, age, etnic)
    response = requests.get(url)
    response.raise_for_status()
    return response.content


if __name__ == '__main__':
    print(new())
