/* */

import api from "./api";
import { showToast } from "../components/ui/Toast";


export async function addDepartmentToCourseApi({course_id, department_id}) {
  try {
    const response = await api.post(
      `/courses/${course_id}/departments/${department_id}`
    );
    return response?.data;
  }
  catch (error) {
    if (error.message) {
      const err_message = "Error adding department to course";
      showToast(error?.response?.data?.error || err_message, "error");
    }
    console.error("Error adding department to course: ", error);
    throw error;
  }
}


export async function addCourseToDepartmentApi({department_id, course_id}) {
  try {
    const response = await api.post(
      `/departments/${department_id}/courses/${course_id}`
    );
    return response?.data;
  }
  catch (error) {
    if (error.message) {
      const err_message = "Error adding course to department";
      showToast(error?.response?.data?.error || err_message, "error");
    }
    console.error("Error adding course to department: ", error);
    throw error;
  }
}


export async function fetchCoursesByDepartmentAndLevelApi({
  department_id, level_id, semester
}) {
  try {
    const response = await api.get(
      `/departments/${department_id}/levels/${level_id}/courses`,
      {params: {semester: semester || null}}
    );
    return response?.data;
  } catch (error) {
      if (error.message) {
        const err_message = "Error fetching department - level courses";
        showToast(error?.response?.data?.error || err_message, "error");
      }
    console.error("Error fetching department - level courses: ", error);
    throw error;
  }
}


export async function deleteDepartmentFromCourseApi({
  course_id, department_id
}) {
  try {
    const response = await api.delete(
      `/courses/${course_id}/departments/${department_id}`
    );
    return response?.data;
  } catch (error) {
    if (error.message){
      const err_message = "Error deleting department from course.";
      showToast(error?.response?.data?.error || err_message, "error");
    }
    console.error("Error deleting department from course: ", error);
    throw error;
  }
}


export async function deleteCourseFromDepartmentApi({course_id, department_id}) {
  try {
    const response = await api.delete(
      `/departments/${department_id}/courses/${course_id}`
    );
    return response?.data;
  } catch (error) {
    if (error.message) {
      const err_message = "Error deleting course from department.";
      showToast(error?.response?.data?.error || err_message, "error");
    }
    console.error("Error deleting course from department: ", error);
    throw error;
  }
}
