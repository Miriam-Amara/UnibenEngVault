import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import * as Yup from "yup";


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
      <label>Department</label>
      <select
        name="department"
        value={formData.department}
        onChange={handleChange}
        disabled={departments.length === 0}
      >
        {departments.length === 0 ? (
            <option value="">Loading departments...</option>
          ) : (
            <>
              <option value="">Select Department</option>
              {departments.map((department) => (
                <option key={department.id} value={department.dept_name}>
                  {department.dept_name}
                </option>
                ))}
            </>
          )}
      </select>
      {errors.department && <p>{errors.department}</p>}
    </div>
    <div>
      <label>Level</label>
      <select
        name="level"
        value={formData.level}
        onChange={handleChange}
        disabled={levels.length === 0}
      >
        {levels.length === 0 ? (
          <option value="">Loading levels...</option>
        ) : (
          <>
            <option value="">Select Level</option>
            {levels.map((level) => (
              <option key={level.id} value={level.name}>
                {level.name}
              </option>
            ))}
          </>
        )}
      </select>
      {errors.level && <p>{errors.level}</p>}
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
    <div>
      <label>Confirm Password</label>
      <input
        type={showConfirmPassword ? "text" : "password"}
        name="confirmpassword"
        value={formData.confirmpassword}
        placeholder="Confirm your password"
        onChange={handleChange}
      />
      <button
        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
      >
        {showConfirmPassword ? "👁️" : "🙈"}
      </button>
      {errors.confirmpassword && <p>{errors.confirmpassword}</p>}
    </div>
    <button type="submit">Register</button>
  </form>);
}

function Register(){
    console.log("Here in Register!")
    return(
        <div>
            <div>
                <h2>
                    UnibenEngVault
                </h2>
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
            <div>
              <RegisterForm pageSize={13} pageNum={1} />
            </div>
        </div>
    )
}

export default Register;