import axios from "axios";

import handleApiError from "./errorHandler";



// Add new level
export const addLevelAPI = async (data) => {
  try {
    const res = await axios.post("/api/v1/levels", data, {withCredentials: true});
    return res.data;
  } catch (error) {
    handleApiError(error, "adding level")
  }
};

// Fetch paginated levels
export const fetchLevelsAPI = async (pageSize = 8, pageNum = 1) => {
  try {
    const res = await axios.get(`/api/v1/levels/${pageSize}/${pageNum}`, {withCredentials: true});
    return res.data;
  } catch (error) {
    handleApiError(error, "fetching level")
  }
};


// Delete level
export const deleteLevelAPI = async (id) => {
  try {
    const res = await axios.delete(`/api/v1/levels/${id}`, {withCredentials: true});
    return res.data;
  } catch (error) {
    console.error(error.data)
    handleApiError(error, "deleting level")
  }
};
