/**
 * 
 */


export function Button({
  type = "button",
  variant = "primary",
  size = "medium",
  className = "",
  onClick,
  children
}) {

  const base = "border-0 rounded-10 cursor-pointer";

  const variants = {
    primary: "text-white font-semibold bg-primary hover-bg-primary-dark",
    secondary: "text-white font-semibold bg-secondary hover-bg-secondary-dark shadow-secondary-dark-sm",
    danger: "",
    outline: "text-primary font-semibold border bg-white hover-bg-primary-light",
  }

  const sizes = {
    sm: "",
    md: "py-2 px-10",
    lg: "py-3 px-15"
  }

  return(
    <button
      type={type}
      onClick={onClick}
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {children}
    </button>
  );
}