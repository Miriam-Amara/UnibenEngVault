/**
 * User Details
 */


import { PopUp } from "../../../components/ui/Modal";
import { Button } from "../../../components/ui/Button";
import closeIcon from "../../../assets/close_icon.png";


export default function UserDetails({ user, onClose }) {
  if (!user)
    return <p>Details not available</p>;

  return (
    <>
    <PopUp>
      <>
        <Button
          type="button"
          variant="icon"
          size="sm"
          onClick={ onClose }
          children={
            <img
              src={ closeIcon }
              alt="close"
              className="w-3 ml-auto"
            />
          }
        />

        <p>Date Created: { new Date(user.created_at).toLocaleDateString() }</p>
        <p>Last updated: { new Date(user.updated_at).toLocaleDateString() } </p>
        <br />
        <p>Email: { user?.email }</p>
        <p>Admin: { user?.is_admin ? "Yes" : "No" }</p>
        <p>Department: { user?.dept_name } - { user?.department }</p>
        <p>Level: { user?.level }</p>
        <p>Number of files added: { user?.course_files_added }</p>
        <p>Warnings: { user?.warnings_count }</p>
      </>
    </PopUp>
  </>
  );
}