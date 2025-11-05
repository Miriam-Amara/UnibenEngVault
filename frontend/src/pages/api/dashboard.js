import axios from "axios";

import handleApiError from "./errorHandler";



export const fetchStatsAPI = async () => {
  try {
    const res = await axios.get("/api/v1/stats", {
      withCredentials: true,
    });
    return res.data;
  } catch (error) {
    console.error("Error fetching stats:", error);
    handleApiError(error, "fetching stats")
  }
};
