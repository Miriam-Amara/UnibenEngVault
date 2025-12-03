/* */

import api from "./api";
import { showToast } from "../utility/toast";


export async function  addLevelApi({level_data}) {
  try {
    const response = await api.post("/levels", level_data);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error adding levels.", "error");
    console.error("Error adding levels: ", error);
    throw error;
  }
}


export async function fetchAllLevelsApi({
  page_size, page_num, created_at, search_level_name
}) {
  try {
    const response = await api.get(
      "/levels",
      {params:
        {
          page_size: page_size || null,
          page_num: page_num || null,
          date_time: created_at || null,
          search: search_level_name || null,
        },
      }
    );
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching all levels.", "error");
    console.error("Error fetching all levels: ", error);
    throw error;
  }
}


export async function fetchLevelApi({level_id}) {
  try {
    const response = await api.get(`/levels/${level_id}`);
    return response?.data
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching level.", "error");
    console.error("Error fetching level: ", error);
    throw error;
  }
}


export async function deleteLevelApi({level_id}) {
  try {
    await api.delete(`/levels/${level_id}`);
  }
  catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error deleting level.", "error");
    console.error("Error deleting level: ", error);
    throw error;
  }
}
