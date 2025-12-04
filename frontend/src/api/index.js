/* */

import api from "./api";
import { showToast } from "../components/ui/Toast";


export async function fetchStatsApi() {
  try {
    const response = api.get("/stats");
    return response?.data;
  } catch (error) {
    if (error.message)
      showToast(error?.response?.data?.error || "Error fetching stats.", "error");
    console.error("Error fetching stats: ", error);
    throw error;
  }
}