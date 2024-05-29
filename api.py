# from resources.products import get_products, add_product, get_product, update_product, delete_product
# from resources.orders import get_orders, add_order, get_order
from resources.alarms import create_alarm, delete_alarm, get_alarm, get_alarms, update_alarm
from resources.auth import authenticate
from resources.users import add_user, delete_user, get_user, get_users, update_user

def handler(event, context):
    method = event['httpMethod']
    path = event['path']
    response = {}

    print(f"Event: {event}")
    
    if method == 'GET' and path == '/users':
        return get_users(event)
    elif method == 'GET' and path.startswith('/users/'):
        return get_user(event)
    elif method == 'POST' and path == '/users':
        return add_user(event)
    elif method == 'PUT' and path.startswith('/users/'):
        return update_user(event)
    elif method == 'DELETE' and path.startswith('/users/'):
        return delete_user(event)
    

    elif method == 'GET' and path == '/alarms':
        return get_alarms(event)
    elif method == 'GET' and path.startswith('/alarms/'):
        return get_alarm(event)
    elif method == 'POST' and path == '/alarms':
        return create_alarm(event)
    elif method == 'PUT' and path.startswith('/alarms/'):
        return update_alarm(event)
    elif method == 'DELETE' and path.startswith('/alarms/'):
        return delete_alarm(event)
    
    elif method == 'POST' and path == '/auth':
        return authenticate(event)
    
    return response
