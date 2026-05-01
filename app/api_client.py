import requests

BASE_URL = "https://www.dnd5eapi.co/api"

def get_monsters():
    response = requests.get(f"{BASE_URL}/monsters")
    return response.json().get("results", [])

def get_spells():
    response = requests.get(f"{BASE_URL}/spells")
    return response.json().get("results", [])

def get_equipment():
    response = requests.get(f"{BASE_URL}/equipment")
    return response.json().get("results", [])

def get_details(category, index):
    response = requests.get(f"{BASE_URL}/{category}/{index}")
    return response.json()
