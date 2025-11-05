import axios from "axios";
import { showToast } from "../utils/toast";


import handleApiError from "./errorHandler";



// Register user
export const addUserAPI = async (data) => {
  try {
    const res = await axios.post("/api/v1/register", data, {withCredentials: true});
    showToast("User added successfully!", "success");
    return res.data;
  } catch (error) {
    handleApiError(error, "adding user")
  }
};

// Fetch user by id
export const fetchUserByIdAPI = async (id, data) => {
  try {
    const res = await axios.put(`/api/v1/users/${id}`, data, {
      withCredentials: true,
    });
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching user")
  }
};


// Fetch paginated users
export const fetchUsersAPI = async (departmentId, levelId, pageSize = 20, pageNum = 1) => {
  try {
    let url = `/api/v1/users`;

    if (departmentId && levelId) {
      url += `/${departmentId}/${levelId}/${pageSize}/${pageNum}`;
    } else {
      url += `/${pageSize}/${pageNum}`;
    }

    const res = await axios.get(url, { withCredentials: true });
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching users");
  }
};


// Update user
export const updateUserAPI = async (id, data) => {
  try {
    const res = await axios.put(`/api/v1/users/${id}`, data, {
    withCredentials: true,
    });
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching users");
  }
};

// Delete user
export const deleteUserAPI = async (id) => {
  try {
    const res = await axios.delete(`/api/v1/users/${id}`, {
    withCredentials: true,
    });
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching users");
  }
};
