from rest_framework.serializers import ValidationError


def is_user_owner_of_obj(user, obj):
    if not obj.created_by == user:
        raise ValidationError(
            f" {user.email} is not owner of this {obj.__class__.__name__}"
        )
