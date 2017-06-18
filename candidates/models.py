from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import random


class GroupCandidates(models.Model):
    """
    Model to represent group of candiates
    """
    when_created = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return '%d - %s' % (self.id, self.when_created)

    def get_winners(self):
        """
        method to get winners of group
        :return: QuerySet
        """
        winners = self.candidates.filter(is_winner=True)

        if winners:
            return winners

        return self._generate_winners()

    def refresh_winners(self):
        """
        method to refresh winners
        :return: QuerySet
        """
        self.clear_winners()
        return self._generate_winners()

    def clear_winners(self):
        """
        method to remove all winners from group
        :return: None
        """
        self.candidates.filter(is_winner=True).update(is_winner=False)

    def _generate_winners(self, count=settings.COUNT_OF_WINNERS):
        """
        method to generate winners
        :param count: int
        :return: QuerySet
        """
        not_winners = self.candidates.filter(is_winner=False)

        if not_winners.count() < count:
            raise ValueError('Count of candidates must be equal or higher then count of candidates')

        while count:
            winner = random.choice(not_winners)
            if winner.is_winner:
                continue
            winner.is_winner=True
            winner.save()
            count -= 1

        return self.candidates.filter(is_winner=True)


class Candidate(models.Model):
    """
    Model to represent candidate
    """
    name = models.CharField(_('Имя'), max_length=50)
    group = models.ForeignKey(
        GroupCandidates,
        verbose_name=_('Група'),
        related_name='candidates'
    )

    is_winner = models.BooleanField(default=False, verbose_name=_('Победитель?'))

    when_created = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        ordering = ('-is_winner', )
        unique_together = ('name', 'group')

    def __str__(self):
        return self.name