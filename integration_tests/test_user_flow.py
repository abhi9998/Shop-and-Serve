from utils import get_unique_user_details, create_user, login_user, get_user_profile, \
                    update_user_profile

user = get_unique_user_details()
token = None

def test_user_create():
    """Test user creation"""
    # Create a user
    res = create_user(user, 201)
    assert res['email'] == user['email']
    assert res['name']  == user['name']
    assert res['mobile']  == user['mobile']
    assert res['address']  == user['address']
    assert res['city'] == user['city']
    assert res['pincode'] == user['pincode']
    assert 'password' not in res

def test_user_login():
    """Login user and get the token"""
    global token
    res = login_user({'email': user['email'], 'password': user['password']}, 200)
    assert 'token' in res
    token = res['token']
    assert res['name'] == user['name']
    assert res['email'] == user['email']

def test_get_user_profile():
    """Test get user profile"""
    res = get_user_profile(token=token, expected_status_code=200)
    assert res['email'] == user['email']
    assert res['name']  == user['name']
    assert res['mobile']  == user['mobile']
    assert res['address']  == user['address']
    assert res['city'] == user['city']
    assert res['pincode'] == user['pincode']
    assert 'password' not in res

def test_update_user_profile():
    """Test update user profile"""
    global user
    data = {"name": 'Updated '+user['name'], "address": 'Updated '+user['address']}
    res = update_user_profile(data=data, token=token, expected_status_code=200)
    assert res['email'] == user['email']
    assert res['name']  ==  'Updated ' + user['name']
    assert res['mobile']  == user['mobile']
    assert res['address']  == 'Updated ' + user['address']
    assert res['city'] == user['city']
    assert res['pincode'] == user['pincode']
    assert 'password' not in res

    user['name'] = 'Updated ' + user['name']
    user['address'] = 'Updated '+user['address']