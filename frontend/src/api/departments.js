/* */

import api from "./api";
import { showToast } from "../utility/toast";


export async function  addDepartmentApi({department_data}) {
  try {
    const response = await api.post("/departments", department_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error adding departments.", "error");
    console.error("Error adding departments: ", error);
    throw error;
  }
}


export async function updateDepartmentApi({department_id, department_data}) {
  try {
    const response = await api.put(`/departments/${department_id}`, department_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error updating departments.", "error");
    console.error("Error updating departments: ", error);
    throw error;
  }
}


export async function fetchAllDepartmentsApi({
  page_size, page_num, created_at, search_dept_name
}) {
  try {
    const response = await api.get(
      "/departments",
      {params:
        {
          page_size: page_size || null,
          page_num: page_num || null,
          date_time: created_at || null,
          search: search_dept_name || null,
        },
      }
    );
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching all departments.", "error");
    console.error("Error fetching all departments: ", error);
    throw error;
  }
}


export async function fetchDepartmentApi({department_id}) {
  try {
    const response = await api.get(`/departments/${department_id}`);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching department.", "error");
    console.error("Error fetching department: ", error);
    throw error;
  }
}


export async function deleteDepartmentApi({department_id}) {
  try {
    await api.delete(`/departments/${department_id}`);
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error deleting department.", "error");
    console.error("Error deleting department: ", error);
    throw error;
  }
}
