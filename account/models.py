from django.contrib.auth.models import Group

class UserMixIn(object):
    """ user method """

    @staticmethod
    def is_user_store_manager(user):
        name = "Store manager"
        group, created = Group.objects.get_or_create(name=name)
        if group in user.groups.all():
            return True

    @staticmethod
    def is_user_department_manager(user):
        name = "Department manager"
        group, created = Group.objects.get_or_create(name=name)
        if group in user.groups.all():
            return True
