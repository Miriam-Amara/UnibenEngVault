/**
 * 
 * @param {*} param0 
 * @returns 
 */


export function Select({
  name,
  value, 
  options = [],
  onChange,
  className = "",
  id = "",
  disabled = false,
  ...rest
}) {
  const selectId = id || name;

  return (
    <select
      id={selectId}
      name={name}
      value={value}
      onChange={onChange}
      disabled={disabled}
      className={`w-100 py-1 px-3 d-block bg-transparent ${className}`}
      {...rest}
    >
      <option value="" disabled>
        Select
      </option>
      {options.map(({ value: optionValue, label: optionLabel }) => (
        <option key={optionValue} value={optionValue}>
          {optionLabel}
        </option>
      ))}
    </select>
  );
}
