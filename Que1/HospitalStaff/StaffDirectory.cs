using System.Diagnostics.CodeAnalysis;

namespace HospitalStaff;

public sealed class StaffDirectory
{
    private readonly Dictionary<string, StaffMember> staffById = new(StringComparer.OrdinalIgnoreCase);

    public IReadOnlyCollection<StaffMember> AllStaff => staffById.Values;

    public bool TryAdd(StaffMember staff)
    {
        ArgumentNullException.ThrowIfNull(staff);
        return staffById.TryAdd(staff.StaffId, staff);
    }

    public bool SearchStaff(string? staffId, [NotNullWhen(true)] out StaffMember? staff)
    {
        if (string.IsNullOrWhiteSpace(staffId))
        {
            staff = null;
            return false;
        }

        return staffById.TryGetValue(staffId.Trim(), out staff);
    }
}
