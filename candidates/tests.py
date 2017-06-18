from django.test import TestCase
from django.db import IntegrityError

from .models import GroupCandidates


# Create your tests here.


class RandomGenerateTestCase(TestCase):
    def setUp(self):
        self.group = GroupCandidates.objects.create()

        self.group.candidates.create(name='Владимир')
        self.group.candidates.create(name='Сергей')

        self.group.candidates.create(name='Пётр')
        self.group.candidates.create(name='Вячеслав')
        self.group.candidates.create(name='Игорь')
        self.group.candidates.create(name='Владислав')

    def test_generate_random_winners(self):
        self.assertEqual(self.group.get_winners().count(), 3)

    def test_refresh_random(self):
        old_winners = self.group.get_winners()
        new_winners = self.group.refresh_winners()

        self.assertNotEqual(old_winners, new_winners)

    def test_add_same_candidate_to_group(self):
        with self.assertRaises(IntegrityError):
            self.group.candidates.create(name='Сергей')

    def test_generate_random_winners_less_than_3_candidates(self):
        self.group.candidates.filter(pk__gt=2).delete()

        with self.assertRaises(ValueError):
            self.group.get_winners()