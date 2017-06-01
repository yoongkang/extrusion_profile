from unittest import TestCase
from profile import Profile


class TestProfile(TestCase):
    def test_create_from_json(self):
        profile = Profile.create_from_json('fixtures/Rectangle.json')
        self.assertEqual(len(profile.edges), 4)
