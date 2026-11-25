namespace StudentRecords;

internal sealed record Student(string Id, string Name, IReadOnlyList<ModuleResult> Results);

internal sealed record ModuleResult(string Module, int? Mark)
{
    // Illustrative boundaries chosen to match the grades shown in the brief.
    public string Grade => Mark switch
    {
        null => "Pending",
        >= 80 => "A",
        >= 70 => "B+",
        >= 60 => "B",
        >= 50 => "C",
        >= 40 => "D",
        _ => "F"
    };
}
