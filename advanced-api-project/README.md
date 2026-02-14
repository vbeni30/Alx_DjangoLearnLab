\# Advanced API Project – Book Management



\## Overview

This project demonstrates the use of Django REST Framework generic views

to build a clean and secure CRUD API for managing books.



\## API Endpoints



| Method | Endpoint | Description | Auth Required |

|------|--------|------------|---------------|

| GET | /api/books/ | List all books | No |

| GET | /api/books/<id>/ | Retrieve a book | No |

| POST | /api/books/create/ | Create a book | Yes |

| PUT/PATCH | /api/books/<id>/update/ | Update a book | Yes |

| DELETE | /api/books/<id>/delete/ | Delete a book | Yes |



\## Permissions

\- Read-only access is public

\- Create, update, and delete operations require authentication



\## Validation

\- `publication\_year` cannot be in the future

\- Validation handled in `BookSerializer`



