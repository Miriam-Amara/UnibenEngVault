/**
 * 
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { Input } from "../../components/ui/Input";
import { Button } from "../../components/ui/Button";
import { loginValidationSchema } from "../../utility/forms_input_validations.js";
import { loginApi, fetchUserApi } from "../../api/users.js";
import { useAuth } from "./AuthContext.jsx";
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



export default function LoginPage() {

  const { login } = useAuth();
  const [ formData, setFormData ] = useState({
    email: "",
    password: "",
  });
  const [ errors, setErrors ] = useState({});
  const [ showPassword, setShowPassword ] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({...prev, [name]: value}));
  };

  let navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const validData = await loginValidationSchema.validate(
        formData, { abortEarly: false }
      );
      const loginSuccess = await loginApi(validData);

      if (loginSuccess) {
        const user = await fetchUserApi("me");

        login(user);
        navigate("/profile");
        setFormData({
          email: "",
          password: "",
        });
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
          Welcome,
          <br />
          Back
        </h1>
        <p className="pr-18 auth-section">
          Welcome back! Log in and continue your learning journey.
        </p>
      </section>

      {/* ----------------------- FORM SECTION ----------------------- */}
      <section className="w-50 py-2 px-18 auth-form">
        <h2 className="mb-6 text-primary-dark">Login</h2>
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

          <div className="relative mb-5">
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

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="text-h5"
            children="Login"
          />
        </form>
      </section>
    </main>
  );
}
