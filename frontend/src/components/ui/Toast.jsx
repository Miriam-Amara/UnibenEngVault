/**
 * Show a toast notification
 * @param {string} message - The text to show
 * @param {'success'|'error'|'info'|'warn'} type - Type of toast
 */


import { Button } from "./Button";

export function ShowToast({
  message,
  type="info",
  size="",
  position="",
  className
}) {

  const types = {
    success: "bg-success",
    warn: "bg-warn",
    error: "bg-error",
    info: "bg-primary-light",
  }

  const sizes = {
    sm: "",
    md: "",
    large: "",
  }

  const positions = {
    center: "",
    topRight: "",
  }


  return (
    <div>
      <div 
        className={ ` ${types[type]} ${sizes[size]} ${positions[position]} ${className}` }
      >
        {message}
      </div>
    </div>
  );
}



export function ConfirmDialog({ message, onConfirm, onCancel }) {
  return (
    <div 
      className={ `${styles.overlay}` }
    >
      <div
        className={ `${styles.box}` }
      >
        <p>{message}</p>

        <div
          className="mt-3 flex gap-1"
        >
          <Button
            type="button"
            variant="outline"
            size="md"
            onClick={ onCancel }
            children="Cancel"
          />

          <Button
            type="button"
            variant="danger"
            size="md"
            onClick={ onConfirm }
            children="Yes, Delete"
          />
        </div>
      </div>
    </div>
  );
}

const styles = {
  overlay: "absolute h-screen w-screen top-0 left-0 bg-grey-dark-75 flex justify-center items-center",
  box: "text-center p-5 rounded-10 bg-white",
}
