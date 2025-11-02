import { useState, useEffect } from "react";

import Layout from "../../components/Layout";
import {
  fetchFilesAPI,
  updateFileAPI,
  deleteFileAPI,
  downloadFileAPI,
} from "../api/files";
import UploadMultipleFilesForm from "../../components/UploadFileForm";



function FilesPageView() {
  const [status, setStatus] = useState("pending");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showUploadForm, setShowUploadForm] = useState(false);

  // Pagination state
  const [pageSize, setPageSize] = useState(15);
  const [pageNum, setPageNum] = useState(1);

  // Fetch files by status, page size, and page number
  async function fetchFiles() {
    setLoading(true);
    try {
      const data = await fetchFilesAPI(status, pageSize, pageNum);
      if (data) {
        setFiles(data);
      } else {
        setFiles([]);
      }
    } catch (error) {
      console.error("Failed to fetch files:", error);
      setFiles([]);
    } finally {
      setLoading(false);
    }
  }

  // Refetch files whenever status, pageSize, or pageNum changes
  useEffect(() => {
    fetchFiles();
  }, [status, pageSize, pageNum]);

  // Approve a file (update status to "approved")
  const handleApprove = async (fileId) => {
    try {
      await updateFileAPI(fileId, { status: "approved" });
      fetchFiles();
    } catch (error) {
      console.error("Failed to approve file:", error);
      alert("Failed to approve file, please try again.");
    }
  };

  // Reject a file (update status to "rejected")
  const handleReject = async (fileId) => {
    try {
      await updateFileAPI(fileId, { status: "rejected" });
      fetchFiles();
    } catch (error) {
      console.error("Failed to reject file:", error);
      alert("Failed to reject file, please try again.");
    }
  };

  // Delete a file
  const handleDelete = async (fileId) => {
    if (window.confirm("Are you sure you want to delete this file?")) {
      try {
        await deleteFileAPI(fileId);
        fetchFiles();
      } catch (error) {
        console.error("Failed to delete file:", error);
        alert("Failed to delete file, please try again.");
      }
    }
  };

  // View or Download file
  const handleView = async (fileId) => {
    try {
      await downloadFileAPI(fileId);
    } catch (error) {
      console.error("Failed to view file:", error);
      alert("Unable to open file. Please try again.");
    }
  };


  return (
        <div>
          <section>
            <h2>Manage Uploaded Files</h2>
          </section>

          <section>
            <button
              onClick={() => setShowUploadForm(true)}
            >
              + Upload Files
            </button>

            {/* Upload Files Modal */}
            {showUploadForm && (
              <div>
                <div>
                  <UploadMultipleFilesForm
                    onClose={() => setShowUploadForm(false)}
                    onUploaded={() => {
                      fetchFiles();
                      setShowUploadForm(false);
                    }}
                  />
                </div>
              </div>
            )}

            {/* Status filter buttons */}
          <div>
            {["pending", "approved", "rejected"].map((s) => (
                <button
                  key={s}
                  className={`px-4 py-2 rounded ${
                    status === s
                      ? "bg-blue-600 text-white"
                      : "bg-gray-200 hover:bg-gray-300"
                  }`}
                  onClick={() => {
                    setStatus(s);
                    setPageNum(1); // reset page on status change
                  }}
                >
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </button>
              ))}
              
              {/* Pagination controls */}
              <div className="mb-4 flex items-center gap-4">
                <label>
                  Files per page:{" "}
                  <select
                    value={pageSize}
                    onChange={(e) => {
                      setPageSize(Number(e.target.value));
                      setPageNum(1); // reset to first page on page size change
                    }}
                    className="border rounded px-2 py-1"
                  >
                    {[10, 15, 25, 50].map((size) => (
                      <option key={size} value={size}>
                        {size}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Page:{" "}
                  <input
                    type="number"
                    min={1}
                    value={pageNum}
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      if (val >= 1) setPageNum(val);
                    }}
                  />
                </label>

                <button
                  onClick={fetchFiles}
                  disabled={loading}
                >
                  Go
                </button>
              </div>
            </div>
          </section>

          

          {/* Files table or loading */}
          <section>
            {loading ? (
              <p>Loading files...</p>
            ) : files.length === 0 ? (
              <p>No files found for status "{status}"</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>View</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {files.map((file) => (
                    <tr key={file.id}>
                      <td>{file.id}</td>
                      <td>{file.file_name}</td>
                      <td>{file.status}</td>
                      <td><button onClick={() => handleView(file.id)}>view</button></td>
                      <td>
                        {status === "pending" && (
                          <>
                            <button
                              onClick={() => handleApprove(file.id)}
                            >
                              Approve
                            </button>
                            <button
                              onClick={() => handleReject(file.id)}
                            >
                              Reject
                            </button>
                          </>
                        )}
                        <button
                          onClick={() => handleDelete(file.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </div>
  );
}


function FilePage() {
  return <Layout main={<FilesPageView />} />
}

export default FilePage