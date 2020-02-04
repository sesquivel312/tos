class config(object):
    secret_key = os.environ.get(CRUD_SECRET_KEY) or 'supersecretpassword'