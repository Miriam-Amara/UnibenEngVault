import { useState, useEffect } from "react";
import * as Yup from "yup";

import { 
  addDepartmentAPI,
  deleteDepartmentAPI,
  fetchDepartmentsAPI,
  updateDepartmentAPI 
} from "../api/departments";
import Layout from "../../components/Layout";
import { showToast } from "../utils/toast";
import "./mainPage.css"



function useDepartments({ pageSize = 13, pageNum = 1 }) {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDepartments = async () => {
    setLoading(true);
    try {
      const data = await fetchDepartmentsAPI(pageSize, pageNum);
      setDepartments(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error fetching departments:", error);
      setDepartments([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDepartments();
  }, [pageSize, pageNum]);

  return { departments, fetchDepartments, loading };
}


function DepartmentForm({ mode = "add", existingData = null, onSuccess }) {
  const [formData, setFormData] = useState({ dept_name: "", dept_code: "" });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (existingData) setFormData(existingData);
  }, [existingData]);

  const validationSchema = Yup.object({
    dept_name: Yup.string()
      .required("Department name is required.")
      .matches(/engineering$/i, "Department name must end with 'engineering'."),
    dept_code: Yup.string()
      .required("Department code is required.")
      .length(3, "Department code must be exactly 3 characters."),
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, { abortEarly: false });

      if (mode === "edit") await updateDepartmentAPI(formData.id, formData);
      else await addDepartmentAPI(formData);

      showToast(
        `${formData.dept_name} ${mode === "edit" ? "updated" : "added"} successfully!`,
        "success");

      setFormData({ dept_name: "", dept_code: "" });
      if (onSuccess) onSuccess();
    } catch (error) {
      if (error.inner) {
        const newErrors = {};
        error.inner.forEach((err) => (newErrors[err.path] = err.message));
        setErrors(newErrors);
      } else if (error.response) {
        showToast(error.response.data?.error || "An unexpected error occurred.", "error");
      } else {
        console.error(error);
        showToast("Something went wrong.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="main-form">
        <h4>Add Departments</h4>
        <div className="main-form-input">
          <label>Department Name</label>
          <div>
            <input
              type="text"
              name="dept_name"
              value={formData.dept_name}
              placeholder="Enter department name"
              onChange={handleChange}
            />
            {errors.dept_name && <p className="error">{errors.dept_name}</p>}
          </div>
        </div>

        <div className="main-form-input">
          <label>Department Code</label>
          <div>
            <input
            type="text"
            name="dept_code"
            value={formData.dept_code}
            placeholder="Enter department code"
            onChange={handleChange}
          />
          {errors.dept_code && <p className="error">{errors.dept_code}</p>}
          </div>
        </div>

        <button type="submit" className="btn-sm">{mode === "edit" ? "Update" : "Add"}</button>
      </div>
    </form>
  );
}


function DepartmentRow({ dept, onEdit, onDelete }) {
  return (
    <tr>
      <td>{dept.dept_name}</td>
      <td>{dept.dept_code}</td>
      <td>{dept.courses}</td>
      <td>{dept.id}</td>
      <td className="actions">
        <button className= "btn-sm" onClick={() => onEdit(dept)}>Edit</button>
        <button className= "btn-dg" onClick={() => onDelete(dept.id)}>Delete</button>
      </td>
    </tr>
  );
}


function DepartmentPageView({ pageSize, pageNum }) {
  const { departments, fetchDepartments, loading } = useDepartments({ pageSize, pageNum });
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState("add");
  const [selectedDept, setSelectedDept] = useState(null);

  const handleEdit = (dept) => {
    setSelectedDept(dept);
    setFormMode("edit");
    setShowForm(true);
  };

  const handleDelete = async (deptId) => {
    if (!window.confirm("Are you sure you want to delete this department?")) return;

    try {
      await deleteDepartmentAPI(deptId);
      showForm("Department deleted successfully!");
      fetchDepartments();
    } catch (error) {
      console.error(error);
      showForm("Failed to delete department.");
    }
  };

  return (
    <main className="main">
      <section className="header-section">
        <div className="header-section-items">
          <h3>Departments</h3>
          <p>Add, edit, view and delete departments from UnibenEngVault</p>
        </div>
      </section>


      {/* forms, search, filters */}
      <section className="control-section">
        <button
          onClick={() => {
            setSelectedDept(null);
            setFormMode("add");
            setShowForm(true);
          }}
          className="btn-lg"
        >
          Add Department
        </button>
        
        {showForm && (
          <div className="modal-overlay" onClick={() => setShowForm(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={() => setShowForm(false)}>Close</button>
              <DepartmentForm
                mode={formMode}
                existingData={selectedDept}
                onSuccess={() => {
                  setShowForm(false);
                  fetchDepartments();
                }}
              />
            </div>
          </div>
        )}
      </section>
      

      {/* table */}
      <section className="table-section">
        {loading ? (
          <p>Loading departments...</p>
        ) : departments.length === 0 ? (
          <p>No department found. Please add some departments.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Code</th>
                <th>Total Courses</th>
                <th>ID</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {departments.map((dept) => (
                <DepartmentRow
                  key={dept.id}
                  dept={dept}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}


function DepartmentPage() {
  return <Layout main={<DepartmentPageView />} />;
}

export default DepartmentPage;
