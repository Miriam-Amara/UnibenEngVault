import axios from "axios";

// Add new level
export const addLevelAPI = async (data) => {
  const res = await axios.post("/api/v1/levels", data, {
    withCredentials: true,
  });
  return res.data;
};

// Fetch paginated levels
export const fetchLevelsAPI = async (pageSize = 8, pageNum = 1) => {
  const res = await axios.get(`/api/v1/levels/${pageSize}/${pageNum}`, {
    withCredentials: true,
  });
  return res.data;
};


// Delete level
export const deleteLevelAPI = async (id) => {
  const res = await axios.delete(`/api/v1/levels/${id}`, {
    withCredentials: true,
  });
  return res.data;
};
