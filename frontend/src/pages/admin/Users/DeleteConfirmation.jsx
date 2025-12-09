/**
 * Delete User confirmation
 * 
 * Props:
 * - show: Boolean – whether modal is visible
 * - onClose: Function – close modal
 * - onDeleted: Function – refresh parent after deletion
 * - user: { id, name, email, department, level, ... }
 */


import { useEffect } from "react";

import { deleteUserApi } from "../../../api/users";
import { ConfirmDialog } from "../../../components/ui/Toast";
import { ShowToast } from "../../../components/ui/Toast";




export default function DeleteUserModal({
  user,
  confirmDelete,
  message,
  onConfirm,
  onCancel,
  onSuccess,

}) {

  useEffect(() => {
    if (confirmDelete) {
      confirmUserDelete();
    }
  }, [confirmDelete]);

  const confirmUserDelete = async () => {
    try {
      await deleteUserApi(user.id);
      onSuccess();
      
    } catch {
      ShowToast(`Failed to delete ${user.email}`, "error");
    }
  };

  return (
    <ConfirmDialog
      message={ message}
      onConfirm={ onConfirm }
      onCancel={ onCancel }
    />
  );
}
