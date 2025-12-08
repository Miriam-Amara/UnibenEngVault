/**
 * 
 */


import { useEffect, useState } from "react";

import { levelValidationSchema } from "../../utility/forms_input_validations";
import {
  addLevelApi,
  fetchAllLevelsApi,
  fetchLevelApi,
  deleteLevelApi,
} from "../../api/levels";
import AdminLayout from "../../components/layout/AdminLayout";
import Table from "../../components/ui/Table";
import { Button } from "../../components/ui/Button";
import { Select } from "../../components/ui/Select";
import { Input } from "../../components/ui/Input";
import { ModalOverlay, PopUp } from "../../components/ui/Modal";
import { ShowToast, ConfirmDialog } from "../../components/ui/Toast";
import closeIcon from "../../assets/close_icon.png";



function LevelPageView({ setShowModal }) {
  const [ levels, setLevels ] = useState([]);
  const [ level, setLevel ] = useState({});

  const [ formData, setFormData ] = useState({level_name: ""});
  const [ errors, setErrors ] = useState({});
  const [ showForm, setShowForm ] = useState(false);
  const [ viewDetails, setViewDetails ] = useState(false);

  const [ showConfirmDialog, setShowConfirmDialog ] = useState(false);
  const [ confirmDelete, setConfirmDelete ] = useState(false);

  const columns = [{ label: "Level", key: "level_name" }]

  const fetchAllLevels = async () => {
    try {
      const allLevels = await fetchAllLevelsApi({ });
      setLevels(allLevels ?? [])
    } catch (error) {
        ShowToast(
          "Error fetching levels",
          "error",
          "sm",
        );
        console.error("Error fetching levels: ", error);
    }
  };

  useEffect(() => {fetchAllLevels();}, []);

  useEffect(() => {
    if (confirmDelete) {
      confirmLevelDelete();
    }
  }, [confirmDelete]);

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({...prev, [name]: Number(value)}));
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const validData = await levelValidationSchema.validate(
        formData, { abortEarly:false });
      
      await addLevelApi(validData);

      ShowToast(
        `${validData.level_name} level added successfully`,
        "success"
      );
      
      setFormData({level_name: ""});
      setErrors({});
      fetchAllLevels();

    } catch (error) {
        if (error.inner) {
          const newErrors = {};
          for (const err of error.inner)
            newErrors[err.path] = err.message;
          setErrors(newErrors);
        } else {
          ShowToast(
            `Failed to add level`,
            "error",
            "md",
          );
          console.error("Failed to add level", error);
        }
    }
  }

  const handleAdd = () => {
    setShowForm(true);
    setShowModal(true);
  }

  const handleCancel = () => {
    setFormData({level_name: ""});
    setErrors({});
    setShowForm(false);
    setShowModal(false);
  }

  const handleView = async (row) => {
    setViewDetails(true);
    setShowModal(true);

    try {
      const levelData = await fetchLevelApi(row.id);
      setLevel(levelData);
    } catch (error) {
        console.error("Error fetching level: ", error);
    }
  }

  const handleDelete = (row) => {
    setLevel(row);
    setShowConfirmDialog(true);
    setShowModal(true);
  };

  const confirmLevelDelete = async () => {
    try {
      await deleteLevelApi(level.id);
      await fetchAllLevels();
      setShowConfirmDialog(false);
      setShowModal(false);
      setConfirmDelete(false);
    } catch (error) {
      ShowToast(
        `Failed to delete ${level.level_name} level`,
        "error"
      );
      console.error("Failed to delete level: ", error);
    }
  };

  return (
    <>
      {/* -------------------------- INTRO SECTION -------------------------- */}
      <section className="mb-5">
        <h4 className="text-primary-dark">Manage Levels</h4>
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
          children="Add Level"
          className="max-w-18"
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
                <label>Level:</label>
                <div>
                  <Select
                    name="level_name"
                    value={ formData.level_name }
                    options={[
                      { value: 100, label: 100 },
                      { value: 200, label: 200 },
                      { value: 300, label: 300 },
                      { value: 400, label: 400 },
                      { value: 500, label: 500 },
                    ]}
                    onChange={ handleChange }
                    className=""
                  />
                  {errors.level_name && <p className="text-sm text-error">{ errors.level_name }</p>}
                </div>
              </div>

              <Button
                type="submit"
                variant="primary"
                size="sm"
                children="Add"
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
            <p>Date Created: { new Date(level.created_at).toLocaleDateString() }</p>
            <p>Last updated: { new Date(level.created_at).toLocaleDateString() } </p>
            <br />
            <p>Level: { level.level_name }</p>
            <p>Number of course in level: { level.no_of_courses_in_level }</p>
            <p>Number of registered users in Level: { level.no_of_users_in_level }</p>
          </>
          }
        />
        }


        {/* ---------- TABLE ---------- */}
        <Table
          columns={ columns }
          data={ levels }
          onClickView={ handleView }
          onClickDelete={ handleDelete }
        />

        {/* ---------- TABLE ---------- */}
        {showConfirmDialog &&
          <ConfirmDialog
            message={ `Are you sure you want to delete ${level.level_name} level?`}
            onConfirm={ () => {setConfirmDelete(true);} }
            onCancel={ () => {setShowConfirmDialog(false); setConfirmDelete(false);} }
          />
        }

      </section>
    </>
  );
}


export default function LevelPage() {
  const [ showModal, setShowModal ] = useState(false);
  return (
    <>
      <AdminLayout
        Page={ <LevelPageView setShowModal={ setShowModal } /> }
        showModal={ showModal }
      />
    </>
  );
}
