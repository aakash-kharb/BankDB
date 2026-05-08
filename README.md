# BankDB : Django Bank Database Management

A lightweight, production-informed web application for managing customer banking records and passbooks. Built with **Django 5.x**, **Bootstrap 5**, and **Google Material Symbols**.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Run](#run)
- [Database Modes](#database-modes)
- [URL Routes](#url-routes)
- [Model Schema](#model-schema)
- [Design System](#design-system)
- [Author](#author)
- [License](#license)

---

## Features

- **CRUD Operations** — Create, read, update, and delete customer records with server-side validation
- **Passbook Views** — View all customers, filter by branch, or look up individual applicants
- **Search & Pagination** — Full-text search across name, IFSC, city, applicant number, and branch
- **SQL Reference** — Browse the parameterized SQL queries used by the application
- **Source Code Viewer** — In-app view of key source files (models, forms, views, settings, URLs)
- **Health Check** — Real-time database connectivity status, record count, and response time
- **Dark Mode** — Toggle between light and dark themes with persistent localStorage preference
- **Responsive Design** — Mobile-friendly layout with collapsible navigation

## Tech Stack

<div align="center">

| Layer      | Technology                           |
|:----------:|:------------------------------------:|
| Backend    | Django 5.x (Python)                  |
| Database   | SQLite (local) / MySQL (Railway)     |
| Frontend   | Bootstrap 5, Google Material Symbols |
| Typography | Inter (Google Fonts)                 |
| Config     | python-dotenv                        |

</div>

## Project Structure

```
bankdb_django_ui/
├── bankdb/                  <- Django project configuration
│   ├── settings.py          <- Settings with DUMMY_DATABASE toggle
│   ├── urls.py              <- Root URL configuration
│   ├── wsgi.py              <- WSGI entry point
│   └── asgi.py              <- ASGI entry point
├── core/                    <- Main application
│   ├── models.py            <- CustomerRecord model
│   ├── views.py             <- All view functions (CRUD, passbook, health)
│   ├── forms.py             <- CustomerForm, CustomerUpdateForm (IFSC validation)
│   ├── urls.py              <- App URL patterns
│   ├── admin.py             <- Django admin registration
│   └── migrations/          <- Database migration files
├── templates/
│   ├── base.html            <- Base template (navbar, footer, Material Symbols)
│   └── core/                <- Page templates
│       ├── home.html         <- Landing page with hero and feature cards
│       ├── records_list.html <- Searchable, paginated records table
│       ├── add_record.html   <- Add new customer record form
│       ├── edit_record.html  <- Edit existing record form
│       ├── delete_record.html<- Delete confirmation
│       ├── passbook_all.html <- Full passbook with totals
│       ├── passbook_branch.html  <- Branch-filtered passbook
│       ├── passbook_applicant.html <- Single applicant lookup
│       ├── sql_queries.html  <- SQL reference cards
│       ├── source_code.html  <- Source code snippets
│       └── health.html       <- Health check dashboard
├── static/
│   ├── css/theme.css         <- Custom design system (light/dark mode)
│   ├── js/ui.js              <- Theme toggle, toasts, active nav
│   └── img/                  <- Favicon and logo assets
├── .env                      <- Environment variables (not committed)
├── .gitignore                <- Git ignore rules
├── manage.py                 <- Django management script
├── requirements.txt          <- Python dependencies
└── LOGO.png                  <- Original logo (1024x1024)
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/aakash-kharb/BankDB/
cd BankDB

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy or edit the `.env` file in the project root:

```env
DUMMY_DATABASE=true          # true = local SQLite, false = MySQL

# MySQL credentials (used when DUMMY_DATABASE=false)
# DB_NAME=bank_db
# DB_USER=root
# DB_PASSWORD=your_password
# DB_HOST=your_host
# DB_PORT=3306
# DB_SSL=true

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=*
```

### Run

```bash
# Apply migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Start the development server
python3 manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

## Database Modes

<div align="center">

| Mode       | `DUMMY_DATABASE` | Engine | Notes                                      |
|:----------:|:----------------:|:------:|:------------------------------------------:|
| Local      | `true`           | SQLite | No external dependency, file-based         |
| Production | `false`          | MySQL  | Requires `DB_*` environment variables      |

</div>

## URL Routes

<div align="center">

| Path                      | View                 | Description                          |
|:-------------------------:|:--------------------:|:------------------------------------:|
| `/`                       | `home`               | Landing page                         |
| `/records/`               | `records_list`       | Paginated record table with search   |
| `/records/add/`           | `add_record`         | Add new customer record              |
| `/records/<pk>/edit/`     | `edit_record`        | Edit existing record                 |
| `/records/<pk>/delete/`   | `delete_record`      | Delete confirmation                  |
| `/passbook/all/`          | `passbook_all`       | Full passbook with totals            |
| `/passbook/branch/`       | `passbook_branch`    | Filter by branch code                |
| `/passbook/applicant/`    | `passbook_applicant` | Look up single applicant             |
| `/sql/`                   | `sql_queries`        | SQL reference page                   |
| `/source/`                | `source_code`        | Source code viewer                   |
| `/health/`                | `healthcheck`        | Database health check                |
| `/admin/`                 | Django Admin         | Admin interface                      |

</div>

## Model Schema

```python
class CustomerRecord(models.Model):
    applicant_no = models.IntegerField(primary_key=True)
    name         = models.CharField(max_length=50)
    ifsc         = models.CharField(max_length=11, db_index=True)
    credit       = models.FloatField(default=0.0)
    debit        = models.FloatField(default=0.0)
    balance      = models.FloatField(default=0.0)
    city         = models.CharField(max_length=50)
    branch       = models.IntegerField()

    class Meta:
        db_table = "customer_records"
        ordering = ["applicant_no"]
```

## Design System

- **CSS Custom Properties** for colors, shadows, radii, and transitions
- **Dark mode** via `[data-bs-theme="dark"]` with persistent preference
- **Google Material Symbols** for all icons (no emojis)
- **Inter** font family throughout
- **Component library**: stat-cards, feature-cards, info-cards, sql-cards, quick-action cards

## Author

**Aakash Kharb**

## License

This project is for educational purposes.
