from utils import complete_order, create_order, get_order_id, get_unique_order_description, \
                get_order_using_group_id, get_order_using_store_id, \
                get_order_using_placer_id, get_order_using_acceptor_id, \
                cancel_order, is_order_part_of, accept_order, checkout_order, \
                get_unique_user_details, login_user, create_user

# TODO - when your tries make order above than the wallet amount

# Create General User
general_user = get_unique_user_details()
create_user(general_user, 201)
res = login_user({'email': general_user['email'], 'password': general_user['password']}, 200)
general_token = res['token']

def test_order_flow_to_complete_order():
    description = get_unique_order_description()
    placerid = 4
    storeid = 3
    acceptorid = 2
    order = {
        "orderDetails":{
            "orderedby": placerid,
            "storeid": storeid,
            "description": description,
            "tipamount": 2,
            "orderamount": 10
        },

        "orderItems":[
            {
                "productid": 3,
                "quantity": 2,
                "price": 5
            },
            {
                "productid":4,
                "quantity": 1,
                "price": 5
            }
        ],
        "group":[1]   
    }

    # # Create order
    res = create_order(order, 201, token=general_token)
    
    # # Get order using group id
    orders = get_order_using_group_id(1, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Get order using store id
    orders = get_order_using_store_id(storeid, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Get order using placer id
    orders = get_order_using_placer_id(placerid, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Accept order
    orderid = get_order_id(order, orders)
    accept_order({"orderid": orderid, "acceptorid": acceptorid}, expected_status_code=201, token=general_token)
    
    # Get order using acceptor id
    orders = get_order_using_acceptor_id(acceptorid, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Checkout order
    checkout_order({"orderid": orderid, "acceptorid": acceptorid}, 201, token=general_token)
    
    # Complete order
    complete_order({"orderid": orderid, "acceptorid": acceptorid, "placerid": placerid}, 201, token=general_token)


def test_order_flow_to_cancel_order():
    description = get_unique_order_description()
    placerid = 2
    acceptorid = 1
    order = {
        "orderDetails":{
            "orderedby": placerid,
            "storeid": 3,
            "description": description,
            "tipamount": 2,
            "orderamount": 10
        },

        "orderItems":[
            {
                "productid": 3,
                "quantity": 2,
                "price": 5
            },
            {
                "productid":4,
                "quantity": 1,
                "price": 5
            }
        ],
        "group":[1]   
    }

    # # Create order
    create_order(order, token=general_token)
    
    # # Get order using group id
    orders = get_order_using_group_id(1, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Get order using store id
    orders = get_order_using_store_id(3, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Get order using placer id
    orders = get_order_using_placer_id(placerid, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Accept order
    orderid = get_order_id(order, orders)
    accept_order({"orderid": orderid, "acceptorid": acceptorid}, expected_status_code=201, token=general_token)
    
    # Get order using acceptor id
    orders = get_order_using_acceptor_id(acceptorid, token=general_token)
    assert is_order_part_of(order, orders) == True

    # Cancel the order
    orderid = get_order_id(order, orders)
    rejectorid = placerid    
    cancel_order({"orderid": orderid, 'rejectorid': rejectorid}, 201, token=general_token) # TODO why rejector id matters in Cancel order
    