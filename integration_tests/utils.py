#!/usr/bin/env python3
# 
import json
import requests
import time
from random import randrange

class client:
    # base_url = "https://ece651-sns-qa.herokuapp.com"
    base_url = "http://app:8000"

    def get(self, url, expected_status_code=None, token=None):
        headers = {
            'Content-Type': 'application/json'
        }

        if token is not None:
            headers['Authorization'] = 'Token ' + token

        response = requests.get(self.base_url + url, headers=headers)

        if expected_status_code is not None:
            assert response.status_code == expected_status_code

        return response

    def post(self, url, data, expected_status_code=None, token=None):
        headers = {
            'Content-Type': 'application/json'
        }
        if token is not None:
            headers['Authorization'] = 'Token ' + token

        response = requests.post(self.base_url + url, data=json.dumps(data), headers=headers)

        if expected_status_code is not None:
            assert response.status_code == expected_status_code

        return response

    def put(self, url, data, expected_status_code=None, token=None):
        headers = {
            'Content-Type': 'application/json'
        }
        if token is not None:
            headers['Authorization'] = 'Token ' + token
        response = requests.put(self.base_url + url, data=json.dumps(data), headers=headers)

        if expected_status_code is not None:
            assert response.status_code == expected_status_code

        return response

    def patch(self, url, data, expected_status_code=None, token=None):
        headers = {
            'Content-Type': 'application/json'
        }
        if token is not None:
            headers['Authorization'] = 'Token ' + token
        response = requests.patch(self.base_url + url, data=json.dumps(data), headers=headers)

        if expected_status_code is not None:
            assert response.status_code == expected_status_code

        return response


def get_all_store(status = None, expected_status_code = None, token=None):
    suffix = ""

    if status is not None:
        suffix = "?status=" + status

    res = client().get("/api/store/info" + suffix, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    
    return res.json() if res.status_code == 200 else res

def get_unique_store_name():
    return "Store" + str(int(time.time()))

def get_unique_product_name():
    return "product" + str(int(time.time()))

def get_store_info_by_id(id, expected_status_code = None, token=None):
    res = client().get("/api/store/info/" + str(id), token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def get_stores_by_city(city, expected_status_code = None, token=None):
    res = client().get("/api/store/info/city/" + str(city), token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def create_store(data, expected_status_code=201, token=None):
    res = client().post("/api/store/", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 201 else res

def is_store_part_of(store, stores):
    for _store in stores:
        try:
            if store['name'] == _store['name'] and \
                store['address'] == _store['address'] and \
                store['city'] == _store['city'] and \
                store['pincode'] == _store['pincode']:
                return True
        except:
            pass
    
    return False

def get_id_of_store(store, token=None):
    stores = get_all_store(token=token)

    for _store in stores:
        try:
            if store['name'] == _store['name'] and \
                store['address'] == _store['address'] and \
                store['city'] == _store['city'] and \
                store['pincode'] == _store['pincode']:
                return _store['id']
        except:
            pass
    
    return -1

def update_status_of_store(storeid, new_status, expected_status_code=None, token=None):
    data = {"makestatus": new_status}
    res = client().put("/api/store/storestatus/" + str(storeid) + "?makestatus=" + new_status, data={}, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res


def get_all_products(expected_status_code=None, token=None):
    res = client().get("/api/product/info", token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    
    return res.json() if res.status_code == 200 else res


def is_product_part_of(product, products):
    for _product in products:
        try:
            if product['name'] == _product['name'] and \
                product['storeid'] == _product['storeid'] and \
                product['brand'] == _product['brand'] and \
                product['description'] == _product['description'] and \
                product['price'] == _product['price'] and \
                product['imagelink'] == _product['imagelink']:
                return True
        except:
            pass
    
    return False


def get_products_by_store_id(storeid, status=None, expected_status_code=None, token=None):
    suffix = ""

    if status is not None:
        suffix = "?status=" + status

    res = client().get("/api/product/info/store/" + str(storeid) + str(suffix), token=token)
    
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    
    return res.json() if res.status_code == 200 else res

def create_product(data, expected_status_code=None, token=None):
    res = client().post("/api/product/", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def update_status_of_product(productid, new_status, expected_status_code=None, token=None):
    res = client().put("/api/product/productstatus/" + str(productid) + "?makestatus=" + new_status, data={}, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res


def get_id_of_product(product, token=None):
    products = get_all_products(token=token)

    for _product in products:
        try:
            if product['name'] == _product['name'] and \
                product['price'] == _product['price'] and \
                product['brand'] == _product['brand'] and \
                product['storeid'] == _product['storeid'] and \
                product['imagelink'] == _product['imagelink']:
                return _product['id']
        except:
            pass
    
    return -1

def create_order(data, expected_status_code=None, token=None):
    res = client().post("/api/order/", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 201 else res


def get_order_using_group_id(group_id, expected_status_code=None, token=None):
    res = client().get("/api/order/group/" + str(group_id), token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def get_order_using_store_id(store_id, expected_status_code=None, token=None):
    res = client().get("/api/order/store/" + str(store_id), token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def get_order_using_placer_id(placerid, expected_status_code=None, token=None):
    res = client().get("/api/order/placer/" + str(placerid), token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def get_order_using_acceptor_id(acceptorid, expected_status_code=None, token=None):
    res = client().get("/api/order/acceptor/" + str(acceptorid), token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def cancel_order(data, expected_status_code=None, token=None):
    res = client().post("/api/order/cancel", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def accept_order(data, expected_status_code=None, token=None):
    res = client().post("/api/order/accept", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 201 else res

def checkout_order(data, expected_status_code=None, token=None):
    res = client().post("/api/order/checkout", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 201 else res

def complete_order(data, expected_status_code=None, token=None):
    res = client().post("/api/order/complete", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 200 else res

def get_unique_order_description():
    return "Test order - " + str(int(time.time()))

def is_order_part_of(order, orders):
    for _order in orders:

        try:
            if str(order['orderDetails']['description']) == _order['description'] and \
               str(float(order['orderDetails']['orderamount'])) == str(float(_order['orderamount'])) and \
               str(order['orderDetails']['storeid']) == str(_order['storeid']) and \
               str(order['orderDetails']['orderedby']) == str(_order['orderedby']) and \
                str(float(order['orderDetails']['tipamount'])) == str(float(_order['tipamount'])):
                list_1 = order['orderItems']
                list_2 = _order['orderItems']
                # TODO Compare two lists
                return True
        except:
            pass
    
    return False

def get_order_id(order, orders):
    for _order in orders:

        try:
            if str(order['orderDetails']['description']) == _order['description'] and \
               str(float(order['orderDetails']['orderamount'])) == str(float(_order['orderamount'])) and \
               str(order['orderDetails']['storeid']) == str(_order['storeid']) and \
               str(order['orderDetails']['orderedby']) == str(_order['orderedby']) and \
                str(float(order['orderDetails']['tipamount'])) == str(float(_order['tipamount'])):
                list_1 = order['orderItems']
                list_2 = _order['orderItems']
                # TODO Compare two lists
                return _order["id"]
        except:
            pass
    
    return -1

def get_unique_user_details(id=1):
    random_string = str(int(time.time())) + str(id)
    data = dict()
    data['email'] = 'testemail' + random_string + '@test.com'
    data['name'] = 'testuser' + random_string
    data['mobile'] = '+1' + random_string
    data['address'] = 'test address' + random_string
    data['city'] = 'TestCity'
    data['pincode'] = 'N2M 5H3'
    data['password'] = 'supersecret' + random_string
    return data

def get_unique_group_details(id):
    random_string = str(int(time.time())) + str(id)
    data = dict()
    data['name'] = 'testgroup' + random_string
    data['description'] = 'Test Group ' + random_string
    data['city'] = 'Kitchener'
    return data

def create_user(data, expected_status_code=None):
    res = client().post("/user/create", data=data)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    return res.json() if res.status_code == 201 else res

def login_user(data, expected_status_code=None):
    res = client().post("/user/login", data=data)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    return res.json() if res.status_code == 200 else res

def get_user_profile(token, expected_status_code=None):
    res = client().get("/user/myprofile", token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    return res.json() if res.status_code == 200 else res

def update_user_profile(data, token, expected_status_code=None):
    res = client().patch("/user/myprofile", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    return res.json() if res.status_code == 200 else res

def get_all_groups(expected_status_code = None, token=None):
    res = client().get("/user/groups/", token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    
    return res.json() if res.status_code == 200 else res

def is_group_part_of(group, groups):
    if 'type' not in group:
        group['type'] = 'private'
    for _group in groups:
        try:
            if group['name'] == _group['name'] and \
                group['description'] == _group['description'] and \
                group['city'] == _group['city'] and \
                group['type'] == _group['type']:
                return True
        except:
            pass
    
    return False

def create_group(data, expected_status_code=None, token=None):
    res = client().post("/user/groups/", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    return res.json() if res.status_code == 201 else res

def get_my_groups(token, expected_status_code=None):
    res = client().get("/user/mygroups", token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"
    return res.json() if res.status_code == 200 else res

def join_group(data, expected_status_code=None, token=None):
    res = client().post("/user/joinGroup/", data=data, token=token)
    if expected_status_code is not None:
        assert res.status_code == expected_status_code, f"{res.status_code} instead of {expected_status_code}"

    return res.json() if res.status_code == 201 else res

def get_id_of_group(group, token=None):
    groups = get_all_groups(token=token)

    for _group in groups:
        try:
            if group['name'] == _group['name'] and \
                group['description'] == _group['description'] and \
                group['city'] == _group['city'] and \
                group['type'] == _group['type']:
                return _group['id']
        except:
            pass
    
    return -1