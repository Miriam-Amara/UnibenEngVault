import axios from "axios";


// Add new department
export const addDepartmentAPI = async (data) => {
  const res = await axios.post("/api/v1/departments", data, {
    withCredentials: true,
  });
  return res.data;
};

// Fetch paginated departments
export const fetchDepartmentsAPI = async (pageSize = 13, pageNum = 1) => {
  const res = await axios.get(`/api/v1/departments/${pageSize}/${pageNum}`, {
    withCredentials: true,
  });
  return res.data;
};

// Update department
export const updateDepartmentAPI = async (id, data) => {
  const res = await axios.put(`/api/v1/departments/${id}`, data, {
    withCredentials: true,
  });
  return res.data;
};

// Delete department
export const deleteDepartmentAPI = async (id) => {
  const res = await axios.delete(`/api/v1/departments/${id}`, {
    withCredentials: true,
  });
  return res.data;
};
