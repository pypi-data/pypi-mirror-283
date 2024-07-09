# django-migrations-auto

A Django app to store migrations in the database and apply them automatically.

## Installation

```bash
pip install django-migrations-auto
```


## Usage

### 1. Add to Installed Apps

Add `'django_migrations_auto.migrations_log'` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_migrations_auto.migrations_log',
]
```

### 2. Run Migrations
```bash 
python manage.py migrate migrations_log
```
### 3. Custom Management Commands

#### `makemigrations`

This command generates new migrations based on the changes detected to your models.

Usage:

```bash
python manage.py makemigrations [app_label]
```
#### auto_migrate
This command runs makemigrations and migrate automatically, storing migration files in the database.
```bash 
python manage.py auto_migrate [app_label]
```

## Running Tests

To run the tests, first set up the test environment:

1. Ensure your `DATABASES` setting in `settings_test.py` points to a test database.

2. Run the tests using the following command:

```bash
DJANGO_SETTINGS_MODULE=django_migrations_auto.settings_test python manage.py test
```

## Compatibility

This package is compatible with Django versions 3.2 to 5.0 and requires Python 3.7 to 3.12.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

### Steps to Contribute

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the maintainer at lmccc.dev@gmail.com.



