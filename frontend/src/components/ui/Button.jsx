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

  const base = "border-0 rounded-10 flex justify-center items-center cursor-pointer";

  const variants = {
    primary: "text-white font-semibold bg-primary hover-bg-primary-dark",
    secondary: "text-white font-semibold bg-secondary hover-bg-secondary-dark",
    danger: "font-semibold bg-warn hover-bg-secondary-dark",
    outline: "text-primary font-semibold border bg-white hover-bg-grey-light",
    icon: "",
  }

  const shadow = {
    primary: "",
    secondary: "shadow-secondary-dark-sm"
  }

  const sizes = {
    sm: "",
    md: "btn-md",
    lg: `py-3 px-15 ${shadow[variant]}`
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
