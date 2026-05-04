# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Maintenance(models.Model):
    train_id = models.IntegerField(blank=True, null=True)
    last_service = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maintenance'


class Passengers(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passengers'


class RouteStations(models.Model):
    route = models.ForeignKey('Routes', models.DO_NOTHING, blank=True, null=True)
    station = models.ForeignKey('Stations', models.DO_NOTHING, blank=True, null=True)
    station_order = models.IntegerField()
    distance_km = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route_stations'


class Routes(models.Model):
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'routes'


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    train = models.ForeignKey('Trains', models.DO_NOTHING, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule'


class SegmentSchedule(models.Model):
    train = models.ForeignKey('Trains', models.DO_NOTHING, blank=True, null=True)
    from_station = models.ForeignKey('Stations', models.DO_NOTHING, db_column='from_station', blank=True, null=True)
    to_station = models.ForeignKey('Stations', models.DO_NOTHING, db_column='to_station', related_name='segmentschedule_to_station_set', blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'segment_schedule'


class Signals(models.Model):
    segment_id = models.IntegerField(blank=True, null=True)
    signal_status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'signals'


class StationTiming(models.Model):
    train_id = models.IntegerField(blank=True, null=True)
    station_id = models.IntegerField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station_timing'


class Stations(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(unique=True, max_length=50)
    print(station_name)

    class Meta:
        managed = False
        db_table = 'stations'
    def __str__(self):
        
        return self.station_name


class Tickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    passenger_id = models.IntegerField(blank=True, null=True)
    from_station = models.IntegerField(blank=True, null=True)
    to_station = models.IntegerField(blank=True, null=True)
    fare = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class TrackSegments(models.Model):
    segment_id = models.AutoField(primary_key=True)
    from_station = models.IntegerField(blank=True, null=True)
    to_station = models.IntegerField(blank=True, null=True)
    route_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track_segments'


class TrainStatus(models.Model):
    train_id = models.IntegerField(blank=True, null=True)
    current_station = models.IntegerField(blank=True, null=True)
    next_station = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'train_status'


class Trains(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=50, blank=True, null=True)
    route = models.ForeignKey(Routes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trains'
