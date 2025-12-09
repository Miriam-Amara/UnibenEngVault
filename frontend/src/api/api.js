/*
Implement a global axios for sending backend requests.
Redirects user to login if session expires.
*/

import axios from "axios";

const apiUrl = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: apiUrl + "/api/v1",
  withCredentials: true,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const skipRedirect = error.config?.skipAuthRedirect;
    if (error.response && error.response.status === 401 && !skipRedirect) {
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
