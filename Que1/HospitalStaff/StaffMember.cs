namespace HospitalStaff;

public abstract class StaffMember
{
    protected StaffMember(string staffId, string name, string department)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(staffId);
        ArgumentException.ThrowIfNullOrWhiteSpace(name);
        ArgumentException.ThrowIfNullOrWhiteSpace(department);
        StaffId = staffId.Trim();
        Name = name.Trim();
        Department = department.Trim();
    }

    public string StaffId { get; }
    public string Name { get; }
    public string Department { get; }
    public abstract string PerformDuty();

    public virtual string Describe() => $"{StaffId} | {Name} | {Department}";
}

public sealed class Doctor : StaffMember
{
    public Doctor(string staffId, string name, string department, string specialty)
        : base(staffId, name, department)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(specialty);
        Specialty = specialty.Trim();
    }

    public string Specialty { get; }

    public override string Describe() => $"{base.Describe()} | Doctor | Specialty: {Specialty}";

    public override string PerformDuty() => $"Diagnoses and treats patients in {Specialty}.";
}

public sealed class Nurse : StaffMember
{
    public Nurse(string staffId, string name, string department, string ward)
        : base(staffId, name, department)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(ward);
        Ward = ward.Trim();
    }

    public string Ward { get; }

    public override string Describe() => $"{base.Describe()} | Nurse | Ward: {Ward}";

    public override string PerformDuty() => $"Monitors and cares for patients in ward {Ward}.";
}

public sealed class AdministrativeStaff : StaffMember
{
    public AdministrativeStaff(string staffId, string name, string department, string office)
        : base(staffId, name, department)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(office);
        Office = office.Trim();
    }

    public string Office { get; }

    public override string Describe() => $"{base.Describe()} | Administrative staff | Office: {Office}";

    public override string PerformDuty() => $"Manages records and appointments in {Office}.";
}
