/* */

import api from "./api";
import { showToast } from "../utility/toast";


export async function  addFileApi({file_data}) {
  try {
    const response = await api.post("/files", file_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error adding files.", "error");
    console.error("Error adding files: ", error);
    throw error;
  }
}


export async function updateFileApi({file_id}) {
  try {
    const response = await api.put(`/files/${file_id}`);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error updating files.", "error");
    console.error("Error updating files: ", error);
    throw error;
  }
}


export async function fetchAllFilesApi({
  page_size, page_num, created_at, search_file_name, file_status
}) {
  try {
    const response = await api.get(
      "/files",
      {params:
        {
          page_size: page_size || null,
          page_num: page_num || null,
          date_time: created_at || null,
          search: search_file_name || null,
          file_status: file_status || null,
        },
      }
    );
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching all files.", "error");
    console.error("Error fetching all files: ", error);
    throw error;
  }
}


export async function fetchFileApi({file_id}) {
  try {
    const response = await api.get(`/files/${file_id}`);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching file.", "error");
    console.error("Error fetching file: ", error);
    throw error;
  }
}


export async function deleteFileApi({file_id}) {
  try {
    await api.delete(`/files/${file_id}`);
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error deleting file.", "error");
    console.error("Error deleting file: ", error);
    throw error;
  }
}
