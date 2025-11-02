import axios from "axios";
import { showToast } from "../utils/toast";

import handleApiError from "./errorHandler";


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
  semester = "",
}) => {
   try {
    let res;
    let url;
    const params = {};

    if (departmentId && levelId) {
      url = `/api/v1/departments/${departmentId}/levels/${levelId}/courses`;
    } else {
      url = `/api/v1/courses/${pageSize}/${pageNum}`;
    }

    if (semester) params.semester = semester;

    res = await axios.get(url, {
      params,
      withCredentials: true,
    });
    return res.data;
  } catch (error) {
    console.log(error)
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
