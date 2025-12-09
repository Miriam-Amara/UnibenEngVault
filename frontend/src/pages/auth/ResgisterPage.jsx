/**
 * 
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { Button } from "../../components/ui/Button";
import { userValidationSchema } from "../../utility/forms_input_validations.js";
import { registerUserApi } from "../../api/users.js";
import { fetchAllDepartmentsApi } from "../../api/departments.js";
import { fetchAllLevelsApi } from "../../api/levels.js";
import hidePasswordIcon from "../../assets/password_hide_icon.png";
import showPasswordIcon from "../../assets/password_show_icon.png";




export const ShowPasswordImg = () => (
  <img
    src={ showPasswordIcon }
    alt="show password"
    className="w-5 bg-grey-light"
  />
);

export const HidePasswordImg = () => (
  <img
    src={ hidePasswordIcon }
    alt="hide password"
    className="w-5 bg-grey-light"
  />
);


export default function ResgisterPage() {
  const [ formData, setFormData ] = useState({
    email: "",
    department_id: "",
    level_id: "",
    password: "",
    confirm_password: "",
    is_admin: false
  });
  const [ errors, setErrors ] = useState({});
  const [ showPassword, setShowPassword ] = useState(false);
  const [ showConfirmPassword, setShowConfirmPassword ] = useState(false);

  const [ departments, setDepartments ] = useState([]);
  const [ levels, setLevels ] = useState([]);


  const fetchAllDepartments = async (params={}) => {
    try {
      const allDepartments = await fetchAllDepartmentsApi(params);
      const options = allDepartments ? allDepartments.map((department) => ({
        value: department.id, label: department.dept_name
      })) : [];

      setDepartments(options);

    } catch (error) {
      console.error("Error fetching departments", error);
    }
  };

  const fetchAllLevels = async (params={}) => {
    try {
      const allLevels = await fetchAllLevelsApi(params);
      const options = allLevels ? allLevels.map((level) => ({
        value: level.id, label: level.level_name
      })) : [];

      setLevels(options);

    } catch (error) {
      console.error("Error fetching levels", error);
    }
  };

  useEffect(() => {
    fetchAllDepartments();
    fetchAllLevels();
  }, []);


  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({...prev, [name]: value}));
  };

  let navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const validData = await userValidationSchema.validate(formData, { abortEarly: false });
      const registeredUser = await registerUserApi(validData);

      if (registeredUser) {
        setFormData({
          email: "",
          department_id: "",
          level_id: "",
          password: "",
          confirm_password: "",
          is_admin: false
        });
        navigate("/login");
      }
      
    } catch (error) {
      if (error.inner) {
        const newErrors = {};
        for (const err of error.inner)
          newErrors[err.path] = err.message;
        setErrors(newErrors);
      }
      console.error("Error submitting form: ", error);
    }
  }

  return(
    <main className="w-100 min-h-screen flex bg-img-desktop bg-contain">

      {/* ----------------------- INFO SECTION ----------------------- */}
      <section className="w-50 py-5 px-15 text-grey-light bg-primary-75 auth-section">
        <h3 className="mb-12 auth-section">UnibenEngVault</h3>
        <h1 className="mb-5">
          Hello,
          <br />
          Welcome
        </h1>
        <p className="pr-18 auth-section">
          Empower your learning register on UnibenEngVault to access
          all materials and take your studies to the next level!
        </p>
      </section>

      {/* ----------------------- FORM SECTION ----------------------- */}
      <section className="w-50 py-2 px-18 auth-form">
        <h2 className="mb-6 text-primary-dark">Register</h2>

        <form onSubmit={handleSubmit} className="flex flex-col gap-1 auth-form">

          <div>
            <label>Email Address</label>
            <Input
              type="email"
              name="email"
              value={formData.email}
              placeholder="Enter your email address"
              onChange={handleChange}
              className="mt-1 mb-1 border-0 border-b-2 border-grey-dark outline-none"
            />
            { errors.email && <p className="text-sm text-error">{ errors.email }</p> }
          </div>

          <div className="relative">
            <label>Password</label>
            <div>
              <Input
                type={ showPassword ? "text" : "password" }
                name="password"
                value={ formData.password }
                placeholder="Enter your password"
                onChange={ handleChange }
                className="mt-1 border-0 border-b-2 outline-none"
              />
              <Button
                type="button"
                variant="icon"
                size="sm"
                className="absolute right-0 top-6"
                onClick={ () => setShowPassword(!showPassword) }
                children={ showPassword ? <ShowPasswordImg /> : <HidePasswordImg />}
              />
              { errors.password && <p className="text-sm text-error">{ errors.password }</p> }
            </div>
          </div>

          <div className="relative">
            <label>Confirm Password</label>
            <div>
              <Input
                type={ showConfirmPassword ? "text" : "password" }
                name="confirm_password"
                value={ formData.confirm_password }
                placeholder="Confirm your password"
                onChange={ handleChange }
                className="mt-1 border-0 border-b-2 outline-none"
              />
              <Button
                type="button"
                variant="icon"
                size="sm"
                className="absolute right-0 top-6"
                onClick={ () => setShowConfirmPassword(!showConfirmPassword) }
                children={ showConfirmPassword ?
                <ShowPasswordImg /> :
                <HidePasswordImg />
                }
              />
              { errors.confirm_password && <p className="text-sm text-error">{ errors.confirm_password }</p> }
            </div>
          </div>

          <div>
            <label>Department</label>
            <Select
              name="department_id"
              value={ formData.department_id }
              options={ departments }
              onChange={handleChange}
              className="mt-1 border-0 border-b-2 outline-none"
              id=""
            />
            { errors.department_id && <p className="text-sm text-error">{ errors.department_id }</p> }
          </div>

          <div className="mb-5">
            <label>Level</label>
            <Select
              name="level_id"
              value={ formData.level_id }
              options={ levels }
              onChange={handleChange}
              className="mt-1 border-0 border-b-2 outline-none"
              id=""
            />
            { errors.level_id && <p className="text-sm text-error">{ errors.level_id }</p> }
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="text-h5"
            children="Register"
          />
        </form>
      </section>
    </main>
  );
}