/**
 * 
 * @param {*} param0 
 * @returns 
 */


export function Select({
  id = "",
  name,
  value, 
  options = [],
  onChange,
  selectType = "",
  size,
  className = "",
  disabled = false,
  ...rest
}) {

  const selectId = id || name;

  const sizes = {
    sm: "px-1 py-1",
    lg: "py-1 px-3"
  }

  return (
    <select
      id={selectId}
      name={name}
      value={value}
      onChange={onChange}
      disabled={disabled}
      className={`w-100 ${size ? sizes[size] : "py-1 px-3"} border-grey d-block bg-transparent ${className}`}
      {...rest}
    >
      <option value="">
        Select { selectType }
      </option>
      {options.map(({ value: optionValue, label: optionLabel }) => (
        <option key={optionValue} value={optionValue}>
          {optionLabel}
        </option>
      ))}
    </select>
  );
}
