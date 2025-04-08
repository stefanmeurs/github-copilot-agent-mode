import json
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        with open('/workspaces/github-copilot-agent-mode/octofit-tracker/backend/octofit_tracker/test_data.json', 'r') as file:
            data = json.load(file)

        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Populate users
        users = {}
        for user_data in data['users']:
            user = User.objects.create(**user_data)
            users[user_data['username']] = user
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))

        # Populate teams
        for team_data in data['teams']:
            members = [users[username] for username in team_data.pop('members')]
            try:
                team = Team.objects.create(**team_data)
                team.members.set(members)
                self.stdout.write(self.style.SUCCESS(f"Created team: {team.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating team: {team_data}, Error: {e}"))

        # Populate activities
        for activity_data in data['activities']:
            activity_data['user'] = users[activity_data['user']]
            activity = Activity.objects.create(**activity_data)
            self.stdout.write(self.style.SUCCESS(f"Created activity: {activity.activity_type} for user {activity.user.username}"))

        # Populate workouts
        for workout_data in data['workouts']:
            workout = Workout.objects.create(**workout_data)
            self.stdout.write(self.style.SUCCESS(f"Created workout: {workout.name}"))

        # Populate leaderboard
        for leaderboard_data in data['leaderboard']:
            leaderboard_data['user'] = users[leaderboard_data['user']]
            leaderboard = Leaderboard.objects.create(**leaderboard_data)
            self.stdout.write(self.style.SUCCESS(f"Created leaderboard entry for user: {leaderboard.user.username} with points: {leaderboard.points}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
