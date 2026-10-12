from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class SurveysPlusAttemptLimitTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='surveyperson',
            email='survey@example.com',
            password='secret123',
        )
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_surveys_plus_allows_two_attempts(self):
        self.profile.system_survey_attempts = 1
        self.profile.save()

        self.client.login(username='surveyperson', password='secret123')
        response = self.client.get(reverse('take_survey', args=['SurveysPlus']))

        self.assertEqual(response.status_code, 200)

    def test_surveys_plus_blocks_more_than_two_attempts(self):
        self.profile.system_survey_attempts = 2
        self.profile.save()

        self.client.login(username='surveyperson', password='secret123')
        response = self.client.get(reverse('take_survey', args=['SurveysPlus']))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('surveys_list'))
