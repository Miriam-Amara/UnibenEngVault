/**
 * 
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { userValidationSchema } from "../../utility/forms_input_validations";
import { updateUserApi } from "../../api/users";
import { fetchAllDepartmentsApi  } from "../../api/departments";
import { fetchAllLevelsApi } from "../../api/levels";
import { useAuth } from "../auth/AuthContext";
import AdminLayout from "../../components/layout/AdminLayout";
import StudentLayout from "../../components/layout/StudentLayout";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { Button } from "../../components/ui/Button";



function ProfilePageView(userData) {
  const [ user, setUser ] = useState({userData});
  const [ editForm, setEditForm ] = useState(false);
  const [ errors, setErrors ] = useState({});
  const [ viewDetails, setViewDetails ] = useState(false);

  const [ departments, setDepartments ] = useState([]);
  const [ levels, setLevels ] = useState([]);

  
  const fetchAllDepartments = async () => {
    try {
      const allDepartments = await fetchAllDepartmentsApi();
      const options = allDepartments ? allDepartments.map((department) => ({
        value: department.id, label: department.name
      })) : [];

      setDepartments(options);

    } catch (error) {
      console.error("Error fetching departments", error);
    }
  };

  const fetchAllLevels = async () => {
    try {
      const allLevels = await fetchAllLevelsApi();
      const options = allLevels ? allLevels.map((level) => ({
        value: level.id, label: level.name
      })) : [];

      setLevels(options);

    } catch (error) {
      console.error("Error fetching levels", error);
    }
  };

  // const fetchUser = async () => {
  //   try {
  //     const userData = await fetchUserApi()
  //     setUser(userData ?? [])
  //   } catch (error) {
  //     console.error("Error fetching user: ", error);
  //   }
  // }

  useEffect(() => {
    if (editForm) {
      console.log("Edit form: ", editForm);
      fetchAllDepartments();
      fetchAllLevels();
    }
  }, [editForm]);

  const handleChange = (e) => {
    const { name, value } = e.target
    setUser((prev) => ({ prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const validData = await userValidationSchema.validate(user, { abortEarly: false });
      const updatedUserData = await updateUserApi(user.id, validData);
      setUser(updatedUserData ?? []);

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

  return (
    <>
      
      {/* ------------------------- INFO SECTION ------------------------- */}
      <section>
        <img
          src=""
          alt=""
        />
        
        <div>
          <Button
            type="button"
            variant="primary"
            size="md"
            className=""
            onClick={ () => { setViewDetails(true); } }
            children="View Details"
          />

          <Button
            type="button"
            variant="primary"
            size="md"
            className=""
            onClick={ () => { setEditForm(true); } }
            children="Edit profile"
          />

          <Button
            type="button"
            variant="danger"
            size="md"
            className=""
            children="Close Account"
          />
        </div>
        
        {viewDetails &&
        <div>
          <p>Email: </p>
        </div>
        }
      </section>

      {/* ------------------------- FORM SECTION ------------------------- */}
      <section>
        <form onSubmit={ handleSubmit }>
            <div>
              <label>Email</label>
              <Input
                type="email"
                name="email"
                value={ user.email }
                onChange={ handleChange }
                className=""
              />
              {errors.email && <p>{ errors.email }</p>}
            </div>

            <div>
              <label>Department</label>
              {departments ?
              <Select
                name="department_id"
                value={ user.department_id }
                options={ departments }
                onChange={ handleChange }
                className=""
                disabled={ false }
              /> :
              
              <Input
                type="dept_name"
                name="dept_name"
                value={ user.dept_name }
                className=""
                disabled={ true }
              />}
              {errors.department_id && <p>{ errors.department_id }</p>}
            </div>

            <div>
              <label>Level</label>
              {levels ?
              <Select
                name="level"
                id={ user.id }
                value={ user.level_name }
                options={ levels }
                onChange={ handleChange }
                className=""
                disabled={ false }
              /> :
              
              <Select
                name="department"
                value={ user.level_name }
                options={ [{ value: user.id , label: user.level_name }] }
              />}
            </div>

            {editForm &&
            <Button
              type="submit"
              variant="primary"
              size="sm"
              className=""
              onClick={ () => {setEditForm(false);} }
              children="Save"
            />}

            {editForm &&
            <Button
              type="button"
              variant="primary"
              size="sm"
              className=""
              onClick={ () => {setEditForm(false);} }
              children="Cancel"
            />}
        </form>
      </section>
    </>
  );
}


export default function ProfilePage() {
  const user = useAuth();
  const navigate = useNavigate();

  if (!user)
    navigate("/");

  if (user.is_admin) {
    return (
      <>
      <AdminLayout
        Page={ <ProfilePageView userData={ user } /> }
      />
    </>
    );
    
  } else {
      return (
      <>
        <StudentLayout
          Page={ <ProfilePageView userData={ user } /> }
        />
      </>
    );
  }
}
