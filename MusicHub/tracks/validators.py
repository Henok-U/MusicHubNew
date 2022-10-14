from rest_framework.serializers import ValidationError


def is_user_owner_of_obj(user, obj):
    if not str(obj.created_by) == str(user):
        raise ValidationError(
            f" {user.email} is not owner of this {obj.__class__.__name__}"
        )
