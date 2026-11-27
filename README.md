# B9CY108 Advanced Programming Techniques

The CA One project includes two independent .NET 10 console projects and two Python tasks.

| Project | What it does | Verification |
| --- | --- | --- |
| `Que1/HospitalStaff` | Adds doctors, nurses and administrative staff, displays duties and searches by staff ID. | Five MSTest cases plus console checks for all three roles, duplicates, empty records, invalid input and end of input. |
| `Que2/StudentRecords` | Looks up any of 20 records by student ID and displays module marks and grades. | All 20 IDs, the supplied example, a missing ID and invalid input were exercised. |

## Run Part I

From this directory with the .NET 10 SDK installed:

```sh
dotnet run --project Que1/HospitalStaff
dotnet test Que1/HospitalStaff.Tests
dotnet run --project Que2/StudentRecords
```

For the staff app, add one member with each of options 1–3, then use option 4 to display everyone and option 5 to search by ID. IDs ignore case and surrounding whitespace. Staff records are held in memory for the current session.

For the student app, try IDs `20001010` to `20001029`. The project reproduces the example student and first three grades from the brief. The other 19 records are synthetic. Module 4 and 5 serve as placeholders for the unnamed columns. The illustrative grade boundaries are A ≥80, B+ ≥70, B ≥60, C ≥50, D ≥40 and F below 40. The example student's final two results are pending.

The evidence folders contain Windows PowerShell screenshots showing all three staff roles, successful and unsuccessful staff searches, five passing tests, and the example student lookup. `Que1/evidence/q1_all_staff_members.png` displays the three roles and duties; `Que1/evidence/q1_staff_member_checking.png` shows both search outcomes; `Que1/evidence/q1_unit_tests.png` shows the five passing tests.

## Run Part II

From the repository root, use Python 3.10 or newer and a running local PostgreSQL instance. Install the dependencies with:

```powershell
python -m pip install -r Que3/requirements.txt -r Que4/requirements.txt
```

### Que3 - Library registration

Create an empty PostgreSQL database named `library` and use an account with permission to create tables in it. In the server PowerShell window, set the connection parameters:

```powershell
$env:PGHOST = '127.0.0.1'
$env:PGPORT = '5432'
$env:PGDATABASE = 'library'
$env:PGUSER = 'postgres' # Replace with your PostgreSQL account
python Que3/Que3_server.py
```

Use your private PostgreSQL password file or local environment for authentication. The server also accepts a connection string supplied as `LIBRARY_DATABASE_URL`. It creates the table on startup and listens locally on TCP port 5050.

In a separate terminal, run `python Que3/Que3_client.py` and enter synthetic details. Select a 6- or 12-month membership. The client prints the assigned registration number after PostgreSQL saves the record. To use a different TCP port, pass the same `--port` value to both programs.

Query `library_members` to inspect the saved rows. `Que3/evidence` contains Windows PowerShell client and server captures of two synthetic registrations (6 and 12 months) and a pgAdmin query showing the matching PostgreSQL 19 rows. The second client run also shows an invalid duration being rejected before accepting `12`.

### Que4 - Dublin postal districts

Run `python Que4/Que4.py` with internet access. The script writes `dublin_postal_districts.json` and `dublin_postal_districts.csv` in `Que4`, then prints all CSV rows. Use `--output-dir` to choose a different directory. The checked-in run produced 178 area rows across 22 numbered Dublin districts, including D6W. `Que4/evidence` contains Windows PowerShell captures of the first CSV rows and the final count and saved-file message.

## Sources

- Dublin Business School, B9CY108 CA One assignment brief, Tasks 1–2. Source for the requirements, menu and example student record.
- [Microsoft Learn, Get started with C# and MSTest](https://learn.microsoft.com/dotnet/core/testing/unit-testing-with-mstest). Reference for the test-project setup and assertions.
- [Microsoft Learn, Install .NET on Linux](https://learn.microsoft.com/en-us/dotnet/core/install/linux). Reference for the SDK used to build and run the projects.
- [Python socketserver documentation](https://docs.python.org/3/library/socketserver.html). TCP request handling.
- [Psycopg query parameters](https://www.psycopg.org/psycopg3/docs/basic/params.html) and [PostgreSQL identity columns](https://www.postgresql.org/docs/17/ddl-identity-columns.html). Database writes and registration identifiers.
- [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). HTML parsing.
- [Wikipedia contributors, List of Dublin postal districts](https://en.wikipedia.org/wiki/List_of_Dublin_postal_districts), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The JSON and CSV extract and normalize area names from the district lists.
