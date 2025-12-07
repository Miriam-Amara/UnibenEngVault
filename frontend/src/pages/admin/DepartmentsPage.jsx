/**
 * 
 */


import { useEffect, useState } from "react";

import { departmentValidationSchema } from "../../utility/forms_input_validations";
import {
  addDepartmentApi,
  updateDepartmentApi,
  fetchAllDepartmentsApi,
  fetchDepartmentApi,
  deleteDepartmentApi
} from "../../api/departments";
import AdminLayout from "../../components/layout/AdminLayout";
import Table from "../../components/ui/Table";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { ModalOverlay, PopUp } from "../../components/ui/Modal";
import { ShowToast, ConfirmDialog } from "../../components/ui/Toast";
import closeIcon from "../../assets/close_icon.png";



function DepartmentPageView({ setShowModal }) {
  const [ departments, setDepartments ] = useState([]);
  const [ department, setDepartment ] = useState({});

  const [ formData, setFormData ] = useState({
    dept_name: "",
    dept_code: "",
  });
  const [ errors, setErrors ] = useState({});
  const [ showForm, setShowForm ] = useState(false);
  const [ formMode, setFormMode ] = useState("add");
  const [ viewDetails, setViewDetails ] = useState(false);
  const [ search, setSearch ] = useState("");

  const [ showConfirmDialog, setShowConfirmDialog ] = useState(false);
  const [ confirmDelete, setConfirmDelete ] = useState(false);

  const columns = [
    { label: "Department Name", key: "dept_name" },
    { label: "Department Code", key: "dept_code" }
  ]

  const fetchAllDepartments = async () => {
    try {
      
      const allDepartments = await fetchAllDepartmentsApi({ search });
      setDepartments(allDepartments ?? [])
    } catch (error) {
        ShowToast(
          "Error fetching departments",
          "error",
          "sm",
        );
        console.error("Error fetching departments: ", error);
    }
  };

  useEffect(() => {
    fetchAllDepartments();
  }, [search]);

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({...prev, [name]: value}));
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const validData = await departmentValidationSchema.validate(
        formData, { abortEarly:false });
      
      if (formMode == "add") {
        await addDepartmentApi(validData);
        ShowToast(
          `${validData.dept_name} added successfully`,
          "success"
        );
      } else {
          await updateDepartmentApi(department.id, validData);
      }
      
      setFormData({
        dept_name: "",
        dept_code: "",
      });
      setErrors({});
      fetchAllDepartments();

    } catch (error) {
        if (error.inner) {
          const newErrors = {};
          for (const err of error.inner)
            newErrors[err.path] = err.message;
          setErrors(newErrors);
        } else {
          ShowToast(
            `Failed to ${formMode} department`,
            "error",
            "md",
          );
          console.error("Failed to add department", error);
        }
    }
  }

  const handleAdd = () => {
    setFormMode("add");
    setShowForm(true);
    setShowModal(true);
  }

  const handleCancel = () => {
    setFormData({
      dept_name: "",
      dept_code: "",
    });
    setErrors({});
    setShowForm(false);
    setShowModal(false);
  }

  const handleView = async (row) => {
    setViewDetails(true);
    setShowModal(true);

    try {
      const departmentData = await fetchDepartmentApi(row.id);
      setDepartment(departmentData);
    } catch (error) {
        console.error("Error fetching department: ", error);
    }
  }

  const handleEdit = (row) => {
    setDepartment(row);
    setFormData(department);
    setFormMode("edit");
    setShowForm(true);
    setShowModal(true);
  }

  const handleDelete = async (row) => {
    setDepartment(row);
    setShowConfirmDialog(true);
    setShowModal(true);

    try {
      confirmDelete && await deleteDepartmentApi(department.id);
      setConfirmDelete(false);
    } catch (error) {
        ShowToast(
          `Failed to delete ${department.dept_name}`,
          "error",
        );
        console.error("Failed to delete department: ", error);
    }
  }


  return (
    <>
      {/* -------------------------- INTRO SECTION -------------------------- */}
      <section className="mb-5">
        <h4 className="text-primary-dark">Manage Departments</h4>
      </section>

      {/* -------------------------- CONTROL SECTION -------------------------- */}
      <section
        className="mb-10 flex "
      >
        <Button
          type="button"
          variant="primary"
          size="md"
          onClick={ handleAdd }
          children="Add Department"
          className="max-w-18"
        />

        <Input
          type="text"
          name="search_dept_name"
          value={ search }
          placeholder="Search departments..."
          onChange={ (e) => {setSearch(e.target.value)} }
          className="ml-auto mr-10 rounded-10 max-w-19"
        />
      </section>

      {/* -------------------------- DISPLAY SECTION -------------------------- */}
      <section>

        {/* ---------- FORM ---------- */}
        {showForm &&
        <ModalOverlay>
            <>
            <Button
              type="button"
              variant="danger"
              size="sm"
              onClick={ handleCancel }
              children="Cancel"
              className="ml-auto"
            />

            <form 
              onSubmit={ handleSubmit }
              className="max-w-85 flex flex-col gap-2"
            >
              <div className="items-center flex gap-5">
                <label>Department Name:</label>
                <div>
                  <Input
                    type="text"
                    name="dept_name"
                    value={ formData.dept_name }
                    placeholder="Enter department name"
                    onChange={ handleChange }
                    className=""
                  />
                  {errors.dept_name && <p className="text-sm text-error">{ errors.dept_name }</p>}
                </div>
              </div>

              <div className="items-center flex gap-5">
                <label>Department Code:</label>
                <div className="ml-auto"> 
                  <Input
                    type="text"
                    name="dept_code"
                    value={ formData.dept_code }
                    placeholder="Enter department code"
                    onChange={ handleChange }
                    className=""
                  />
                  {errors.dept_code && <p className="text-sm text-error">{ errors.dept_code }</p>}
                </div>
              </div>

              <Button
                type="submit"
                variant="primary"
                size="sm"
                children={ formMode === "add" ? "Add" : "Update" }
                className="mt-5 mr-auto"
              />
            </form>
          </>
        </ModalOverlay>}

        
        {/* ---------- VIEW DETAILS ---------- */}
        {viewDetails &&
        <PopUp
          children={
            <>
              <Button
              type="button"
              variant="icon"
              size="sm"
              onClick={ () => {setViewDetails(false); setShowModal(false);} }
              children={
                <img
                  src={ closeIcon }
                  alt="close"
                  className="w-3 ml-auto"
                />
              }
              className=""
            />
            <p>Date Created: { new Date(department.created_at).toLocaleDateString() }</p>
            <p>Last updated: { new Date(department.created_at).toLocaleDateString() } </p>
            <br />
            <p>Department Name: { department.dept_name }</p>
            <p>Department Code: { department.dept_code }</p>
            <p>No of Courses offered: { department.no_of_courses }</p>
            <p>No of Users: { department.no_of_users }</p>
          </>
          }
        />
        }


        {/* ---------- TABLE ---------- */}
        {departments.length !== 0 &&
          <Table
            columns={ columns }
            data={ departments }
            onClickView={ handleView }
            onClickEdit={ handleEdit }
            onClickDelete={ handleDelete }
          />
        }

        {/* ---------- TABLE ---------- */}
        {showConfirmDialog &&
          <ConfirmDialog
            message={ `Are you sure you want to delete ${department.dept_name}?`}
            onConfirm={ () => {setConfirmDelete(true);} }
            onCancel={ () => {setShowConfirmDialog(false);} }
          />
        }

      </section>
    </>
  );
}


export default function DepartmentPage() {
  const [ showModal, setShowModal ] = useState(false);
  return (
    <>
      <AdminLayout
        Page={ <DepartmentPageView setShowModal={ setShowModal } /> }
        showModal={ showModal }
      />
    </>
  );
}
