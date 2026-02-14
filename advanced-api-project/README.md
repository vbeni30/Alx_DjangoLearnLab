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



\## Filtering, Searching, and Ordering



\### Book List Endpoint

`GET /api/books/`



Supports:



\- Filtering:

&nbsp;   - `?title=<title>`

&nbsp;   - `?author\_\_name=<author\_name>`

&nbsp;   - `?publication\_year=<year>`

\- Searching:

&nbsp;   - `?search=<text>` (search in title and author)

\- Ordering:

&nbsp;   - `?ordering=title`

&nbsp;   - `?ordering=-publication\_year` (descending)



\### Examples



1\. Filter books published in 2008:

GET /api/books/?publication\_year=2008





2\. Search books by author or title:

GET /api/books/?search=Clean





3\. Order books by title ascending:

GET /api/books/?ordering=title





4\. Order books by publication year descending:

GET /api/books/?ordering=-publication\_year

