from utils import get_all_store, get_store_info_by_id, is_store_part_of, create_store, \
                    get_unique_store_name, get_id_of_store, update_status_of_store, \
                    get_stores_by_city, get_unique_user_details, create_user, \
                    login_user
                        

def test_store_flow():
    # Create Admin User
    admin_user = get_unique_user_details()
    admin_user['is_staff'] = True
    create_user(admin_user, 201)
    res = login_user({'email': admin_user['email'], 'password': admin_user['password']}, 200)
    admin_token = res['token']

    # Create General User
    general_user = get_unique_user_details()
    create_user(general_user, 201)
    res = login_user({'email': general_user['email'], 'password': general_user['password']}, 200)
    general_token = res['token']

    city = "Waterloo"
    name = get_unique_store_name()
    address = "Farmers market"
    pincode = "ER3DFG"
    store = {"name": name, "address": address, "city": city, "pincode": pincode, "active": "Y"}

    # Get all the stores and verify store is not present already
    stores = get_all_store(token=general_token)
    assert is_store_part_of(store, stores) == False

    # Create Store
    res = create_store(store, 201, token=admin_token)

    # Get all the store and verify store is present in response.
    stores = get_all_store(token=general_token)
    assert is_store_part_of(store, stores) == True

    # Get store info by its id
    id = get_id_of_store(store, token=general_token)
    _store = get_store_info_by_id(id, token=general_token)
    assert _store["name"] == store["name"]
    assert _store["address"] == store["address"]
    assert _store["pincode"] == store["pincode"]

    # Search store using its city, it should be present as store is active.
    stores = get_stores_by_city(city, 200, token=general_token)
    assert is_store_part_of(store, stores) == True # Search by city returns only active stores.

    # Make store inactive
    update_status_of_store(id, "inactive", 204, token=admin_token)

    # Get all the store and verify store is present in response.
    stores = get_all_store(token=general_token)
    assert is_store_part_of(store, stores) == True

    # Get all the active store and verify store is absent in response.
    stores = get_all_store("active", token=general_token)
    assert is_store_part_of(store, stores) == False

    # Get all the inactive store and verify store is present in response.
    stores = get_all_store("inactive", token=general_token)
    assert is_store_part_of(store, stores) == True

    # Search store using its city, it should be absent as store is inactive.
    stores = get_stores_by_city(city, 200, token=general_token)
    assert is_store_part_of(store, stores) == False # Search by city returns only active stores.

    # Make store active
    update_status_of_store(id, "active", 204, token=admin_token)

    # Get all the active store and verify store is absent in response.
    stores = get_all_store("active", token=general_token)
    assert is_store_part_of(store, stores) == True

    # Get all the inactive store and verify store is present in response.
    stores = get_all_store("inactive", token=general_token)
    assert is_store_part_of(store, stores) == False
