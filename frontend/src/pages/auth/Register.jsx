import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import * as Yup from "yup";
import "./authPage.css"


function useDepartments({pageSize, pageNum}) {

  const pagesize = pageSize ?? 13;
  const pagenum = pageNum?? 1;

  const [departments, setDepartments] = useState([]);
  useEffect(() => {
    axios.get(`/api/v1/departments/${pagesize}/${pagenum}`)
    .then((response) => {
      console.log("response data", response.data);
      setDepartments(response.data);
    })
    .catch((error) => console.error("Error fetching departments:", error));
  }, [pagesize, pagenum]);

  return departments
}

function useLevels({pageSize, pageNum}) {

  const pagesize = pageSize ?? 13;
  const pagenum = pageNum?? 1;

  const [levels, setLevels] = useState([]);
  useEffect(() => {
    axios.get(`/api/v1/levels/${pagesize}/${pagenum}`)
    .then((response) => {
      console.log(response.data);
      setLevels(response.data);
    })
    .catch((error) => console.error("Error fetching levels:", error));
  }, [pagesize, pagenum]);

  return levels
}


function RegisterForm({pageSize, pageNum}) {
  
  const departments = useDepartments({ pageSize, pageNum });
  const levels = useLevels({ pageSize, pageNum })

  console.log("Form rendered", { departments, levels });
  const [formData, setFormData] = useState(
    {
      email: "",
      department: "",
      level: "",
      password: "",
      confirmpassword: "",
    }
  );

  const validationSchema = Yup.object(
    {
      email: Yup.string().required("Email is required").email("Invalid email format"),
      department: Yup.string().required("Department is required"),
      level: Yup.string().required("Level is required"),
      password: Yup.string()
        .required("Password is required")
        .min(8, "Password must be at least 8 characters")
        .matches(/[0-9]/, "Password must contain at least one number")
        .matches(/[A-Z]/, "Password must contain at least one uppercase")
        .matches(/[a-z]/, "Password must contain at least one lowercase"),
      confirmpassword: Yup.string()
        .required("Confirm password is required")
        .oneOf([Yup.ref("password")], "Password must match"),

    }
  );

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, {abortEarly: false});
      const response = await axios.post("/api/v1/register", formData);
      console.log("Registration successful: ", response.data);

      setFormData({
        email: "",
        department: "",
        level: "",
        password: "",
        confirmpassword: "",
      });
      
      alert("Registration successful!");
      navigate("/login")

    } catch (error){
      if (error.inner) {
        const newError = {};
        error.inner.forEach((err) => {
          newError[err.path] = err.message;
        });
        setErrors(newError)
      } else {
          console.error("Error submitting form: ", error);
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
  <form onSubmit={handleSubmit} className="form">
    <div className="form-field">
      <label className="form-label">Email Address</label>
      <div>
        <input 
          type="email"
          name="email"
          value={formData.email}
          placeholder="Enter your email address"
          onChange={handleChange}
          className="form-input"
        />
        {errors.email && <p className="error">{errors.email}</p>}
      </div>
    </div>

    <div className="form-field">
      <label className="form-label">Department</label>
      <div>
        <select
          name="department"
          value={formData.department}
          onChange={handleChange}
          disabled={departments.length === 0}
          className="form-input"
        >
          {departments.length === 0 ? (
              <option value="">Loading departments...</option>
            ) : (
              <>
                <option value=""></option>
                {departments.map((department) => (
                  <option key={department.id} value={department.dept_name}>
                    {department.dept_name}
                  </option>
                  ))}
              </>
            )}
        </select>
        {errors.department && <p className="error">{errors.department}</p>}
      </div>
    </div>

    <div className="form-field">
      <label className="form-label">Level</label>
      <div>
        <select
          name="level"
          value={formData.level}
          onChange={handleChange}
          disabled={levels.length === 0}
          className="form-input"
        >
          {levels.length === 0 ? (
            <option value="">Loading levels...</option>
          ) : (
            <>
              <option value=""></option>
              {levels.map((level) => (
                <option key={level.id} value={level.name}>
                  {level.name}
                </option>
              ))}
            </>
          )}
        </select>
        {errors.level && <p className="error">{errors.level}</p>}
      </div>
    </div>

    <div className="form-field">
      <label className="form-label">Password</label>
        <div>
          <div className="form-password">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={formData.password}
              placeholder="Enter your password"
              onChange={handleChange}
              className="form-input-password"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="btn-password"
            >
              {showPassword ? "👁️" : "🙈"}
            </button>
          </div>
        {errors.password && <p className="error">{errors.password}</p>}
      </div>
    </div>

    <div className="form-field">
      <label className="form-label">Confirm Password</label>
      <div>
        <div className="form-password">
          <input
            type={showConfirmPassword ? "text" : "password"}
            name="confirmpassword"
            value={formData.confirmpassword}
            placeholder="Confirm your password"
            onChange={handleChange}
            className="form-input-password"
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="btn-password"
          >
            {showConfirmPassword ? "👁️" : "🙈"}
          </button>
        </div>
        {errors.confirmpassword && <p className="error">{errors.confirmpassword}</p>}
      </div>
    </div>

    <div className="btn-container">
      <button type="submit" className="btn-submit">Register</button>
    </div>

  </form>);
}

function Register(){
    console.log("Here in Register!")
    return(
        <main className="auth-main-body">
            <div className="auth-content">
                <div className="">
                    <h5>UnibenEngVault</h5>
                </div>
                
                <div className="auth-content-body">
                  <h1>
                    Hello, <br />Welcome
                  </h1>
                  <p>
                    Empower your learning,
                    register on UnibenEngVault to
                    access all materials and take
                    your studies to the next level!
                  </p>
                </div>
            </div>

            <div className="auth-container">
              <h3>Register</h3>
              <RegisterForm pageSize={13} pageNum={1} />
            </div>
        </main>
    )
}

export default Register;