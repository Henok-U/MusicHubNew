import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    id = factory.Faker("uuid4")
    password = "abcABC123*"
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_verified = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.set_password(kwargs["password"])
        obj.save()
        return obj
