import factory

from MusicHub.users.test.user_factory import UserFactory


class PlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "playlists.Playlist"

    id = factory.Faker("uuid4")
    name = factory.Faker("text", max_nb_chars=20)
    is_public = factory.Faker("boolean")
    playlist_image = factory.Faker("file_name", category="image")
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date_time")
    likes = factory.Faker("random_int")
