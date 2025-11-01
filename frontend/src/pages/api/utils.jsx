import axios from "axios";
import { useState, useEffect } from "react";
import * as Yup from "yup";

import Layout from "../../components/Layout";



function useDepartments({pageSize, pageNum}) {
  const [departments, setDepartments] = useState([]);
  const pagesize = pageSize ?? 13;
  const pagenum = pageNum?? 1;

  const fetchDepartments = () => {
    axios.get(`/api/v1/departments/${pagesize}/${pagenum}`, {withCredentials: true})
    .then((response) => {
      setDepartments(response.data);
      console.log(response.data);
    })
    .catch((error) => console.error("Error fetching departments:", error));
  };

  useEffect(() => {
    fetchDepartments();
  }, [pagesize, pagenum]);

  return { departments, fetchDepartments };
}


function DepartmentForm({ mode = "add", existingData = null, onSuccess }) {

  const [formData, setFormData] = useState(
    existingData || {
      dept_name: "",
      dept_code: "",
    }
  );

  useEffect(() => {
    if (existingData) {
      setFormData(existingData);
    }
  }, [existingData]);

  const validationSchema = Yup.object(
    {
      dept_name: Yup.string()
        .required("Department name is required.")
        .matches(/engineering$/i, "Department name must end with 'engineering'."),
      dept_code: Yup.string()
        .required()
        .length(3, "Department code must be exactly 3 characters."),
    }
  );

  const [errors, setErrors] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, {abortEarly: false});

      let response;
      if (mode === "edit") {
        response = await axios.put(
          `/api/v1/departments/${formData.id}`,
          formData,
          { withCredentials: true }
        );
        alert(`${formData.dept_name} updated successfully!`)
      }else {
        response = await axios.post(
          "/api/v1/departments",
          formData,
          {withCredentials: true}
        )
        alert(`${formData.dept_name} added successfully`);
      }

      console.log("Success", response.data);
      if (onSuccess) onSuccess();
      
      setFormData({dept_name: "", dept_code: ""});

    } catch (error){
      if (error.inner) {
        const newError = {};
        error.inner.forEach((err) => {
          newError[err.path] = err.message;
        });
        setErrors(newError)
        return;
      }
      if (axios.isAxiosError(error)) {
          if (error.response) {
            const status = error.response.status;
            let message = "An unexpected error occurred. Please try again.";
            
            switch (status) {
              case 409:
                message = "Department already exist";
                break;
              case 500:
                message = "Server error. Please try again later.";
                break;
              default:
                message = error.response?.message || message;
            }
            alert(message);
          }
        }else{
          console.error("Unexpected error: ", error);
          alert("Something went wrong. Please try again.");
        }
    }
  };

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData({
        ...formData,
        [name]: value
      });
  };

  return (
  <form onSubmit={handleSubmit}>
    <div>
      <label>Department Name</label>
      <input 
        type="text"
        name="dept_name"
        value={formData.dept_name}
        placeholder="Enter department name"
        onChange={handleChange}
      />
      {errors.dept_name && <p>{errors.dept_name}</p>}
    </div>
    <div>
      <label>Department Code</label>
      <input 
        type="text"
        name="dept_code"
        value={formData.dept_code}
        placeholder="Enter department code"
        onChange={handleChange}
      />
      {errors.dept_code && <p>{errors.dept_code}</p>}
    </div>
    <button type="submit">
      {mode === "edit" ? "update" : "Add"}
    </button>
  </form>);
}

function DepartmentPageView({pageSize, pageNum}){

  const { departments, fetchDepartments } = useDepartments({pageSize, pageNum})
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState("add");
  const [selectedDept, setSelectedDept] = useState(null);

  const handleEdit = (dept) => {
      setSelectedDept(dept);
      setFormMode("edit");
      setShowForm(true);
    }

    const handleDelete = async (deptId) => {
    const confirmed = window.confirm("Are you sure you want to delete this department?");
    if (!confirmed) return;

    try {
      await axios.delete(`/api/v1/departments/${deptId}`, { withCredentials: true });
      alert("Department deleted successfully!");
      fetchDepartments(); // refresh the table
    } catch (error) {
      alert("Failed to delete department. Please try again.");
      console.error("Delete error:", error);
    }
  };

    return(
        <main>
            <title>UnibenEngVault-Departments</title>
            <section>
                <h2>Departments</h2>
            </section>
            <div>
                <section>
                  <button onClick={() => {
                    setSelectedDept(null);
                    setFormMode("add");
                    setShowForm(true);
                    }}>
                      Add
                    </button>
                  {showForm && (
                    <div>
                        <button onClick={() => setShowForm(false)}>
                            close
                        </button>
                        <DepartmentForm
                          mode={formMode}
                          existingData={selectedDept}
                          onSuccess={() => {
                            setShowForm(false);
                            fetchDepartments();
                          }}
                        />
                    </div>
                  )}
                </section>
                <div>
                  {departments.length > 0 ? (
                    <table border="1" cellPadding="8" cellSpacing="0">
                      <thead>
                        <tr>
                          <th>Name</th>
                          <th>Code</th>
                          <th>Courses by Level</th>
                          <th>Total Courses</th>
                          <th>ID</th>
                          <th>Date Created</th>
                          <th>Last Updated</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {departments.map((dept) => (
                          <tr key={dept.id}>
                            <td>{dept.dept_name}</td>
                            <td>{dept.dept_code}</td>
                            <td>
                              <div>100L - {dept.dept_level_courses_count.level_100}</div>
                              <div>200L - {dept.dept_level_courses_count.level_200}</div>
                              <div>300L - {dept.dept_level_courses_count.level_300}</div>
                              <div>400L - {dept.dept_level_courses_count.level_400}</div>
                              <div>500L - {dept.dept_level_courses_count.level_500}</div>
                            </td>
                            <td>{dept.courses}</td>
                            <td>{dept.id}</td>
                            <td>{new Date(dept.created_at).toLocaleString()}</td>
                            <td>{new Date(dept.updated_at).toLocaleString()}</td>
                            <td>
                              <div onClick={() => handleEdit(dept)}>Edit</div>
                              <div onClick={() => handleDelete(dept.id)}>Delete</div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ): (
                    <p>Loading departments...</p>
                  )}
                </div>
            </div>
        </main>
    )
}

function DepartmentPage() {
  return (
    <>
      <Layout
        main={<DepartmentPageView />}
      />
    </>
  )
}

export default DepartmentPage;