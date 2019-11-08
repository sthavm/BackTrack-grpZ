# Generated by Django 2.2.6 on 2019-11-08 18:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_manager', models.BooleanField(default=False, verbose_name='manager status')),
                ('is_prodowner', models.BooleanField(default=False, verbose_name='product owner status')),
                ('is_devteam', models.BooleanField(default=False, verbose_name='development team member status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectID', models.CharField(max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DevTeamMember',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(auto_now_add=True)),
                ('durationInDays', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('endDate', models.DateField()),
                ('totalEffortHours', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=False, verbose_name='active sprint status')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Pbi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(default='NotYetStarted', max_length=20)),
                ('description', models.CharField(max_length=2000)),
                ('priority', models.DecimalField(decimal_places=0, max_digits=4)),
                ('storyPt', models.DecimalField(decimal_places=0, max_digits=2)),
                ('projectID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Project')),
                ('sprints', models.ManyToManyField(to='orders.Sprint')),
            ],
            options={
                'unique_together': {('title', 'projectID')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('title', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=2000)),
                ('status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=15)),
                ('priority', models.DecimalField(decimal_places=0, max_digits=4)),
                ('effortHours', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('pbi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Pbi')),
                ('creator', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.DevTeamMember')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOwner',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('project', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Project')),
            ],
        ),
    ]
