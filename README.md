# B9CY108 Advanced Programming Techniques

Part I checkpoint for CA One, 25 November 2026. The two .NET 10 console projects run independently.

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

The evidence folders contain images rendered from genuine terminal sessions. The project can be rerun to capture native terminal screenshots for the report.

## Part II on 26 November 2026

1. Implement `Que3_server.py` and `Que3_client.py` for library sign-up over TCP. Use PostgreSQL and confirm the returned registration number matches the stored record. Capture client, server and database evidence with synthetic details.
2. Implement `Que4.py` to extract Dublin district codes and names from the assigned Wikipedia page, write JSON, read it back to create CSV, and print the CSV rows. Save both output files and capture the console result.
3. Record separate GitHub updates as work is completed. Add the repository link and evidence to the report, keep its body within 700 words, and add the official Electronic Assignment Cover Sheet. Package all four folders and the report under the actual student ID. The brief lists 27 November 2026 as the due date and Moodle as the submission route.

## Sources and assistance

- Dublin Business School, B9CY108 CA One assignment brief, Tasks 1–2. Source for the requirements, menu and example student record.
- [Microsoft Learn, Get started with C# and MSTest](https://learn.microsoft.com/dotnet/core/testing/unit-testing-with-mstest). Reference for the test-project setup and assertions.
- [Microsoft Learn, Install .NET on Linux](https://learn.microsoft.com/en-us/dotnet/core/install/linux). Reference for the SDK used to build and run the projects.
- OpenAI ChatGPT, 25 November 2026. Assisted with interpreting the brief, drafting the C# code and MSTest cases, running and checking the applications, capturing terminal output and preparing this checkpoint. Record any subsequent assistance and changes in the report.
