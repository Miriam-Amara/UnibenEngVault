import { useState, useEffect, useRef } from "react";
import * as Yup from "yup";
import { useFormik, FieldArray, FormikProvider } from "formik";

import { uploadFileAPI } from "../pages/api/files";
import { fetchCoursesAPI } from "../pages/api/courses";
import { showToast } from "../pages/utils/toast";



const FILE_TYPES = ["past question", "past questions", "lecture material", "note"];
const STATUS_OPTIONS = ["approved", "rejected", "pending"];

export default function UploadMultipleFilesForm({ onClose, onUploaded }) {
  const [courses, setCourses] = useState([]);
  const [courseSearch, setCourseSearch] = useState("");
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [uploading, setUploading] = useState(false);
  const courseInputRef = useRef();

  // Load courses on mount
  useEffect(() => {
    async function loadCourses() {
      const data = await fetchCoursesAPI({ pageSize: 50, pageNum: 1 });
      setCourses(data);
      setFilteredCourses(data);
    }
    loadCourses();
  }, []);

  // Filter courses as user types course code
  useEffect(() => {
    const filtered = courses.filter(c =>
      c.course_code.toLowerCase().includes(courseSearch.toLowerCase())
    );
    setFilteredCourses(filtered);
  }, [courseSearch, courses]);


  // Yup validation schema for the rows
  const fileRowSchema = Yup.object({
    file_type: Yup.string()
      .oneOf(FILE_TYPES)
      .required("File type is required"),
    file: Yup.mixed().required("File is required"),
    session: Yup.string().test(
      "session-required-for-past-question",
      "Session is required for past questions",
      function(value) {
        const { file_type } = this.parent;
        if (["past question", "past questions"].includes(file_type)) {
          return !!value;
        }
        return true;
      }
    ),
  });

  // Main validation schema
  const validationSchema = Yup.object({
    course_id: Yup.string().required("Course selection is required"),
    files: Yup.array().of(fileRowSchema).min(1, "At least one file must be uploaded"),
  });

  // Formik setup
  const formik = useFormik({
    initialValues: {
      course_id: "",
      files: [
        {
          file_type: "",
          session: "",
          file: null,
        },
      ],
    },
    validationSchema,
    onSubmit: async (values) => {
      console.log("onSubmit triggered", values);
      
      if (!selectedCourse || selectedCourse.id !== values.course_id) {
        showToast("Please select a valid course from the dropdown", "error");
        return;
      }

      setUploading(true);
      try {
        for (const row of values.files) {
          const formData = new FormData();
          formData.append("file", row.file);
          const metadata = {
            file_type: row.file_type,
          };
          if (row.session) {
            metadata.session = row.session;
          }
          formData.append("metadata", JSON.stringify(metadata));
          
          // Upload each file separately with the selected course id
          await uploadFileAPI(values.course_id, formData);
        }

        onUploaded?.();
        onClose?.();
      } catch (error) {
        console.error("Upload failed:", error);
        showToast("Failed to upload files. Please try again.", "error");
      } finally {
        setUploading(false);
      }

      onUploaded?.();
      onClose?.();
      setUploading(false);
    },
  });

  // Handle course selection from autocomplete dropdown
  function handleCourseSelect(course) {
    setSelectedCourse(course);
    formik.setFieldValue("course_id", course.id);
    setCourseSearch(course.course_code);
    setFilteredCourses([]); // Hide suggestions after select
    // Focus out of input optionally
    courseInputRef.current.blur();
  }

  // Handle typing in course input
  function handleCourseSearchChange(e) {
    setCourseSearch(e.target.value);
    setSelectedCourse(null);
    formik.setFieldValue("course_id", "");
  }

  return (
    <div>
      <button
        type="button"
        onClick={onClose}
        className="modal-close"
        disabled={uploading}
      >
        Close
      </button>
      <h4>Upload Multiple Files</h4>

      {/* Course autocomplete */}
      <div className="main-form">
        <div className="main-form-input">
          <label>Course (type to search)</label>
          <div>
            <input
              id="course_search"
              type="text"
              value={courseSearch}
              onChange={handleCourseSearchChange}
              ref={courseInputRef}
              autoComplete="off"
              placeholder="Start typing course code..."
            />
            {formik.touched.course_id && formik.errors.course_id && (
              <p className="error">{formik.errors.course_id}</p>
            )}
          </div>
        </div>

        {/* Suggestions dropdown */}
        <div>
          {filteredCourses.length > 0 && !selectedCourse && (
            <ul>
              {filteredCourses.slice(0, 10).map((c) => (
                <li
                  key={c.id}
                  onClick={() => handleCourseSelect(c)}
                >
                  {c.course_code} - {c.semester}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <FormikProvider value={formik}>
        <form onSubmit={formik.handleSubmit}>

          <FieldArray
            name="files"
            render={arrayHelpers => (
              <>
                <table>
                  <thead>
                    <tr>
                      <th>File Type</th>
                      <th>Session</th>
                      <th>Select File</th>
                      <th>Remove</th>
                    </tr>
                  </thead>
                  <tbody>
                    {formik.values.files.map((fileRow, index) => {
                      const fileTypeError = formik.errors.files?.[index]?.file_type;
                      const fileError = formik.errors.files?.[index]?.file;
                      const sessionError = formik.errors.files?.[index]?.session;
                      const touchedFileRow = formik.touched.files?.[index] || {};

                      return (
                        <tr key={index} className="border-b">
                          {/* File Type */}
                          <td className="border px-2 py-1">
                            <select
                              name={`files[${index}].file_type`}
                              value={fileRow.file_type}
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              className="w-full border rounded px-2 py-1"
                            >
                              <option value="">Select file type</option>
                              {FILE_TYPES.map((type) => (
                                <option key={type} value={type}>{type}</option>
                              ))}
                            </select>
                            {touchedFileRow.file_type && fileTypeError && (
                              <p className="error">{fileTypeError}</p>
                            )}
                          </td>

                          {/* Session */}
                          <td className="border px-2 py-1">
                            <input
                              type="text"
                              name={`files[${index}].session`}
                              value={fileRow.session}
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              placeholder="e.g. 2020/2021"
                              disabled={
                                !["past question", "past questions"].includes(fileRow.file_type)
                              }
                              className={`w-full border rounded px-2 py-1 ${
                                !["past question", "past questions"].includes(fileRow.file_type)
                                  ? "bg-gray-100"
                                  : ""
                              }`}
                            />
                            {touchedFileRow.session && sessionError && (
                              <p className="error">{sessionError}</p>
                            )}
                          </td>

                          {/* File input */}
                          <td>
                            <input
                              type="file"
                              name={`files[${index}].file`}
                              onChange={(e) => {
                                formik.setFieldValue(`files[${index}].file`, e.currentTarget.files[0]);
                              }}
                            />
                            {touchedFileRow.file && fileError && (
                              <p className="error">{fileError}</p>
                            )}
                          </td>

                          {/* Remove row */}
                          <td>
                            <button
                              type="button"
                              disabled={formik.values.files.length === 1}
                              onClick={() => arrayHelpers.remove(index)}
                            >
                              &times;
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>

                {/* Buttons */}
                <div className="upload-file-container">

                  {/* Add new file row */}
                  <button
                    type="button"
                    onClick={() =>
                    arrayHelpers.push({
                      file_type: "",
                      session: "",
                      file: null})}
                    className="btn-lg"
                  >
                    Add Another File
                  </button>
                  
                  <button
                    type="submit"
                    disabled={uploading}
                    className={`${
                      uploading ? "btn-grey" : "btn-lg"
                    }`}
                  >
                    {uploading ? "Uploading..." : "Upload All"}
                  </button>
                </div>
              </>
            )}
          />
        </form>
      </FormikProvider>
    </div>
  );
}
