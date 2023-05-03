#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one user
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/users")
    r_j = r.json()
    user_id = r_j[0].get('id')

    """ PUT /api/v1/users/<user_id>
    """
    r = requests.put("http://0.0.0.0:5050/api/v1/users/{}".format(user_id), data=json.dumps({ 'first_name': "newfirstname" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') == user_id)
    print(r_j.get('first_name') == "newfirstname")

    """ Verify if the state is updated
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/users")
    r_j = r.json()
    for user_j in r_j:
        if user_j.get('id') == user_id:
            print(user_j.get('first_name') == "newfirstname")
