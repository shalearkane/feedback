from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets


class Poll(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.BooleanField(editable=True, null=True)

    def __str__(self):
        return f"{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}"
