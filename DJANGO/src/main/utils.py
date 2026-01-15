

def user_list_path(instance,filename):
    return f'user_{0}/list/{1}'.format(instance.seller.user.id,filename)