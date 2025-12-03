/* */

import api from "./api";
import { showToast } from "../utility/toast";


export async function  registerUserApi({user_data}) {
  try {
    const response = await api.post("/register", user_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error adding users.", "error");
    console.error("Error adding users: ", error);
    throw error;
  }
}


export async function updateUserApi({user_id, user_data}) {
  try {
    const response = await api.put(`/users/${user_id}`, user_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error updating users.", "error");
    console.error("Error updating users: ", error);
    throw error;
  }
}


export async function fetchAllUsersApi({
  page_size, page_num, created_at, search_email
}) {
  try {
    const response = await api.get(
      "/users",
      {params:
        {
          page_size: page_size || null,
          page_num: page_num || null,
          date_time: created_at || null,
          search: search_email || null,
        },
      }
    );
    return response?.data;
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching all users.", "error");
    console.error("Error fetching all users: ", error);
    throw error;
  }
}


export async function fetchUsersByDepartmentAndLevel({
  department_id, level_id, page_size, page_num
}) {
  try {
    const response = await api.get(
      `/users/${department_id}/${level_id}`,
      {params: {
        page_size: page_size || null,
        page_num: page_num || null,
      }}
    );
    return response?.data;
  } catch (error) {
    const err_msg = "Error fetching users by department and level."
    
    if (error.message) {
      showToast(error?.response?.data?.error || err_msg, "error");
    }
    console.error("Error fetching users by department and level: ", error);
    throw error;
  }
}


export async function fetchUserApi({user_id}) {
  try {
    const response = await api.get(`/users/${user_id}`);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching user.", "error");
    console.error("Error fetching user: ", error);
    throw error;
  }
}


export async function deleteUserApi({user_id}) {
  try {
    await api.delete(`/users/${user_id}`);
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error deleting user.", "error");
    console.error("Error deleting user: ", error);
    throw error;
  }
}
