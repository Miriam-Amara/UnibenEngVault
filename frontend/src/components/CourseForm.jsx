import { useState, useEffect } from "react";
import * as Yup from "yup";

import { addCourseAPI, updateCourseAPI } from "../pages/api/courses";
import { showToast } from "../pages/utils/toast";
import { fetchLevelsAPI } from "../pages/api/levels";

export default function CourseForm({ onClose, onSaved, editData }) {
  const [levels, setLevels] = useState([]);
  const [errors, setErrors] = useState({});

  const [form, setForm] = useState({
    course_code: "",
    semester: "",
    credit_load: 0,
    level_id: "",
    title: "",
    outline: "",
    is_active: true,
  });

  const [saving, setSaving] = useState(false);

  // Yup validation schema
  const schema = Yup.object({
    course_code: Yup.string()
      .required("Course code is required")
      .length(6, "Course code must be exactly 6 characters")
      .matches(/^[a-z]{3}\d{3}$/, "Course code must be 3 letters followed by 3 digits (e.g., IDE562)"),
    semester: Yup.string().required("Semester is required"),
    credit_load: Yup.number()
      .required("Credit load is required")
      .min(1, "Credit load must not be less than 1")
      .max(10, "Credit load must not exceed 10"),
    level_id: Yup.string().required("Level is required"),
    title: Yup.string()
      .required("Course title is required")
      .min(5, "Minimum of 5 characters")
      .max(500, "Maximum of 500 characters"),
    outline: Yup.string()
      .required("Course outline is required")
      .min(5, "Minimum of 5 characters")
      .max(2000, "Maximum of 2000 characters"),
    is_active: Yup.boolean(),
  });

  useEffect(() => {
    // Load levels async
    const loadLevels = async () => {
      try {
        const data = await fetchLevelsAPI();
        setLevels(data);
      } catch (err) {
        console.log(err)
        showToast("Failed to load levels", "error");
      }
    };

    loadLevels();
  }, []);

  useEffect(() => {
    if (editData) {
      setForm({
        course_code: editData.course_code || "",
        semester: editData.semester || "",
        credit_load: editData.credit_load || 0,
        level_id: editData.level_id || "",
        title: editData.title || "",
        outline: editData.outline || "",
        is_active: editData.is_active ?? true,
      });
    }
  }, [editData]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;

    // Handle boolean select conversion
    if (name === "is_active") {
      setForm({
        ...form,
        [name]: value === "true",
      });
      return;
    }

    // Handle number inputs properly
    if (type === "number") {
      setForm({
        ...form,
        [name]: value === "" ? "" : Number(value),
      });
      return;
    }

    setForm({
      ...form,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await schema.validate(form, { abortEarly: false });
      setSaving(true);

      if (editData) {
        await updateCourseAPI(editData.id, form);
        showToast("Course updated successfully!", "success");
      } else {
        await addCourseAPI(form);
        showToast("Course added successfully!", "success");
      }

      onSaved();
      onClose();
    } catch (err) {
      if (err.inner) {
        const newErrors = {};
        err.inner.forEach((error) => {
          newErrors[error.path] = error.message;
        });
        setErrors(newErrors);
      } else {
        showToast("Error saving course", "error");
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <h2>{editData ? "Update Course" : "Add New Course"}</h2>
      <form onSubmit={handleSubmit} noValidate>
        <div>
          <label>Course Code</label>
          <input
            type="text"
            name="course_code"
            value={form.course_code}
            onChange={handleChange}
            placeholder="Enter course code"
          />
          {errors.course_code && <p className="error">{errors.course_code}</p>}
        </div>

        <div>
          <label>Semester</label>
          <select name="semester" value={form.semester} onChange={handleChange}>
            <option value="">Select Semester</option>
            <option value="First">First</option>
            <option value="Second">Second</option>
          </select>
          {errors.semester && <p className="error">{errors.semester}</p>}
        </div>

        <div>
          <label>Credit Load</label>
          <input
            type="number"
            name="credit_load"
            value={form.credit_load}
            onChange={handleChange}
            placeholder="Credit Load"
            min={1}
            max={10}
          />
          {errors.credit_load && <p className="error">{errors.credit_load}</p>}
        </div>

        <div>
          <label>Level</label>
          <select name="level_id" value={form.level_id} onChange={handleChange}>
          <option value="">Select Level</option>
            {levels.map((lvl) => (
              <option key={lvl.id} value={lvl.id}>
                {lvl.level || lvl.name || `Level ${lvl.id}`}
              </option>
            ))}
          </select>
          {errors.level_id && <p className="error">{errors.level_id}</p>}
        </div>

        <div>
          <label>Title</label>
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="Enter course title"
          />
          {errors.title && <p className="error">{errors.title}</p>}
        </div>

        <div>
          <label>Course Outline</label>
          <textarea
            name="outline"
            value={form.outline}
            onChange={handleChange}
            placeholder="Enter course outline"
            rows={4}
          />
          {errors.outline && <p className="error">{errors.outline}</p>}
        </div>

        <div>
          <label>Is course still being offered?</label>
            <select name="is_active" value={String(form.is_active)} onChange={handleChange}>
            <option value="">Select</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>

        <div>
          <button type="button" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" disabled={saving}>
            {saving ? "Saving..." : "Save"}
          </button>
        </div>
      </form>
    </div>
  );
}
