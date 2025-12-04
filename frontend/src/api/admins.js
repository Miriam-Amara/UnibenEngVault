/* */

import api from "./api";
import { showToast } from "../components/ui/Toast";


export async function updateAdminApi({admin_id, admin_data}) {
  try{
    const response = await api.put(`/admins/${admin_id}`, admin_data);
    return response.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error updating admin.", "error");
    console.error("Error updating admin: ", error);
    throw error;
  }
}


export async function fetchAllAdminsApi() {
  try{
    const response = await api.get("/admins");
    return response.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching all admins.", "error");
    console.error("Error fetching all admins: ", error);
    throw error;
  }
}


export async function fetchAdminApi({admin_id}) {
  try{
    const response = await api.get(`/admins/${admin_id}`);
    return response.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching admin.", "error");
    console.error("Error fetching admin: ", error);
    throw error;
  }
}


export async function deleteAdminApi({admin_id}) {
  try{
    await api.delete(`/admins/${admin_id}`);
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error deleting admin.", "error");
    console.error("Error deleting admin: ", error);
    throw error;
  }
}