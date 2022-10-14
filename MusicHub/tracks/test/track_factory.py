import factory

from MusicHub.users.test.user_factory import UserFactory


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tracks.Track"

    id = factory.Faker("uuid4")
    filename = factory.Faker("text", max_nb_chars=20)
    created_by = factory.SubFactory(UserFactory)
    is_public = factory.Faker("boolean")
    created_at = factory.Faker("date_time")
    file = factory.django.FileField(filename="test.mp3")
    track_length = factory.Faker("random_int")

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for like in extracted:
                self.likes.add(like)
