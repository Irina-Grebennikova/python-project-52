### Hexlet tests and linter status:

[![Actions Status](https://github.com/Irina-Grebennikova/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Irina-Grebennikova/python-project-52/actions)

<hr>

[![Task Manager CI](https://github.com/Irina-Grebennikova/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/Irina-Grebennikova/python-project-52/actions/workflows/ci.yml)
[![Quality gate status](https://sonarcloud.io/api/project_badges/measure?project=Irina-Grebennikova_python-project-52&metric=alert_status&token=e29fe314b416b2cf5c6080bb977045b9f8ed979b)](https://sonarcloud.io/summary/new_code?id=Irina-Grebennikova_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Irina-Grebennikova_python-project-52&metric=coverage&token=e29fe314b416b2cf5c6080bb977045b9f8ed979b)](https://sonarcloud.io/summary/new_code?id=Irina-Grebennikova_python-project-52)

### About

**Task Manager** is a Django-based educational project that implements a task management system. It demonstrates CRUD operations, user authentication, relational database management with the Django ORM, class-based views, and automated testing. The application allows users to manage tasks, statuses, labels, and user accounts through a simple web interface.

### Links

**App link**: https://task-manager-i0du.onrender.com

#### Tooling

| Tool                                 | Description                                                           |
| ------------------------------------ | --------------------------------------------------------------------- |
| [uv](https://docs.astral.sh/uv/)     | An extremely fast Python package and project manager, written in Rust |
| [ruff](https://docs.astral.sh/ruff/) | An extremely fast Python linter and code formatter, written in Rust   |

#### Runtime

| Tool                                      | Description                     |
| ----------------------------------------- | ------------------------------- |
| [Django](https://www.djangoproject.com/)  | High-level Python web framework |
| [Gunicorn](https://gunicorn.org/)         | Python WSGI HTTP server         |
| [PostgreSQL](https://www.postgresql.org/) | Relational database             |

---

## Requirements

- Python 3.11+
- uv
- PostgreSQL

### Installation

```bash
git clone <repository-url>
cd <repository-name>
make install
```

Create a .env file and configure the required environment variables.

Apply database migrations:

```bash
make migrate
```

### Run

Start the development server:

```bash
make run
```

Run tests:

```bash
make test
```
