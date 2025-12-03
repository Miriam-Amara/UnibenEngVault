/* */

import * as yup from "yup";


export const courseValidationSchema = yup.object({
  course_code: yup.string()
    .required("Course code is required")
    .length(6, "Course code must be exactly 6 characters."),
  semester: yup.string()
    .required("Semester is required")
    .oneOf(["first", "second"], "Semester must be either first or second."),
  credit_load: yup.number()
    .required("Credit load is required")
    .moreThan(0, "Credit load should be more than 0")
    .lessThan(7, "Credit load should not exceed 6."),
  level_id: yup.string()
    .required("Level id is required")
    .length(36, "Level id must be exactly 36 characters."),
  title: yup.string()
    .required("Course title is required")
    .min(3, "Minimum of three characters.")
    .max(500, "Maximum of 500 characters."),
  outline: yup.string()
    .required("Course outline is required."),
  is_active: yup.string()
    .required("Active status is required.")
    .oneOf([true, false], "Active status must be either yes or no.")
})


export const departmentValidationSchema = yup.object({
  dept_name: yup.string()
    .required("Department name is required.")
    .matches(/.*\bengineering$/i, "Department name must end with engineering."),
  dept_code: yup.string()
    .required("Department code is required.")
    .length("Department code must be exactly 3 characters."),
})


export const fileValidationSchema = yup.object({
  course_id: yup.string()
    .required("Course id is required.")
    .length(36, "Course id must be exactly 36 characters."),
  file_type: yup.string()
    .required("File type is required.")
    .oneOf(
      ["lecture material", "note", "past question", "past questions"],
    "File type must be either: lecture material, note or past question(s)"
  ),
  session: yup.string()
    .transform((value, originalValue) => (originalValue === "" ? null : value))
    .matches(/^\d{4}\/\d{4}$/, "Session should match this pattern 2020/2021")
    .when("file_type", {
        is: (val) => ["past question", "past questions"].includes(val),
        then: (schema) =>
            schema.required("Session is required when file type is past question(s)."),
          otherwise: (schema) => schema.nullable()})
      .nullable(),
  status: yup.string()
    .transform((value, originalValue) => (originalValue === "" ? null : value))
    .oneOf(
      ["pending", "approved", "rejected"],
    "Status must be either: pending, rejected or approved.")
    .nullable(),
  rejection_reason: yup.string()
      .transform((value, originalValue) => (originalValue === "" ? null : value))
      .max(1024, "Maximum 1024 characters")
      .when("status", {
        is: "rejected",
        then: (schema) =>
            schema.required("Rejection reason is required when status is rejected."),
        otherwise: (schema) => schema.nullable()})
      .nullable()
})


export const levelValidationSchema = yup.object({
  level_name: yup.number()
    .required("Level is required.")
    .oneOf(
      [100, 200, 300, 400, 500],
      "Level must be either: 100, 200, 300, 400 or 500"
    )
})


export const reportValidationSchema = yup.object({
  report_type: yup.string()
    .required("Report type is required")
    .oneOf(
      ["file", "tutorial_link", "content", "other"],
      "Report type must be either: file, tutorial link, content or other."
    ),
  message: yup.string()
    .required("Message is required.")
    .min(5, "Minimum of 5 characters.")
    .max(2000, "Maximum of 2000 characters."),
  file_id: yup.string()
    .transform((value, originalValue) => (originalValue === "" ? null : value))
    .length(36, "File id must be exactly 36 characters.")
    .nullable(),
  tutorial_link_id: yup.string()
    .transform((value, originalValue) => (originalValue === "" ? null : value))
    .length(36, "Tutorial link id must be exactly 36 characters.")
    .nullable(),
})


export const loginValidationSchema = yup.object({
  email: yup.string()
    .email("Invalid email format.")
    .required("Email is required."),
  password: yup.string()
    .required("Password is required")
})


export const userValidationSchema = yup.object({
  email: yup.string()
    .email("Invalid email format.")
    .required("Email is required.")
    .max(100, "Maximum of 100 characters"),
  password: yup.string()
      .required("Password is required")
      .min(8, "Password must be at least 8 characters")
      .max(200, "Maximum of 200 characters")
      .matches(/[0-9]/, "Password must contain at least one number")
      .matches(/[A-Z]/, "Password must contain at least one uppercase")
      .matches(/[a-z]/, "Password must contain at least one lowercase"),
  is_admin: yup.string()
    .required("Is admin required.")
    .oneOf([true, false], "Is admin must be either: true or false."),
  department_id: yup.string()
    .required("Department id is required.")
    .length(36, "Department id must be exactly 36 characters."),
  level_id: yup.string()
    .required("Department id is required.")
    .length(36, "Department id must be exactly 36 characters."),
})
