/**
 * 
 */

import { useEffect, useState } from "react";

import { updateUserValidationSchema } from "../../utility/forms_input_validations";
import { updateUserApi } from "../../api/users";
import { fetchAllDepartmentsApi  } from "../../api/departments";
import { fetchAllLevelsApi } from "../../api/levels";
import { useAuth } from "../auth/AuthContext";
import AdminLayout from "../../components/layout/AdminLayout";
import StudentLayout from "../../components/layout/StudentLayout";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { Button } from "../../components/ui/Button";
import profileImg from "../../assets/user_filled_colored_icon.png";
import closeIcon from "../../assets/close_icon.png";



function ProfilePageView(userData) {
  const [ user, setUser ] = useState(userData.userData);
  const [ editForm, setEditForm ] = useState(false);
  const [ errors, setErrors ] = useState({});
  const [ viewDetails, setViewDetails ] = useState(false);

  const [ departments, setDepartments ] = useState([]);
  const [ levels, setLevels ] = useState([]);

  console.log("user", user);
  
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
    if (editForm) {
      fetchAllDepartments();
      fetchAllLevels();
    }
  }, [editForm]);

  useEffect(() => {
    setUser(userData.userData);
  }, [userData]);


  const handleChange = (e) => {
    const { name, value } = e.target
    setUser((prev) => ({ ...prev, [name]: value }))
  }

  const handleCancel = () => {
    setEditForm(false);
    setErrors({});
    setDepartments([]);
    setLevels([]);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = {
        email: user?.email,
        department_id: user?.department_id,
        level_id: user?.level_id,
        is_admin: user?.is_admin
      }
      const validData = await updateUserValidationSchema.validate(
        formData, { abortEarly: false }
      );
      const updatedUserData = await updateUserApi(user.id, validData);
      setUser(updatedUserData ?? []);
      setEditForm(false);
      setDepartments([]);
      setLevels([]);

    } catch (error) {
      if (error.inner) {
        const newErrors = {};
        for (const err of error.inner)
          newErrors[err.path] = err.message;
        setErrors(newErrors);
        console.log("error.inner: ", newErrors);
      }
      console.error("Error submitting form: ", error);
    }  
  }

  return (
    <>
      
      {/* ------------------------- INFO SECTION ------------------------- */}
      <section
        className="h-18 py-5 px-10 mb-5 rounded-10 bg-primary-light flex justify-between profile-info-section"
      >
        <div
          className="w-15 h-15 mr-5 bg-white rounded-50 flex justify-center items-center profile-info-section"
        >
          <img
            src={ profileImg }
            alt="profile Image"
            className="w-75"
          />
        </div>

        <div
          className="mr-auto flex flex-col justify-center items-end"
        >
          <div className="flex items-center gap-1">
            <div className="h-2 w-2 bg-primary-dark rounded-50"></div>
            <p className="text-sm">{ user?.is_active ? "Active" : "Not active"}</p>
          </div>
          <p className="text-sm">Admin</p>
        </div>
        
        <div
          className="mr-5 flex flex-col gap-2 profile-btn"
        >
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
        </div>

        <Button
          type="button"
          variant="danger"
          size="md"
          className="self-start"
          children="Close Account"
        />
        
        {viewDetails &&
        <div
          className="h-screen w-screen bg-grey-dark-75 absolute top-0 left-0 flex justify-center items-center"
        >
          <div
            className="w-75 max-w-23 h-50 min-h-21 p-5 bg-grey-light rounded-10 flex flex-col justify-center"
          >
            <div
              onClick={ () => {setViewDetails(false);} }
              className="w-3 ml-auto cursor-pointer"
            >
              <img
                src={ closeIcon }
                alt="close"
                className="w-100"
              />
            </div>
            <p>Active: { user?.is_active ? "Yes" : "No" }</p>
            <p>Date Created: { new Date(user?.created_at).toLocaleDateString() }</p>
            <p>Last Updated: { new Date(user?.updated_at).toLocaleDateString() }</p>
            <br />
            <p>Email: { user?.email }</p>
            <p>Department: { user?.dept_name } - { user?.department }</p>
            <p>Level: { user?.level_name }</p>
            <br />
            <p>Number of files added: { user?.course_files_added }</p>
            <p>Warnings: { user?.warnings_count }</p>
            
          </div>
        </div>
        }
      </section>

      {/* ------------------------- FORM SECTION ------------------------- */}
      <section
        className=" p-5 rounded-10 bg-primary-light"
      >
        <form
          onSubmit={ handleSubmit }
          className="w-25 flex flex-col gap-5 profile-form"  
        >
            <div
              className="flex gap-5"
            >
              <label className="w-50 profile-form">Email: </label>
              {editForm ?
              <>
                <Input
                  type="email"
                  name="email"
                  value={ user?.email }
                  onChange={ handleChange }
                  disabled={ editForm ? false : true }
                  className="border-1"
                />
                {errors?.email && <p className="text-sm text-error">{ errors.email }</p>}
              </> :
              <p>{ user?.email }</p>}
            </div>

            <div
              className="flex gap-5"
            >
              <label className="w-50 profile-form">Department: </label>
              {editForm ?
              <Select
                id="department_id"
                name="department_id"
                value={ user?.department_id } 
                options={ departments }
                onChange={ handleChange }
                className=""
              /> :
              
              <p>{ user?.department }</p>}
            </div>

            <div
              className="flex gap-5"
            >
              <label className="w-50 profile-form">Level: </label>
              {editForm ?
              <Select
                id="level_id"
                name="level_id"
                value={ user?.level_id }
                options={ levels }
                onChange={ handleChange }
                className=""
              /> :
              <p>{ user?.level }</p>}
            </div>

            <div
              className="flex gap-5"
            >
              <label className="w-50 profile-form">Date Created:</label>
              <p>{ new Date(user?.created_at).toLocaleDateString() }</p>
            </div>

            <div
              className="h-6 flex gap-2"
            >
              {editForm &&
              <Button
                type="submit"
                variant="primary"
                size="md"
                children="Save"
              />}

              {editForm &&
              <Button
                type="button"
                variant="outline"
                size="md"
                className="text-error"
                onClick={ handleCancel }
                children="Cancel"
              />}
            </div>
        </form>
      </section>
    </>
  );
}


export default function ProfilePage() {
  const { user, loading } = useAuth();

  if (loading) {
    console.log("User in profile page loading: ", user);
    return(
      <p>Loading...</p>
    );
  }

  if (user?.is_admin) {
    console.log("User in profile page user?.is_admin: ", user);
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
