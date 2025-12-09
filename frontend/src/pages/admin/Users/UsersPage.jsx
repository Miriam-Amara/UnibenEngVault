/**
 * 
 */


import { useState } from "react";

import { fetchUserApi } from "../../../api/users";
import { useUsers } from "../../../hook/useUsers";
import { useSelectLevels } from "../../../hook/useLevels";
import { useSelectDepartments } from "../../../hook/useDepartments";
import UserForm from "./UsersForm";
import UserTable from "./UsersTable";
import UserDetails from "./UsersDetails";
import DeleteUserModal from "./DeleteConfirmation";
import Filters from "./Filters";
import AdminLayout from "../../../components/layout/AdminLayout";
import { Button } from "../../../components/ui/Button";



function UsersPageView({ setShowModal }) {
  const departments = useSelectDepartments();
  const levels = useSelectLevels();
  const {
    users,
    search, setSearch,
    date, setDate,
    // pageNum, setPageNum,
    pageSize, setPageSize,
    departmentId, setDepartmentId,
    levelId, setLevelId,
    clearFilters, fetchAllUsers
  } = useUsers();

  const [ user, setUser ] = useState({});
  const [ showForm, setShowForm ] = useState(false);
  const [ mode, setMode ] = useState("add");
  const [ viewDetails, setViewDetails ] = useState(false);

  const [ showConfirmDialog, setShowConfirmDialog ] = useState(false);
  const [ confirmDelete, setConfirmDelete ] = useState(false);

  const fetchUser = async (row) => {
    try {
      const data = await fetchUserApi(row.id);
      setUser(data);
    } catch {
        setUser({});
    }
  }
 
  return (
    <>
      {/* -------------------------- INTRO SECTION -------------------------- */}
      <section className="mb-5">
        <h4 className="text-primary-dark">Manage Users</h4>
      </section>


      {/* -------------------------- CONTROL SECTION -------------------------- */}
      <section className="mb-10 flex flex-col gap-5">

          {/* ---------------- ADD USER ---------------- */}
          <Button
            type="button"
            variant="primary"
            size="md"
            onClick={() => {setMode("add"); setShowForm(true); setShowModal(true);}}
            children="Add User"
            className="max-w-16"
          />

          {/* ---------------- Filters ---------------- */}
          <Filters
            pageSize={ pageSize }
            setPageSize={ setPageSize }
            date={ date }
            setDate={ setDate }
            search={ search}
            setSearch={ setSearch}
            departmentId={ departmentId }
            setDepartmentId={ setDepartmentId }
            departments={ departments }
            levelId={ levelId }
            setLevelId={ setLevelId }
            levels={ levels }
            clearFilters={ clearFilters }
          />
      </section>



      {/* -------------------------- DISPLAY SECTION -------------------------- */}
      <section>

        {/* ---------- FORM ---------- */}
        {showForm &&
        <UserForm
          mode={ mode }
          user={ user }
          departments={ departments }
          levels={ levels }
          onSuccess={() => {fetchAllUsers(); setShowForm(false); setShowModal(false);}}
          onCancel={() => {setShowForm(false); setShowModal(false);}}
        />}

        
        {/* ---------- VIEW DETAILS ---------- */}
        {viewDetails &&
        <UserDetails
          user={ user }
          onClose={()=>{setViewDetails(false); setShowModal(false);}}
        />}


        {/* ---------- TABLE ---------- */}
        <UserTable
          users={ users }
          onView={(row) => {
            fetchUser(row); setViewDetails(true); setShowModal(true);}
          }
          onEdit={(row) => {
            fetchUser(row); setMode("edit"); setShowForm(true); setShowModal(true);}
          }
          onDelete={(row) => {
            fetchUser(row); setShowConfirmDialog(true); setShowModal(true);}
          }
        />

        {/* ---------- CONFIRM DELETE DIALOG ---------- */}
        {showConfirmDialog &&
        <DeleteUserModal
          user={ user }
          confirmDelete={ confirmDelete }
          message={`Are you sure you want to delete ${user.email}?`}
          onConfirm={() => {setConfirmDelete(true);}}
          onCancel={() => {setShowConfirmDialog(false); setConfirmDelete(false); setShowModal(false);}}
          onSuccess={() => {
            fetchAllUsers();
            setConfirmDelete(false);
            setShowConfirmDialog(false);
            setShowModal(false);}}
        />}
      </section>
    </>
  );
}


export default function UserPage() {
  const [ showModal, setShowModal ] = useState(false);
  return (
    <>
      <AdminLayout
        Page={ <UsersPageView setShowModal={ setShowModal } /> }
        showModal={ showModal }
      />
    </>
  );
}
