import { useState, useEffect } from "react";
import * as Yup from "yup";

import {
  addUserAPI,
  updateUserAPI,
  deleteUserAPI,
  fetchUsersAPI,
} from "../api/users";
import { fetchDepartmentsAPI } from "../api/departments";
import { fetchLevelsAPI } from "../api/levels";
import Layout from "../../components/Layout";
import { showToast } from "../utils/toast";




// fetch users
function useUsers({ departmentId, levelId, pageSize = 20, pageNum = 1 }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await fetchUsersAPI(departmentId, levelId, pageSize, pageNum);
      setUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [pageSize, pageNum]);

  return { users, fetchUsers, loading };
}



function UserForm({ mode = "add", existingData = null, onSuccess }) {
  const [formData, setFormData] = useState({
    email: "",
    department_id: "",
    level_id: "",
    password: "",
    confirm_password: "",
    is_admin: false,
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (existingData) setFormData(existingData);
  }, [existingData]);

  const validationSchema =
    mode === "add"
      ? Yup.object({
          email: Yup.string().email("Invalid email").required("Email required"),
          department_id: Yup.string()
            .required("Department required")
            .length(36, "Department ID must be exactly 36 characters"),
          level_id: Yup.string()
            .required("Level required")
            .length(36, "Level id must be exactly 36 characters"),
          password: Yup.string()
            .min(8, "Password must be at least 8 characters")
            .required("Password required"),
          confirm_password: Yup.string()
            .oneOf([Yup.ref("password"), null], "Passwords must match")
            .required("Confirm password required"),
        })
      : Yup.object({
          department_id: Yup.string().length(36, "Department ID must be exactly 36 characters"),
          level_id: Yup.string().length(36, "Level ID must be exactly 36 characters."),
          is_admin: Yup.boolean(),
        });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, { abortEarly: false });

      if (mode === "edit") {
        await updateUserAPI(formData.id, {
          is_admin: formData.is_admin,
          department_id: formData.department_id,
          level_id: formData.level_id,
        });
      } else {
        await addUserAPI({
          email: formData.email,
          department_id: formData.department_id,
          level_id: formData.level_id,
          password: formData.password,
          confirm_password: formData.confirm_password,
        });
      }

      showToast(`User ${mode === "edit" ? "updated" : "registered"} successfully!`, "success");
      setFormData({
        email: "",
        department_id: "",
        level_id: "",
        password: "",
        confirm_password: "",
        is_admin: false,
      });
      if (onSuccess) onSuccess();
    } catch (error) {
      if (error.inner) {
        const newErrors = {};
        error.inner.forEach((err) => (newErrors[err.path] = err.message));
        setErrors(newErrors);
      } else if (error.response) {
        showToast(error.response.data?.error || "Server error occurred.", "error");
      } else {
        console.error(error);
        showToast("Something went wrong.", "error");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {mode === "add" && (
        <>
          <div>
            <label>Email</label>
            <input
              name="email"
              type="email"
              placeholder="Enter email"
              value={formData.email}
              onChange={handleChange}
            />
            {errors.email && <p>{errors.email}</p>}
          </div>

          <div>
            <label>Password</label>
            <input
              name="password"
              type="text"
              placeholder="Enter password"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && <p>{errors.password}</p>}
          </div>

          <div>
            <label>Confirm Password</label>
            <input
              name="confirm_password"
              type="text"
              placeholder="Confirm password"
              value={formData.confirm_password}
              onChange={handleChange}
            />
            {errors.confirm_password && <p>{errors.confirm_password}</p>}
          </div>
        </>
      )}

      <div>
        <label>Department ID</label>
        <input
          name="department_id"
          type="text"
          placeholder="Enter department ID"
          value={formData.department_id}
          onChange={handleChange}
        />
        {errors.department_id && <p>{errors.department_id}</p>}
      </div>

      <div>
        <label>Level ID</label>
        <input
          name="level_id"
          type="text"
          placeholder="Enter level ID"
          value={formData.level_id}
          onChange={handleChange}
        />
        {errors.level_id && <p>{errors.level_id}</p>}
      </div>

      {mode === "edit" && (
        <div>
          <label>Is Admin</label>
          <input
            name="is_admin"
            type="checkbox"
            checked={formData.is_admin}
            onChange={handleChange}
          />
        </div>
      )}

      <button type="submit">{mode === "edit" ? "Update" : "Register"}</button>
    </form>
  );
}




function UserRow({ user, onEdit, onDelete }) {
  return (
    <tr>
      <td>{user.email}</td>
      <td>{user.department}</td>
      <td>{user.level}</td>
      <td>{user.id}</td>
      <td>{new Date(user.created_at).toLocaleString()}</td>
      <td>{new Date(user.updated_at).toLocaleString()}</td>
      <td>
        <button onClick={() => onEdit(user)}>Edit</button>
        <button onClick={() => onDelete(user.id)}>Delete</button>
      </td>
    </tr>
  );
}




function UsersPageView({ pageSize, pageNum }) {

  const [departmentId, setDepartmentId] = useState("");
  const [levelId, setLevelId] = useState("");
  const [departments, setDepartments] = useState([]);
  const [levels, setLevels] = useState([]);

  const { users, fetchUsers, loading } = useUsers({
    departmentId, levelId, pageSize, pageNum
  });
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState("add");
  const [selectedUser, setSelectedUser] = useState(null);

  const handleEdit = (user) => {
    setSelectedUser(user);
    setFormMode("edit");
    setShowForm(true);
  };

  const handleDelete = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await deleteUserAPI(userId);
      alert("User deleted successfully!");
      fetchUsers();
    } catch (error) {
      console.error(error);
      alert("Failed to delete user.");
    }
  };

  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const deps = await fetchDepartmentsAPI();
        setDepartments(deps);
        const levs = await fetchLevelsAPI();
        setLevels(levs);
      } catch (error) {
        console.error("Error fetching filters", error);
      }
    };
    fetchFilters();
  }, []);

  return (
    <main>
      <section>
        <h2>Users</h2>
      </section>

      {/* Forms, search, filters */}
      <section>
        <button
          onClick={() => {
            setSelectedUser(null);
            setFormMode("add");
            setShowForm(true);
          }}
        >
          Register User
        </button>
        {showForm && (
          <div>
            <button onClick={() => setShowForm(false)}>Close</button>
            <UserForm
              mode={formMode}
              existingData={selectedUser}
              onSuccess={() => {
                setShowForm(false);
                fetchUsers();
              }}
            />
          </div>
        )}
        <div>
          <label>
            Department:{" "}
            <select
              value={departmentId}
              onChange={(e) => setDepartmentId(e.target.value)}
            >
              <option value="">All</option>
              {departments.map((dep) => (
                <option key={dep.id} value={dep.id}>
                  {dep.dept_name}
                </option>
              ))}
            </select>
          </label>

          <label style={{ marginLeft: "1rem" }}>
            Level:{" "}
            <select value={levelId} onChange={(e) => setLevelId(e.target.value)}>
              <option value="">All</option>
              {levels.map((lev) => (
                <option key={lev.id} value={lev.id}>
                  {lev.name}
                </option>
              ))}
            </select>
          </label>

          <button
            style={{ marginLeft: "1rem" }}
            onClick={() => fetchUsers()}
          >
            Filter
          </button>
        </div>
      </section>


      {/* Table */}
      <section>
        {loading ? (
          <p>Loading users...</p>
        ) : (
          <table border="1" cellPadding="8" cellSpacing="0">
            <thead>
              <tr>
                <th>Email</th>
                <th>Department</th>
                <th>Level</th>
                <th>ID</th>
                <th>Date Created</th>
                <th>Last Updated</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <UserRow
                  key={user.id}
                  user={user}
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


function UsersPage() {
  return <Layout main={<UsersPageView />} />;
}

export default UsersPage;
