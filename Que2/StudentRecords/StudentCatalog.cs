namespace StudentRecords;

internal static class StudentCatalog
{
    public static Dictionary<string, Student> Load()
    {
        Student[] records =
        [
            Create("20001010", "Charles Severance", 70, 65, 55, null, null),
            Create("20001011", "Avery Parker", 78, 81, 72, 68, 75),
            Create("20001012", "Jordan Hayes", 62, 71, 69, 74, 66),
            Create("20001013", "Morgan Blake", 91, 87, 89, 84, 88),
            Create("20001014", "Casey Walsh", 57, 63, 60, 54, 61),
            Create("20001015", "Taylor Reed", 74, 76, 82, 79, 73),
            Create("20001016", "Cameron Quinn", 49, 58, 64, 52, 56),
            Create("20001017", "Riley Burke", 83, 77, 86, 81, 79),
            Create("20001018", "Harper Kelly", 68, 72, 75, 70, 67),
            Create("20001019", "Drew Nolan", 56, 55, 63, 59, 58),
            Create("20001020", "Peyton Doyle", 88, 90, 85, 87, 92),
            Create("20001021", "Robin Hughes", 65, 69, 70, 62, 71),
            Create("20001022", "Emery Clarke", 73, 80, 77, 76, 82),
            Create("20001023", "Sage Byrne", 45, 52, 48, 57, 53),
            Create("20001024", "Rowan Bennett", 81, 84, 78, 85, 80),
            Create("20001025", "Devon Flynn", 67, 64, 72, 65, 69),
            Create("20001026", "Ellis Murray", 76, 73, 81, 78, 74),
            Create("20001027", "Sydney Lane", 59, 61, 56, 63, 60),
            Create("20001028", "Blair Adams", 93, 92, 88, 90, 86),
            Create("20001029", "Jamie Scott", 71, 76, 73, 70, 77)
        ];

        return records.ToDictionary(student => student.Id, StringComparer.Ordinal);
    }

    private static Student Create(string id, string name, int programming, int databases,
        int networking, int? module4, int? module5) =>
        new(id, name,
        [
            new("Advanced Programming", programming),
            new("Advanced Databases", databases),
            new("Networking & Security", networking),
            new("Module 4", module4),
            new("Module 5", module5)
        ]);
}
