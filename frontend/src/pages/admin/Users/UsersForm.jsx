/**
 * User Form
 */

import { useState, useEffect } from "react";

import {
  userValidationSchema,
  updateUserValidationSchema
} from "../../../utility/forms_input_validations";
import {
  registerUserApi,
  updateUserApi
} from "../../../api/users";
import { ModalOverlay } from "../../../components/ui/Modal";
import { ShowToast } from "../../../components/ui/Toast";
import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/ui/Select";
import { Button, ButtonIcon } from "../../../components/ui/Button";
import hidePasswordIcon from "../../../assets/password_hide_icon.png";
import showPasswordIcon from "../../../assets/password_show_icon.png";


export const ShowPasswordImg = () => (
  <img
    src={ showPasswordIcon }
    alt="show password"
    className="w-3 bg-white"
  />
);

export const HidePasswordImg = () => (
  <img
    src={ hidePasswordIcon }
    alt="hide password"
    className="w-3 bg-white"
  />
);

const emptyForm = {
  email: "",
  department_id: "",
  level_id: "",
  password: "",
  confirm_password: "",
  is_admin: false,
};


export default function UserForm({
  mode = "add",
  user,
  departments,
  levels,
  onSuccess,
  onCancel
}) {

  const [ formData, setFormData ] = useState(mode === "add" ? emptyForm : user);
  const [ errors, setErrors ] = useState({});
  const [ showPassword, setShowPassword ] = useState(false);
  const [ showConfirmPassword, setShowConfirmPassword ] = useState(false);

  useEffect(() => {
    setFormData(mode === "add" ? emptyForm : user);
  }, [user, mode]);

  const handleChange = (e) => {
    const { name, value } = e.target

    if (name === "is_admin") {
      setFormData(prev => ({ ...prev, is_admin: value === "true" }));
      return;
    }

    setFormData((prev) => ({...prev, [name]: value}));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const schema = mode === "add" ? userValidationSchema : updateUserValidationSchema;
      const validData = schema.validateSync(formData, {abortEarly: false});

      if (mode == "add") {
        await registerUserApi(validData);
      } else {
        await updateUserApi(user.id, validData);
      }

      ShowToast(
        `${validData.email} ${mode === "add" ? "added" : "updated"} successfully`,
        "success"
      );
      
      if (mode === "add")
        setFormData(emptyForm);
      setErrors({});
      onSuccess();

    } catch (error) {
        if (error.inner) {
          const newErrors = {};
          error.inner.forEach((err) => (newErrors[err.path] = err.message));
          setErrors(newErrors);
        } else {
          ShowToast(`Failed to ${mode} user`, "error");
          console.error(`Failed to ${mode} user`, error);
        }
    }
  };
  

  return(
    <ModalOverlay>
      <Button
        type="button"
        variant="danger"
        size="sm"
        onClick={() => {onCancel(); setFormData(emptyForm); setErrors({});}}
        children="Cancel"
        className="ml-auto"
      />

      <form 
        onSubmit={ handleSubmit }
        className="max-w-95 flex flex-col gap-2"
      >

        {/* --------------- EMAIL --------------- */}
        <div className="items-center flex gap-5">
          <label>Email Address</label>
          <div className="ml-auto">
            <Input
              type="email"
              name="email"
              value={formData.email}
              placeholder="Enter your email address"
              onChange={handleChange}
            />
            {errors.email &&
            <p className="text-sm text-error">
              { errors.email }
            </p>}
          </div>
        </div>

        {/* --------------- PASSWORD (Only add mode) --------------- */}
        {mode === "add" &&
        <>
          <div className="relative items-center flex gap-5">
            <label>Password</label>
            <div className="flex flex-col">
              <div className="ml-auto flex flex-row-reverse items-center">
                <Input
                  type={ showPassword ? "text" : "password" }
                  name="password"
                  value={ formData.password }
                  placeholder="Enter your password"
                  onChange={ handleChange }
                />
                <ButtonIcon
                  className="absolute mr-1"
                  onClick={ () => setShowPassword(!showPassword) }
                  children={ showPassword ? <ShowPasswordImg /> : <HidePasswordImg />}
                />
              </div>
              {errors.password && <p className="text-sm text-error"> { errors.password } </p>}
            </div>
          </div>

          <div className="relative items-center flex gap-5">
            <label>Confirm Password</label>
            <div className="flex flex-col">
              <div className="ml-auto flex flex-row-reverse items-center">
                <Input
                  type={ showConfirmPassword ? "text" : "password" }
                  name="confirm_password"
                  value={ formData.confirm_password }
                  placeholder="Confirm your password"
                  onChange={ handleChange }
                />
                <ButtonIcon
                  className="absolute mr-1"
                  onClick={ () => setShowConfirmPassword(!showConfirmPassword) }
                  children={ showConfirmPassword ?
                  <ShowPasswordImg /> :
                  <HidePasswordImg />
                  }
                />
              </div>
              {errors.confirm_password &&
              <p className="text-sm text-error"> { errors.confirm_password } </p>}
            </div>
          </div>
        </>}

        {/* --------------- DEPARTMENT --------------- */}
        <div className="items-center flex gap-5">
          <label>Department</label>
          <div className="ml-auto">
            <Select
              name="department_id"
              value={ formData.department_id }
              options={ departments }
              onChange={handleChange}
              id=""
            />
            {errors.department_id &&
            <p className="text-sm text-error">
              { errors.department_id }
            </p>}
          </div>
        </div>

        {/* --------------- LEVEL --------------- */}
        <div className="items-center flex gap-5">
          <label>Level</label>
          <div className="ml-auto">
            <Select
              name="level_id"
              value={ formData.level_id }
              options={ levels }
              onChange={handleChange}
            />
            {errors.level_id &&
              <p className="text-sm text-error">
                { errors.level_id }
              </p>}
          </div>
        </div>

        {/* --------------- ADMIN --------------- */}
        <div className="items-center flex gap-5">
          <label>Is Admin?</label>
          <div className="ml-auto">
            <Select
              name="is_admin"
              value={ formData.is_admin }
              options={[
                {value: "true", label: "Yes"},
                {value: "false", label: "No"}
              ]}
              onChange={handleChange}
            />
            {errors.is_admin &&
            <p className="text-sm text-error">
              { errors.is_admin }
            </p>}
          </div>
        </div>

        {/* --------------- SUBMIT BUTTON --------------- */}
        <Button
          type="submit"
          variant="primary"
          size="sm"
          children={ mode === "add" ? "Add" : "Update" }
          className="mt-5 mr-auto"
        />
      </form>
    </ModalOverlay>
  );
}
