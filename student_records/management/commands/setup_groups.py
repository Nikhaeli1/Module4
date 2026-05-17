from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from student_records.models import StudentRecord

class Command(BaseCommand):
    help = 'Create RBAC groups and demo users for lab testing.'

    def handle(self, *args, **options):
        # Part B: Create the three groups
        for name in ['Admin', 'Faculty', 'Student']:
            group, created = Group.objects.get_or_create(name=name)
            self.stdout.write(f"Group '{name}' - {'created' if created else 'exists'}")

        # Create demo users
        demo_users = [
            ('admin_user',   'Admin@1234',   'Admin',   True),
            ('faculty_user', 'Faculty@1234', 'Faculty', False),
            ('student_user', 'Student@1234', 'Student', False),
        ]
        for username, password, role, is_staff in demo_users:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, password=password, is_staff=is_staff
                )
                user.groups.add(Group.objects.get(name=role))
                self.stdout.write(self.style.SUCCESS(f'Created {username} -> {role}'))