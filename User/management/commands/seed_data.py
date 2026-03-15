from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial test data including users, projects, bids, contracts and reviews'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('🌱 Seeding test data...'))
        self.create_superuser()
        clients = self.create_clients()
        freelancers = self.create_freelancers()
        self.stdout.write(self.style.SUCCESS('✅ Test data seeded successfully!\n'))
        self.stdout.write(self.style.WARNING('Test credentials:'))
        self.stdout.write('  Client     → username: client1     | password: client123')
        self.stdout.write('  Freelancer → username: freelancer1 | password: freelancer123')
        self.stdout.write('  Admin      → username: admin       | password: admin123')

    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@freelancemarketplace.com',
                password='admin123',
                role='client'
            )
            self.stdout.write('  ✓ Superuser created: admin / admin123')
        else:
            self.stdout.write('  - Superuser already exists, skipping.')

    def create_clients(self):
        clients_data = [
            {
                'username': 'client1',
                'email': 'client1@example.com',
                'password': 'client123',
                'bio': 'Experienced product manager looking for talented developers.',
            },
            {
                'username': 'client2',
                'email': 'client2@example.com',
                'password': 'client123',
                'bio': 'Startup founder building the next big thing.',
            },
        ]
        clients = []
        for data in clients_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    role='client',
                    bio=data['bio']
                )
                clients.append(user)
                self.stdout.write(f"  ✓ Client created: {data['username']} / {data['password']}")
            else:
                clients.append(User.objects.get(username=data['username']))
                self.stdout.write(f"  - Client already exists: {data['username']}, skipping.")
        return clients

    def create_freelancers(self):
        freelancers_data = [
            {
                'username': 'freelancer1',
                'email': 'freelancer1@example.com',
                'password': 'freelancer123',
                'bio': 'Full-stack developer with 5 years of experience in Django and React.',
            },
            {
                'username': 'freelancer2',
                'email': 'freelancer2@example.com',
                'password': 'freelancer123',
                'bio': 'Mobile app developer specializing in Flutter and React Native.',
            },
            {
                'username': 'freelancer3',
                'email': 'freelancer3@example.com',
                'password': 'freelancer123',
                'bio': 'UI/UX designer with a passion for clean, user-friendly interfaces.',
            },
        ]
        freelancers = []
        for data in freelancers_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    role='freelancer',
                    bio=data['bio']
                )
                freelancers.append(user)
                self.stdout.write(f"  ✓ Freelancer created: {data['username']} / {data['password']}")
            else:
                freelancers.append(User.objects.get(username=data['username']))
                self.stdout.write(f"  - Freelancer already exists: {data['username']}, skipping.")
        return freelancers
