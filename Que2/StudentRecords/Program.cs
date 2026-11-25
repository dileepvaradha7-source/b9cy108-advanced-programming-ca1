using StudentRecords;

Dictionary<string, Student> students = StudentCatalog.Load();

Console.WriteLine("STUDENT RECORD LOOKUP");
Console.WriteLine($"Loaded {students.Count} student records.");

while (true)
{
    Console.Write("\nStudent ID (0 to exit): ");
    string? id = Console.ReadLine()?.Trim();

    if (id is null or "0")
        return;

    if (id.Length != 8 || !id.All(char.IsAsciiDigit))
    {
        Console.WriteLine("Enter an 8-digit student ID.");
        continue;
    }

    if (!students.TryGetValue(id, out Student? student))
    {
        Console.WriteLine("No student found with that ID.");
        continue;
    }

    Console.WriteLine($"Student ID: {student.Id}");
    Console.WriteLine($"Student name: {student.Name}");
    Console.WriteLine($"{"Module",-27} {"Mark",5}  Grade");
    Console.WriteLine(new string('-', 42));

    foreach (ModuleResult result in student.Results)
    {
        string mark = result.Mark?.ToString() ?? "-";
        Console.WriteLine($"{result.Module,-27} {mark,5}  {result.Grade}");
    }
}
