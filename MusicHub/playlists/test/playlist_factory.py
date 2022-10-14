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

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        """Populate many to many field 'likes' with dummy data given in constructor"""
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for like in extracted:
                self.likes.add(like)
