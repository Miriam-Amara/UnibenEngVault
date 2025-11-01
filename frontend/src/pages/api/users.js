import axios from "axios";



// Register user
export const addUserAPI = async (data) => {
  const res = await axios.post("/api/v1/register", data, {
    withCredentials: true,
  });
  return res.data;
};

// Fetch user by id
export const fetchUserByIdAPI = async (id, data) => {
  const res = await axios.put(`/api/v1/users/${id}`, data, {
    withCredentials: true,
  });
  return res.data;
};

// Fetch paginated users
export const fetchUsersAPI = async (departmentId, levelId, pageSize = 13, pageNum = 1) => {
  const res = await axios.get(`/api/v1/users/${departmentId}/${levelId}/${pageSize}/${pageNum}`, {
    withCredentials: true,
  });
  return res.data;
};

// Update user
export const updateUserAPI = async (id, data) => {
  const res = await axios.put(`/api/v1/users/${id}`, data, {
    withCredentials: true,
  });
  return res.data;
};

// Delete user
export const deleteUserAPI = async (id) => {
  const res = await axios.delete(`/api/v1/users/${id}`, {
    withCredentials: true,
  });
  return res.data;
};
