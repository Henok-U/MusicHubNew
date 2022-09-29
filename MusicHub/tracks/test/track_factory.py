import factory

from MusicHub.users.test.user_factory import UserFactory


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tracks.Track"

    id = factory.Faker("uuid4")
    filename = "Track 01 - track"
    created_by = factory.SubFactory(UserFactory) or ""
    track = factory.django.FileField(filename="test.mp3")
    track_length = 145

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = cls.build(*args, **kwargs)
        instance.save()
        return instance
