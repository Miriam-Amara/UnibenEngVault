import axios from "axios";
import { useState, useEffect } from "react";
import * as Yup from "yup";


function useDepartments({pageSize, pageNum}) {

  const pagesize = pageSize ?? 13;
  const pagenum = pageNum?? 1;

  const [departments, setDepartments] = useState([]);
  useEffect(() => {
    axios.get(`/api/v1/departments/${pagesize}/${pagenum}`)
    .then((response) => {
      console.log(response.data);
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
    .catch((error) => console.error("Error fetching departments:", error));
  }, [pagesize, pagenum]);

  return levels
}


function Form({pageSize, pageNum}) {

  const departments = useDepartments({ pageSize, pageNum });
  const levels = useLevels({ pageSize, pageNum })

  const [formData, setFormData] = useState(
    {
      email: "",
      department: "",
      level: "",
      password: "",
      confirmpassword: ""
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, {abortEarly: false})
      console.log("Form Submitted", formData);
    }
    catch (error){
      const newError = {};
      error.inner.forEach((err) => {
        newError[err.path] = err.message;
      });
      setErrors(newError)
    }
  };

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData(
      {
        ...formData,
        [name]: value
      }
    );
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
                <option key={department.id} value={department.name}>
                  {department.name}
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
        type="password"
        name="password"
        value={formData.password}
        placeholder="Enter your password"
        onChange={handleChange}
      />
      {errors.password && <p>{errors.password}</p>}
    </div>
    <div>
      <label>Confirm Password</label>
      <input
        type="password"
        name="confirmpassword"
        value={formData.confirmpassword}
        placeholder="Confirm your password"
        onChange={handleChange}
      />
      {errors.confirmpassword && <p>{errors.confirmpassword}</p>}
    </div>
    <button type="submit">Register</button>
  </form>);
}

function Register(){

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
                    and take
                </p>
            </div>
            <div>
              <Form pageSize={13} pageNum={1} />
            </div>
        </div>
    )
}

export default Register;