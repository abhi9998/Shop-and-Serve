from utils import get_all_products, get_products_by_store_id, create_product, \
                    get_unique_product_name, is_product_part_of, update_status_of_product, \
                    get_id_of_product, get_unique_user_details, create_user, login_user


def test_product_flow():
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

    storeid = 3
    product = {'name': get_unique_product_name(), 
               'description': 'this is a sample sitafal', 
               'price': '3.00', 
               'brand': 'apple', 
               'imagelink': 'http://sitafla.com', 
               'weight': '2.00', 
               'active': 'Y', 
               'storeid': storeid}

    # Product shouldn't be present in response when all products are fetched.
    products = get_all_products(token=general_token)
    assert is_product_part_of(product, products) == False

    # Create product
    create_product(product, 201, token=admin_token)

    # Product should be present in response when all products are fetched.
    products = get_all_products(token=general_token)
    assert is_product_part_of(product, products) == True
    
    # Get products by its store id
    products = get_products_by_store_id(storeid, token=general_token)
    assert is_product_part_of(product, products) == True

    # Get products of another store and verify that product is present in response.
    products = get_products_by_store_id(storeid + 1, token=general_token)
    assert is_product_part_of(product, products) == False

    # Update product status to inactive
    id = get_id_of_product(product, token=general_token)
    res = update_status_of_product(id, "inactive", 204, token=admin_token)

    # It should be present when all the products of store are fetched.
    products = get_products_by_store_id(storeid, token=general_token)
    assert is_product_part_of(product, products) == True

    # It should be present when only inactive products are fetched.
    products = get_products_by_store_id(storeid, "inactive", token=general_token)
    assert is_product_part_of(product, products) == True

    # It should be absent when only active products are fetched.
    products = get_products_by_store_id(storeid, "active", token=general_token)
    assert is_product_part_of(product, products) == False

    # Update product status
    id = get_id_of_product(product, token=general_token)
    res = update_status_of_product(id, "active", 204, token=admin_token)

    # It should be present when only inactive products are fetched.
    products = get_products_by_store_id(storeid, "inactive", token=general_token)
    assert is_product_part_of(product, products) == False

    # It should be present when only active products are fetched.
    products = get_products_by_store_id(storeid, "active", token=general_token)
    assert is_product_part_of(product, products) == True

