DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/home/production_web/WeekendTrips/mysql_settings.conf',
            "init_command": "SET foreign_key_checks = 0;",
        },
    }
}
