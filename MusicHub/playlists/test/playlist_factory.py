import factory
from factory import fuzzy

from ...users.test.user_factory import UserFactory


class PlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "playlists.Playlist"

    id = factory.Faker("uuid4")
    name = factory.Faker("text", max_nb_chars=30)
    is_public = factory.Faker("boolean")
    playlist_image = fuzzy.FuzzyChoice(["test.jpg", "test.png", "test.jpeg"])
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date_time")
    likes = factory.Faker("random_int")
