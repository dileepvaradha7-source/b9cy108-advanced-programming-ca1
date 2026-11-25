using HospitalStaff;

var directory = new StaffDirectory();

while (true)
{
    Console.WriteLine("""

        STAFF MANAGEMENT
        1. Add Doctor
        2. Add Nurse
        3. Add Administrative Staff
        4. Display All Staff
        5. Search Staff
        0. Exit
        """);
    Console.Write("Choice: ");

    switch (Console.ReadLine()?.Trim())
    {
        case "1":
            if (!AddStaff("Specialty", (id, name, department, specialty) =>
                new Doctor(id, name, department, specialty)))
                return;
            break;
        case "2":
            if (!AddStaff("Ward", (id, name, department, ward) =>
                new Nurse(id, name, department, ward)))
                return;
            break;
        case "3":
            if (!AddStaff("Office", (id, name, department, office) =>
                new AdministrativeStaff(id, name, department, office)))
                return;
            break;
        case "4":
            if (directory.AllStaff.Count == 0)
                Console.WriteLine("No staff records have been added.");

            foreach (StaffMember staff in directory.AllStaff)
                DisplayStaff(staff);
            break;
        case "5":
            string? staffId = ReadRequired("Staff ID");
            if (staffId is null)
                return;

            if (directory.SearchStaff(staffId, out StaffMember? found))
            {
                Console.WriteLine("Staff member found.");
                DisplayStaff(found);
            }
            else
            {
                Console.WriteLine("No staff member found with that ID.");
            }
            break;
        case "0":
        case null:
            return;
        default:
            Console.WriteLine("Enter a menu option from 0 to 5.");
            break;
    }
}

bool AddStaff(string detailLabel, Func<string, string, string, string, StaffMember> createStaff)
{
    if (ReadRequired("Staff ID") is not string id ||
        ReadRequired("Name") is not string name ||
        ReadRequired("Department") is not string department ||
        ReadRequired(detailLabel) is not string detail)
    {
        return false;
    }

    StaffMember staff = createStaff(id, name, department, detail);
    Console.WriteLine(directory.TryAdd(staff)
        ? "Staff member added."
        : "A staff member with that ID already exists.");
    return true;
}

static string? ReadRequired(string label)
{
    while (true)
    {
        Console.Write($"{label}: ");
        string? value = Console.ReadLine();
        if (value is null)
            return null;
        if (!string.IsNullOrWhiteSpace(value))
            return value.Trim();

        Console.WriteLine("This field is required.");
    }
}

static void DisplayStaff(StaffMember staff)
{
    Console.WriteLine(staff.Describe());
    Console.WriteLine($"  Duty: {staff.PerformDuty()}");
}
