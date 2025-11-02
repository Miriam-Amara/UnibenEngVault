import { useState, useEffect } from "react";
import { addLevelAPI, deleteLevelAPI, fetchLevelsAPI } from "../api/levels";
import Layout from "../../components/Layout";
import * as Yup from "yup";

// Custom hook to fetch levels
function useLevels({ pageSize = 8, pageNum = 1 }) {
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchLevels = async () => {
    setLoading(true);
    try {
      const data = await fetchLevelsAPI(pageSize, pageNum);
      setLevels(data);
    } catch (error) {
      console.error("Error fetching levels:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLevels();
  }, [pageSize, pageNum]);

  return { levels, fetchLevels, loading };
}

// Level form (add only)
function LevelForm({ onSuccess }) {
  const [formData, setFormData] = useState({ name: "" });
  const [errors, setErrors] = useState({});

  const validationSchema = Yup.object({
    name: Yup.number()
      .required("Level name is required.")
      .min(100, "Level should not be less that 100")
      .max(600, "Level should not exceed 600")
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: Number(value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await validationSchema.validate(formData, { abortEarly: false });
      await addLevelAPI(formData);
      alert(`${formData.name} added successfully!`);
      setFormData({ name: "" });
      if (onSuccess) onSuccess();
    } catch (error) {
      if (error.inner) {
        const newErrors = {};
        error.inner.forEach((err) => (newErrors[err.path] = err.message));
        setErrors(newErrors);
      } else if (error.response) {
        alert(error.response.data?.message || "An unexpected error occurred.");
      } else {
        console.error(error);
        alert("Something went wrong.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <select name="name" value={formData.name} onChange={handleChange}>
        <option value="">Select Level</option>
          {[100, 200, 300, 400, 500].map((lvl) => (
            <option key={lvl} value={lvl}>
              {lvl}
            </option>
          ))}
        </select>
        {errors.name && <p className="error">{errors.name}</p>}
      </div>

      <button type="submit">Add</button>
    </form>
  );
}

// Level row
function LevelRow({ level, onDelete }) {
  return (
    <tr>
      <td>{level.name}</td>
      <td>{level.id}</td>
      <td>{new Date(level.created_at).toLocaleString()}</td>
      <td>
        <button onClick={() => onDelete(level.id)}>Delete</button>
      </td>
    </tr>
  );
}

// Page view
function LevelPageView({ pageSize, pageNum }) {
  const { levels, fetchLevels, loading } = useLevels({ pageSize, pageNum });
  const [showForm, setShowForm] = useState(false);

  const handleDelete = async (levelId) => {
    if (!window.confirm("Are you sure you want to delete this level?")) return;
    try {
      await deleteLevelAPI(levelId);
      alert("Level deleted successfully!");
      fetchLevels();
    } catch (error) {
      console.error(error);
      alert("Failed to delete level.");
    }
  };

  return (
    <main>
      <section>
        <h2>Levels</h2>
      </section>

      <section>
        <div>
          <button onClick={() => setShowForm(true)}>Add Level</button>
        </div>

        <div>
          {showForm && (
            <div>
              <button onClick={() => setShowForm(false)}>Close</button>
              <LevelForm onSuccess={() => {
                setShowForm(false);
                fetchLevels();
              }} />
            </div>
          )}

          {loading ? (
            <p>Loading levels...</p>
          ) : (
            <table border="1" cellPadding="8" cellSpacing="0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>ID</th>
                  <th>Date Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {levels.map((level) => (
                  <LevelRow key={level.id} level={level} onDelete={handleDelete} />
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>
    </main>
  );
}

// Page component
function LevelPage() {
  return <Layout main={<LevelPageView />} />;
}

export default LevelPage;
