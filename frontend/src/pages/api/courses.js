import axios from "axios";
import { showToast } from "../utils/toast";

// Helper for error handling
const handleApiError = (error, action = "operation") => {
  if (error.response) {
    const { status, data } = error.response;
    switch (status) {
      case 400:
        showToast(data?.error || "Bad request", "error");
        break;
      case 401:
        showToast("Unauthorized: Please log in again.", "error");
        break;
      case 403:
        showToast("Forbidden: You're not supposed to be here", "error");
        break;
      case 404:
        showToast("Not found: The requested resource could not be found.", "error");
        break;
      case 409:
        showToast(data?.error || "Conflict: Duplicate or invalid data.", "error");
        break;
      case 500:
        showToast("Server error: Please try again later.", "error");
        break;
      default:
        showToast(data?.error || `An error occurred during ${action}.`, "error");
    }
  } else {
    showToast("Network error: Unable to reach the server.", "error");
  }
  throw error; // rethrow so the caller can handle if needed
};

// Add new course
export const addCourseAPI = async (data) => {
  try {
    const res = await axios.post("/api/v1/courses", data, { withCredentials: true });
    showToast("Course added successfully!", "success");
    return res.data;
  } catch (error) {
    handleApiError(error, "adding course");
  }
};

// Update existing course
export const updateCourseAPI = async (id, data) => {
  try {
    const res = await axios.put(`/api/v1/courses/${id}`, data, { withCredentials: true });
    showToast("Course updated successfully!", "success");
    return res.data;
  } catch (error) {
    handleApiError(error, "updating course");
  }
};

// Delete a course
export const deleteCourseAPI = async (id) => {
  try {
    const res = await axios.delete(`/api/v1/courses/${id}`, { withCredentials: true });
    showToast("Course deleted successfully!", "success");
    return res.data;
  } catch (error) {
    handleApiError(error, "deleting course");
  }
};

// Fetch all or filtered courses
export const fetchCoursesAPI = async ({
  pageSize = 10,
  pageNum = 1,
  departmentId = "",
  levelId = "",
}) => {
  try {
    let res;
    if (departmentId && levelId) {
      res = await axios.get(
        `/api/v1/departments/${departmentId}/levels/${levelId}/courses`,
        { withCredentials: true }
      );
    } else {
      res = await axios.get(`/api/v1/courses/${pageSize}/${pageNum}`,
        { withCredentials: true }
      );
    }
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching courses");
  }
};

// Assign a course to a department
export const assignCoursesToDepartmentAPI = async (departmentId, courseId) => {
  try {
    const res = await axios.post(
      `/api/v1/departments/${departmentId}/courses/${courseId}`,
      {},
      { withCredentials: true }
    );
    return res.data;
  } catch (error) {
    handleApiError(error, "assigning course");
  }
};

// Remove a course from a department
export const removeCoursesFromDepartmentAPI = async (departmentId, courseId) => {
  try {
    const res = await axios.delete(
      `/api/v1/departments/${departmentId}/courses/${courseId}`,
      { withCredentials: true }
    );
    showToast("Course removed successfully!", "success");
    return res.data;
  } catch (error) {
    handleApiError(error, "removing course");
  }
};
