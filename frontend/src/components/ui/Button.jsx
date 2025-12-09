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
    danger: "text-white font-semibold bg-error hover-bg-secondary-dark",
    outline: "text-primary font-semibold border-primary bg-white hover-bg-grey-light",
    icon: "bg-white",
  }

  const shadow = {
    primary: "",
    secondary: "shadow-secondary-dark-sm"
  }

  const sizes = {
    sm: "btn-sm",
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

export function ButtonIcon({ children, onClick, className }) {
  return (
    <button
      type="button"
      onClick={ onClick }
      className={ `p-1 border-0 bg-white flex justify-center items-center cursor-pointer ${className}` }
    >
      { children }      
    </button>
  );
}
