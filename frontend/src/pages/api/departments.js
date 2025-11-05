import axios from "axios";

import { showToast } from "../utils/toast";
import handleApiError from "./errorHandler";


// Add new department
export const addDepartmentAPI = async (data) => {
  try{
    const res = await axios.post("/api/v1/departments", data, {withCredentials: true});
    showToast("Department added successfully!", "success")
    return res.data;
  } catch (error) {
    handleApiError(error, "adding department")
  }
};

// Fetch paginated departments
export const fetchDepartmentsAPI = async (pageSize = 13, pageNum = 1) => {
  try{
    const res = await axios.get(`/api/v1/departments/${pageSize}/${pageNum}`, {withCredentials: true});
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching departments")
  }
};

// Update department
export const updateDepartmentAPI = async (id, data) => {
  try{
    const res = await axios.put(`/api/v1/departments/${id}`, data, {withCredentials: true});
    showToast("Successful!", "success")
    return res.data;
  } catch (error) {
    handleApiError(error, "updating department")
  }
};

// Delete department
export const deleteDepartmentAPI = async (id) => {
  try{
    const res = await axios.delete(`/api/v1/departments/${id}`, {withCredentials: true});
    showToast("Department deleted sucessfully!", "success")
    return res.data;
  } catch (error) {
    handleApiError(error, "deleting department")
  }
};
