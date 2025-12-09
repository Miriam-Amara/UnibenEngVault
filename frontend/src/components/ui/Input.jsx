/**
 * 
 */

export function Input({
  type = "text",
  id,
  name,
  value,
  placeholder = "",
  onChange,
  disabled=false,
  size,
  className = "",
}) {

  const sizes = {
    sm: "px-1 py-1",
    lg: "py-1 px-3"
  }

  return (
    <input
      id={id}
      type={type}
      name={name}
      value={value}
      placeholder={placeholder}
      disabled={ disabled }
      onChange={onChange}
      className={`w-100 ${size ? sizes[size] : "py-1 px-3"} border-grey d-block bg-transparent ${className}`}
    />
  );
}
