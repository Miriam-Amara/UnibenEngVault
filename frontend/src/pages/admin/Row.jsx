import { assignCourseToDepartmentAPI, removeCourseFromDepartmentAPI } from "../api/courses";
import { showToast } from "../utils/toast";

export default function CourseRow({ course, departmentId, onEdit, onRemove }) {
  const handleRemove = async () => {
    if (!window.confirm(`Remove ${course.course_code} from this department?`)) return;
    try {
      await removeCourseFromDepartmentAPI(course.id, departmentId);
      showToast("Course removed from department", "success");
      if (onRemove) onRemove();
    } catch (err) {
      console.error(err);
      showToast("Failed to remove course", "error");
    }
  };

  return (
    <tr>
      <td>{course.course_code}</td>
      <td>{course.semester}</td>
      <td>{course.credit_load}</td>
      <td>{course.title}</td>
      <td>{course.level_name}</td>
      <td>{course.is_active ? "Yes" : "No"}</td>
      <td>
        <button onClick={() => onEdit(course)}>Edit</button>
        <button onClick={handleRemove}>Remove</button>
      </td>
    </tr>
  );
}
