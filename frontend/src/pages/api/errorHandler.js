import { showToast } from "../utils/toast";


// Helper for error handling
export default function handleApiError (error, action = "operation") {
  console.log("handleApiError called with status:", error.response?.status);
  if (error.response) {
    const { status, data } = error.response;
    console.log("handleApiError data?.error:", data?.error);
    switch (status) {
      case 400:
        showToast(data?.error || "Bad request", "error");
        break;
      case 401:
        showToast("Unauthorized: Please log in again.", "error");
        break;
      case 403:
        showToast("Forbidden: You're not supposed to be here", "error");
        break;
      case 404:
        showToast(data?.error || "Not found: The requested resource could not be found.", "error");
        break;
      case 409:
        showToast(data?.error || "Conflict: Duplicate or invalid data.", "error");
        break;
      case 500:
        showToast("Server error: Please try again later.", "error");
        break;
      default:
        showToast(data?.error || `An error occurred during ${action}.`, "error");
    }
  } else {
    showToast("Network error: Unable to reach the server.", "error");
  }
  // throw error;
};