/**
 * 
 * @param {*} param0 
 * @returns 
 */


import { Button } from "./Button";
import viewIcon from "../../assets/view_icon.png";
import editIcon from "../../assets/edit_icon.png";
import deleteIcon from "../../assets/delete_icon.png";


const ViewDetails = ({ onClickView }) => {
  return (
    <Button
      type="button"
      variant="icon"
      size="sm"
      onClick={ onClickView }
      className=""
      children={
        <img
          src={ viewIcon }
          alt="view"
          className="w-4"
        />
      }
    />
  );
}

const Edit = ({ onClickEdit }) => {
  return (
    <Button
      type="button"
      variant="icon"
      size="sm"
      onClick={ onClickEdit }
      className=""
      children={
        <img
          src={ editIcon }
          alt="edit"
          className="w-3"
        />
      }
    />
  );
}

const Delete = ({ onClickDelete }) => {
  return (
    <Button
      type="button"
      variant="icon"
      size="sm"
      onClick={ onClickDelete }
      className=""
      children={
        <img
          src={ deleteIcon }
          alt="delete"
          className="w-3"
        />
      }
    />
  );
}




export default function Table({
  columns = [],
  data = [],
  onClickView,
  onClickEdit,
  onClickDelete

}) {

  return (
    <table
      className="w-100 border-collapse"
    >
      <thead>
        <tr>
          {columns.map((col) => (
            <th
              key={col.key}
              className="text-left p-2 border bg-primary-light"
            >
              {col.label}
            </th>
          ))}
          <th
            className="text-left p-2 border bg-primary-light"
          >
            Actions
          </th>
        </tr>
      </thead>

      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {columns.map((col) => (
              <td
                key={col.key}
                className="p-2 border"
              >
                {row[col.key]}
              </td>
            ))}
            <td className=" p-2 border flex gap-3 items-center">
              <ViewDetails onClickView={ () => {onClickView(row);} }/>
              <Edit onClickEdit={ () => {onClickEdit(row)} }/>
              <Delete onClickDelete={ () => {onClickDelete(row)} }/>
            </td>
          </tr>
        ))}

        {data.length === 0 && (
          <tr>
            <td style={{ padding: "10px", textAlign: "center" }} colSpan={columns.length}>
              No data found
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
}
