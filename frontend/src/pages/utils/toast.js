import Swal from "sweetalert2";
import "@sweetalert2/theme-dark/dark.css"; // optional theme

/**
 * Show a toast notification
 * @param {string} message - The text to show
 * @param {'success'|'error'|'info'|'warning'} type - Type of toast
 */
export function showToast(message, type = "info") {
  Swal.fire({
    toast: true,
    position: "top-end",
    icon: type,
    title: message,
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
  });
}
