import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as Yup from "yup";


function LoginForm() {

  const [formData, setFormData] = useState(
    {
      email: "",
      password: ""
    }
  );

  const validationSchema = Yup.object(
    {
      email: Yup.string().required("Email is required").email("Invalid email format"),
      password: Yup.string().required("Password is required")
    }
  );

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, {abortEarly: false});
      const response = await axios.post(
        "/api/v1/auth_session/login",
        formData,
        {withCredentials: true}
      );

      console.log("Login successful: ", response.data);

      const res = await axios.get("/api/v1/users/me", {
          withCredentials: true,
      });
      const user = res.data;

      if (user.is_admin) {
          navigate("/admin/dashboard");
      } else {
          navigate("/mycourses");
      }

      setFormData({
        email: "",
        password: ""
      });

    } catch (error){
        if (error.inner) {
          const newError = {};
          error.inner.forEach((err) => {
            newError[err.path] = err.message;
          });
          setErrors(newError);
          return;
        }
        if (axios.isAxiosError(error)) {
          if (error.response) {
            const status = error.response.status;
            let message = "An unexpected error occurred. Please try again.";
            
            switch (status) {
              case 401:
                message = "Unauthorized.";
                break;
              case 404:
                message = "Incorrect email.";
                break;
              case 500:
                message = "Server error. Please try again later.";
                break;
              default:
                message = error.response?.message || message;
            }
            alert(message);
          }
        }else{
          console.error("Unexpected error: ", error);
          alert("Something went wrong. Please try again.");
        }
      }
  };

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData({
        ...formData,
        [name]: value
      });
  };

  return (
  <form onSubmit={handleSubmit}>
    <div>
      <label>Email Address</label>
      <input 
        type="email"
        name="email"
        value={formData.email}
        placeholder="Enter your email address"
        onChange={handleChange}
      />
      {errors.email && <p>{errors.email}</p>}
    </div>
    <div>
      <label>Password</label>
      <input
        type={showPassword ? "text" : "password"}
        name="password"
        value={formData.password}
        placeholder="Enter your password"
        onChange={handleChange}
      />
      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
      >
        {showPassword ? "👁️" : "🙈"}
      </button>
      {errors.password && <p>{errors.password}</p>}
    </div>
    <button type="submit">Login</button>
  </form>);
}

function Login(){

    return(
        <div>
            <div>
                <h2>
                    UnibenEngVault
                </h2>
                <h1>
                    Welcome <br />Back
                </h1>
                <p>
                    Welcome back! Login and continue
                    your learning journey.
                </p>
            </div>
            <div>
              <LoginForm />
            </div>
        </div>
    )
}

export default Login;