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
  className = "",
}) {


  return (
    <input
      id={id}
      type={type}
      name={name}
      value={value}
      placeholder={placeholder}
      disabled={ disabled }
      onChange={onChange}
      className={`w-100 py-1 px-3 d-block bg-transparent ${className}`}
    />
  );
}
