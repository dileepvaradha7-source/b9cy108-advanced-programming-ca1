using Microsoft.VisualStudio.TestTools.UnitTesting;
[assembly: Parallelize(Scope = ExecutionScope.MethodLevel)]

namespace HospitalStaff.Tests;

[TestClass]
public sealed class StaffDirectoryTests
{
    [TestMethod]
    public void SearchStaffReturnsTrueAndTheMatchingStaffMember()
    {
        var directory = new StaffDirectory();
        var doctor = new Doctor("D001", "Alex Morgan", "Cardiology", "Cardiology");
        Assert.IsTrue(directory.TryAdd(doctor));

        bool found = directory.SearchStaff(" d001 ", out StaffMember? result);

        Assert.IsTrue(found);
        Assert.AreSame(doctor, result);
    }

    [TestMethod]
    [DataRow("missing")]
    [DataRow("")]
    [DataRow("   ")]
    public void SearchStaffReturnsFalseAndNullForUnmatchedIds(string id)
    {
        var directory = new StaffDirectory();
        directory.TryAdd(new Nurse("N001", "Jamie Lee", "Surgery", "A2"));

        bool found = directory.SearchStaff(id, out StaffMember? result);

        Assert.IsFalse(found);
        Assert.IsNull(result);
    }

    [TestMethod]
    public void DuplicateIdKeepsTheOriginalStaffMember()
    {
        var directory = new StaffDirectory();
        var doctor = new Doctor("D001", "Alex Morgan", "Cardiology", "Cardiology");
        Assert.IsTrue(directory.TryAdd(doctor));

        bool added = directory.TryAdd(new Nurse("d001", "Jamie Lee", "Surgery", "A2"));

        Assert.IsFalse(added);
        Assert.IsTrue(directory.SearchStaff("D001", out StaffMember? result));
        Assert.AreSame(doctor, result);
    }
}
