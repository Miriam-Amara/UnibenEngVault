/**
 * Show a toast notification
 * @param {string} message - The text to show
 * @param {'success'|'error'|'info'|'warning'} type - Type of toast
 */


export function showToast(message, type="info") {
  return (
    <div>
      <div className={type}>
        {message}
      </div>
    </div>
  );
}