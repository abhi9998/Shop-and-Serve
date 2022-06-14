from venv import create
from utils import create_group, create_user, get_unique_group_details, get_unique_user_details, \
                    login_user, get_all_groups, is_group_part_of, get_my_groups,  get_id_of_group, \
                    join_group

public_group = get_unique_group_details(1)
private_group = get_unique_group_details(2)

# Create users for group operations
group_admin_user = get_unique_user_details(1)
group_admin_token = None
general_user = get_unique_user_details(2)
general_user_token = None

def test_group_flow():
    """Test creating a new group"""
    #### USER CREATION ####
    # Admin user creates a new group
    create_user(group_admin_user)
    global group_admin_token
    res = login_user({'email': group_admin_user['email'], 'password': group_admin_user['password']}, 200)
    group_admin_token = res['token']

    # General user to get all groups
    create_user(general_user)
    global general_user_token
    res = login_user({'email': general_user['email'], 'password': general_user['password']}, 200)
    general_user_token = res['token']

    #### GROUP CREATION ####
    # Get all groups
    groups = get_all_groups(token=general_user_token)
    assert len(groups) > 0

    # Check that admin user is part of no groups
    mygroups = get_my_groups(token=group_admin_token)
    assert len(mygroups) == 0

    # Check if the private group is not already in all groups
    assert is_group_part_of(private_group, groups) == False

    # Create private group
    res = create_group(private_group, 201, token=group_admin_token)
    assert 'id' in res
    assert res['name'] == private_group['name']
    assert res['type']  == 'private' # Deafult group type is private
    assert res['description']  == private_group['description']
    assert res['city']  == private_group['city']
    assert 'createdat' in res    

    # Get all groups and verify this private group is already present
    groups = get_all_groups(token=general_user_token)
    assert is_group_part_of(private_group, groups) == True

    global public_group
    # Check if the public group is not already in all groups
    assert is_group_part_of(public_group, groups) == False

    # Create a public group
    public_group['type'] = 'public'
    res = create_group(public_group, 201, token=group_admin_token)
    assert 'id' in res
    assert res['name'] == public_group['name']
    assert res['type']  == 'public'
    assert res['description']  == public_group['description']
    assert res['city']  == public_group['city']
    assert 'createdat' in res

    # Check if public group is present in all groups
    groups = get_all_groups(token=general_user_token)
    assert is_group_part_of(public_group, groups) == True

    #### GET ALL MY GROUPS - ADMIN ####
    # Check if admin user is part of two groups that he created
    mygroups = get_my_groups(token=group_admin_token)
    assert len(mygroups) == 2

    # Check that general user is part of no groups
    mygroups = get_my_groups(token=general_user_token)
    assert len(mygroups) == 0

    #### REQUEST To Join Group - PUBLIC ####
    public_group_id = get_id_of_group(public_group, token=general_user_token)
    assert public_group_id > 0

    join_group({'groupid': public_group_id}, expected_status_code=201, token=general_user_token)
    
    # Check that general user is part of one group
    mygroups = get_my_groups(token=general_user_token)
    assert len(mygroups) == 1

    #### Request to Join Group - PRIVATE ####
    private_group_id = get_id_of_group(private_group, token=general_user_token)
    assert private_group_id > 0

    join_group({'groupid': private_group_id}, expected_status_code=201, token=general_user_token)
    # Check for no entry in mygroups - as invite sent
    mygroups = get_my_groups(token=general_user_token)
    assert len(mygroups) == 1