/**
 * User Table
 */


import Table from "../../../components/ui/Table";



export default function UserTable({
  users=[],
  onView,
  onEdit,
  onDelete
}) {

  const columns = [
      { label: "Email", key: "email" },
      { label: "Department", key: "department" },
      { label: "Level", key: "level" }
    ];
  
  return (
    <Table
      columns={ columns }
      data={ users }
      onClickView={ onView }
      onClickEdit={ onEdit }
      onClickDelete={ onDelete }
    />

  );
}