import { useState, useEffect } from "react";
import { fetchCoursesAPI, deleteCourseAPI } from "../api/courses";
import { showToast } from "../utils/toast"; // same utility you already use

export function useCourses() {
  const [courses, setCourses] = useState([]);
  const [pageNum, setPageNum] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalCourses, setTotalCourses] = useState(0);
  const [departmentId, setDepartmentId] = useState("");
  const [level, setLevel] = useState("");
  const [unassigned, setUnassigned] = useState(false);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch courses
  const fetchCourses = async () => {
    try {
      setLoading(true);
      const data = await fetchCoursesAPI({
        pageNum,
        pageSize,
        departmentId,
        level,
        unassigned,
        search,
      });
      setCourses(data.items || []);
      setTotalCourses(data.total || 0);
    } catch (error) {
      console.error("Failed to fetch courses:", error);
      showToast("Failed to load courses", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, [pageNum, pageSize, departmentId, level, unassigned, search]);

  // Delete a course
  const deleteCourse = async (id) => {
    try {
      await deleteCourseAPI(id);
      showToast("Course deleted successfully", "success");
      fetchCourses();
    } catch (error) {
      showToast("Failed to delete course", "error");
    }
  };

  return {
    courses,
    totalCourses,
    loading,
    pageNum,
    setPageNum,
    pageSize,
    setPageSize,
    departmentId,
    setDepartmentId,
    level,
    setLevel,
    unassigned,
    setUnassigned,
    search,
    setSearch,
    fetchCourses,
    deleteCourse,
  };
}
