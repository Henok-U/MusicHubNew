from django.db.models import Manager
from MusicHub.users.models import User


class AggregationManager(Manager):
    def aggregate_number_of_tracks(self, playlist):
        return self.filter(
            created_by=playlist.created_by, track__playlist=playlist.name
        ).count()

    def aggregate_likes(self, **kwargs):
        return User.objects.filter(**kwargs).count()
