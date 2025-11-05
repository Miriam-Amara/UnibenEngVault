import axios from "axios";

import { showToast } from "../utils/toast";
import handleApiError from "./errorHandler";

// Base path (no trailing slash)
const BASE_URL = "/api/v1";



// upload file
export async function uploadFileAPI(courseId, formData) {
  try {
    const response = await axios.post(
      `${BASE_URL}/courses/${courseId}/files`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true,
      }
    );
    return response.data;
  } catch (error) {
    handleApiError(error, "uploading file")
  }
}



// fetch file metadata by status
export async function fetchFilesAPI(status = "approved", pageSize = 15, pageNum = 1) {
  try {
    const url = `${BASE_URL}/files/${status}/${pageSize}/${pageNum}`;
    const response = await axios.get(url, { withCredentials: true });
    return response.data;
  } catch (error) {
    handleApiError(error, "fetching files")
  }
}


// get approved files metadata
export async function fetchApprovedCourseFilesAPI(courseId) {
  try {
    const response = await axios.get(
      `${BASE_URL}/courses/${courseId}/files/approved`,
      { withCredentials: true }
    );
    return response.data;
  } catch (error) {
    handleApiError(error, "loading approved files")
    if (error.response)
      showToast(error.response.data?.error || "Failed to load approved files", "error");
  }
}


// update file metadata
export async function updateFileAPI(fileId, payload) {
  try {
    const response = await axios.put(
      `${BASE_URL}/files/${fileId}`,
      payload,
    {
      headers: { "Content-Type": "application/json" },
      withCredentials: true,
    }
  );
    return response.data;
  } catch (error) {
    handleApiError(error, "updating file metadata")
  }
}


// delete file
export async function deleteFileAPI(fileId) {
  try {
    const response = await axios.delete(
      `${BASE_URL}/files/${fileId}`,
      { withCredentials: true }
    );
    return response.data;
  } catch (error) {
    handleApiError(error, "deleting file")
  }
}


// download/serve files
export async function downloadFileAPI(fileId) {
  try {
    // Step 1: Get the presigned S3 URL from backend
    const response = await axios.get(`${BASE_URL}/${fileId}`, {
      withCredentials: true,
    });

    // Extract the URL from backend response
    const presignedUrl = response.data?.url;
    if (!presignedUrl) {
      throw new Error("No download URL returned from server.");
    }

    // Open the file in a new tab or trigger a download
    const a = document.createElement("a");
    a.href = presignedUrl;
    a.target = "_blank"; // or "_self" if you prefer direct download
    // a.download = ""; // optional — allows browser to download instead of preview
    document.body.appendChild(a);
    a.click();
    a.remove();

    showToast("File download started!", "success");
  } catch (error) {
    handleApiError(error, "downloading file");
  }
}
