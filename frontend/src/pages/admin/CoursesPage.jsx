// CoursesPageView.jsx (main component)

import { useState, useEffect } from "react";

import Layout from "../../components/Layout";
import { fetchCoursesAPI, deleteCourseAPI } from "../api/courses";
import { fetchDepartmentsAPI } from "../api/departments";
import { fetchLevelsAPI } from "../api/levels";
import CourseForm from "../../components/CourseForm";
import AssignCoursesForm from "../../components/AssignCoursesForm";
import { showToast } from "../utils/toast";
import "./mainPage.css"


function CoursesTableView({
  courses,
  loading,
  onEdit,
  onDelete,
  pageNum,
  totalCourses,
  onPageChange,
  pageSize,
}) {

  return (
    <>
      {/* Courses Table */}
      <section className="table-section">
        <table>
          <thead>
            <tr>
              <th>Course Code</th>
              <th>Semester</th>
              <th>Credit Load</th>
              <th>Level</th>
              <th>Title</th>
              <th>Departments</th>
              <th>No. of Files</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td>Loading...</td></tr>
            ) : courses.length === 0 ? (
              <tr><td>No courses found.</td></tr>
            ) : (
              courses.map(course => (
                <tr key={course.id}>
                  <td>{course.course_code}</td>
                  <td>{course.semester}</td>
                  <td>{course.credit_load}</td>
                  <td>{course.level}</td>
                  <td>{course.title}</td>
                  <td>
                    {course.departments?.length ? course.departments.join(", ") : "Unassigned"}
                  </td>
                  <td>{course.files}</td>
                  <td className="actions">
                    <button onClick={() => onEdit(course)}>Edit</button>
                    <button onClick={() => onDelete(course.id)}>Delete</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
        {/* Pagination */}
        <div>
          <button
            disabled={pageNum === 1}
            onClick={() => onPageChange(pageNum - 1)}>
              Prev
          </button>
          <span>Page {pageNum} — Total: {totalCourses}</span>
          <button
            disabled={pageNum * pageSize >= totalCourses}
            onClick={() => onPageChange(pageNum + 1)}>
              Next
          </button>
        </div>
      </section>
    </>
  );
}


function CoursesPageView() {
  const [departmentId, setDepartmentId] = useState("");
  const [levelId, setLevelId] = useState("");
  const [semester, setSemester] = useState("");
  const [pageNum, setPageNum] = useState(1);
  const pageSize = 20;

  const [departments, setDepartments] = useState([]);
  const [levels, setLevels] = useState([]);
  const [courses, setCourses] = useState([]);
  const [totalCourses, setTotalCourses] = useState(0);

  const [loading, setLoading] = useState(false);
  const [showCourseForm, setShowCourseForm] = useState(false);
  const [showAssignForm, setShowAssignForm] = useState(false);
  const [editData, setEditData] = useState(null);

  // Load departments and levels once
  useEffect(() => {
    fetchDepartmentsAPI()
    .then(setDepartments)
    .catch(() => showToast("Failed to load departments", "error"));

    fetchLevelsAPI()
    .then(setLevels)
    .catch(() => showToast("Failed to load levels", "error"));
  }, []);
  
  // Load courses on filters/page change
  const fetchCourses = () => {
    setLoading(true);
    fetchCoursesAPI({
      pageSize,
      pageNum,
      departmentId: departmentId || undefined,
      levelId: levelId || undefined,
      semester: semester || undefined,
    })
      .then((data) => {
        setCourses(data);
        setTotalCourses(data.total || 0);
      })
      // .catch(() => showToast("Failed to load courses", "error"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchCourses();
  }, [departmentId, levelId, semester, pageNum]);

  
  const handleEdit = (course) => {
    setEditData(course);
    setShowCourseForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this course?")) return;
    try {
      await deleteCourseAPI(id);
      showToast("Course deleted successfully", "success");
      fetchCourses();
      setPageNum(1);
    } catch {
      showToast("Failed to delete course", "error");
    }
  };

  const onDepartmentChange=(e) => { setDepartmentId(e.target.value); setPageNum(1); }
  const onLevelChange=(e) => { setLevelId(e.target.value); setPageNum(1); }
  const onSemesterChange=(e) => { setSemester(e.target.value); setPageNum(1); }

  return (
    <main className="main">
      <section className="header-section">
        <div className="header-section-items">
          <h3>Courses</h3>
          <p>Add, edit, view and delete courses from UnibenEngVault</p>
        </div>
      </section>

      <section className="control-section">
        
        {/* Buttons */}
        <div className="control-section-buttons">
          <button onClick={() => { setEditData(null); setShowCourseForm(true); }}>
            Add Course
          </button>

          <button onClick={() => setShowAssignForm(true)}>
            Assign/Remove Courses
          </button>
        </div>

        {showCourseForm && (
        <CourseForm
          onClose={() => setShowCourseForm(false)}
          onSaved={() => {
            setShowCourseForm(false);
            fetchCourses();
            setPageNum(1);
          }}
          editData={editData}
        />
      )}

        {showAssignForm && (
          <AssignCoursesForm
            onClose={() => setShowAssignForm(false)}
            onSaved={() => {
              setShowAssignForm(false);
              fetchCourses();
              setPageNum(1);
            }}
            departments={departments}
            courses={courses}
          />
        )}

        {/* Filters */}
        <div className="filter">
          <div>
            <label>Departments: </label>
            <select value={departmentId} onChange={onDepartmentChange}>
              <option value="">All Departments</option>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>{d.dept_name}</option>
              ))}
            </select>
          </div>

          <div>
            <label>Levels: </label>
            <select value={levelId} onChange={onLevelChange}>
              <option value="">All Levels</option>
              {levels.map((lvl) => (
                <option key={lvl.id} value={lvl.id}>{lvl.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label>Semester: </label>
            <select value={semester} onChange={onSemesterChange}>
              <option value="">Semester</option>
              {["first", "second"].map((sems) => (
                <option key={sems} value={sems}>{sems}</option>
              ))}
            </select>
          </div>
        </div>
      </section>
        

        <CoursesTableView          
          courses={courses}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
          pageNum={pageNum}
          totalCourses={totalCourses}
          onPageChange={setPageNum}
          pageSize={pageSize}
        />
    </main>
  );
}

const CoursesPage = () => <Layout main={<CoursesPageView />} />;

export default CoursesPage;
