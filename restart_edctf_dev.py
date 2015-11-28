import os


def main():
    dropdb = 'sudo -u postgres psql -c "DROP DATABASE edctf;"'
    rm_migrations = 'rm edctf/api/migrations/0*'
    createdb = 'sudo python generate_secrets.py'
    run_migrations = '''python manage.py makemigrations \\
    && python manage.py migrate \\
    && cat createsuperuser.py | python manage.py shell
    '''

    choice = raw_input('This program will destroy the edctf database and delete migrations, then attempts to recreate the database\n\nARE YOU SURE? (Y/n) >')
    print

    if 'n' in choice.lower():
        exit()

    os.system(rm_migrations)
    os.system(dropdb)
    os.system(createdb)
    os.system(run_migrations)
    print

if __name__ == '__main__':
    main()