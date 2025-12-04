/* */

import api from "./api";
import { showToast } from "../components/ui/Toast";


export async function  addCourseApi({course_data}) {
  try {
    const response = await api.post("/courses", course_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error adding courses.", "error");
    console.error("Error adding courses: ", error);
    throw error;
  }
}


export async function updateCourseApi({course_id, course_data}) {
  try {
    const response = await api.put(`/courses/${course_id}`, course_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error updating courses.", "error");
    console.error("Error updating courses: ", error);
    throw error;
  }
}


export async function fetchAllCoursesApi({
  page_size, page_num, created_at, search_course_code
}) {
  try {
    const response = await api.get(
      "/courses",
      {params:
        {
          page_size: page_size || null,
          page_num: page_num || null,
          date_time: created_at || null,
          search: search_course_code || null,
        },
      }
    );
    return response?.data
  }
  catch (error) {
    if (error.message) {
      const err_message = "Error fetching all courses.";
      showToast(error?.response?.data?.error || err_message, "error");
    }
    console.error("Error fetching all courses: ", error);
    throw error;
  }
}


export async function fetchCourseApi({course_id}) {
  try {
    const response = await api.get(`/courses/${course_id}`);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching course.", "error");
    console.error("Error fetching course: ", error);
    throw error;
  }
}


export async function deleteCourseApi({course_id}) {
  try {
    await api.delete(`/courses/${course_id}`);
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error deleting course.", "error");
    console.error("Error deleting course: ", error);
    throw error;
  }
}
