import { useState } from "react";

import {
  assignCoursesToDepartmentAPI,
  removeCoursesFromDepartmentAPI
} from "../pages/api/courses";
import { showToast } from "../pages/utils/toast";



export default function AssignCoursesForm({
  onClose,
  onSaved,
  departments,
  courses,
}) {
  console.log("Inside AssignCourse", courses)
  const [departmentId, setDepartmentId] = useState("");
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [mode, setMode] = useState("assign"); // assign or remove
  const [saving, setSaving] = useState(false);

  const toggleCourse = (id) => {
    setSelectedCourses((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!departmentId) {
      showToast("Please select a department", "error");
      return;
    }
    if (selectedCourses.length === 0) {
      showToast("Please select at least one course", "error");
      return;
    }

    try {
      setSaving(true);

      // Loop over each selected course and call API sequentially
      for (const courseId of selectedCourses) {
        if (mode === "assign") {
          await assignCoursesToDepartmentAPI(departmentId, courseId);
        } else {
          await removeCoursesFromDepartmentAPI(departmentId, courseId);
        }
      }

      showToast(
        mode === "assign"
          ? "Courses assigned successfully"
          : "Courses removed successfully",
        "success"
      );

      onSaved();
      onClose();
    } catch (err) {
      console.log(err)
    } finally {
      setSaving(false);
    }
  };


  return (
    <div>
      <div>
        <h2>
          {mode === "assign" ? "Assign Courses" : "Remove Courses"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div>
            <select
              value={departmentId}
              onChange={(e) => setDepartmentId(e.target.value)}
            >
              <option value="">Select Department</option>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.dept_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            {courses.map((c) => (
              <label
                key={c.id}
              >
                <div>
                <input
                  type="checkbox"
                  checked={selectedCourses.includes(c.id)}
                  onChange={() => toggleCourse(c.id)}
                />
                  {c.course_code}
                </div>
              </label>
            ))}
          </div>

          <div>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
            >
              <option value="assign">Assign</option>
              <option value="remove">Remove</option>
            </select>

            <div>
              <button
                type="button"
                onClick={onClose}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saving}
              >
                {saving ? "Saving..." : "Save"}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
