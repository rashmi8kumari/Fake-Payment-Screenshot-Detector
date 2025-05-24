import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { FaMoon, FaSun, FaUpload, FaCheckCircle, FaTimesCircle, FaImage, FaEye, FaEyeSlash, FaFileDownload } from "react-icons/fa";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState("");
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [showMetadata, setShowMetadata] = useState(false);
  const [reportUrl, setReportUrl] = useState("");

  const handleFileChange = (file) => {
    if (!file) return;

    // ✅ Validate file type
    const allowedTypes = ["image/png", "image/jpeg", "image/jpg"];
    if (!allowedTypes.includes(file.type)) {
      setError("❌ Invalid file type. Only PNG, JPG, and JPEG are allowed.");
      return;
    }

    // ✅ Validate file size (Max: 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError("❌ File is too large. Max size is 5MB.");
      return;
    }

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setError("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("⚠️ Please select a file first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(response.data.result);
      setMetadata(response.data.metadata);
      setError("");

      // ✅ Use the direct report URL for PDF download
      setReportUrl(response.data.report_url);
    } catch (error) {
      setError(error.response?.data?.error || "❌ Error processing image.");
      setResult("");
      setMetadata(null);
      setReportUrl("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`d-flex flex-column ${darkMode ? "bg-dark text-light" : "bg-light text-dark"}`} style={{ minHeight: "100vh" }}>

      {/* ✅ Stylish Header */}
      <nav className={`navbar navbar-expand-lg shadow ${darkMode ? "navbar-dark bg-gradient bg-secondary" : "navbar-light bg-gradient bg-primary"}`}>
        <div className="container">
          <a className="navbar-brand fw-bold text-light" href="/">🛡️ Fake Payment Detector</a>
          <div>
            <button className="btn btn-outline-light mx-2">Home</button>
            <button className="btn btn-outline-light mx-2">About</button>
            <button className="btn btn-outline-light mx-2">Login</button>
            <button className="btn btn-outline-light mx-2">Signup</button>
            <button className={`btn ${darkMode ? "btn-warning" : "btn-dark"}`} onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? <FaSun size={20} /> : <FaMoon size={20} />}
            </button>
          </div>
        </div>
      </nav>

      {/* ✅ Centered Content */}
      <div className="container d-flex flex-column align-items-center justify-content-center flex-grow-1">
        
        {/* ✅ Drag & Drop Zone */}
        <div
          className={`border p-4 ${dragging ? "bg-secondary text-white" : darkMode ? "bg-dark text-light" : "bg-light text-dark"} rounded shadow mt-4 text-center w-75`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            handleFileChange(e.dataTransfer.files[0]);
          }}
        >
          <FaImage size={40} className="text-muted" />
          <p className="mt-2 fw-bold">Drag & Drop an image here, or click to select</p>
          <input type="file" className="form-control mt-2" onChange={(e) => handleFileChange(e.target.files[0])} />
        </div>

        {/* ✅ Image Preview */}
        {preview && <img src={preview} alt="Preview" className="img-thumbnail mt-3 shadow d-block mx-auto" style={{ maxHeight: "200px" }} />}

        {/* ✅ Upload Button */}
        <button className="btn btn-success w-50 mt-3" onClick={handleUpload} disabled={loading}>
          {loading ? "Analyzing..." : <><FaUpload /> Analyze</>}
        </button>

        {/* ✅ Progress Bar */}
        {loading && <div className="progress mt-3 w-50"><div className="progress-bar progress-bar-striped progress-bar-animated w-100"></div></div>}

        {/* ✅ Error Message */}
        {error && <h4 className="text-danger mt-4"><FaTimesCircle /> {error}</h4>}

        {/* ✅ Result Display */}
        {result && (
          <h2 className={`mt-4 p-3 rounded shadow text-center w-50 ${result === "Fake" ? "bg-danger text-white" : "bg-success text-white"}`}>
            {result === "Fake" ? <FaTimesCircle /> : <FaCheckCircle />} Result: {result}
          </h2>
        )}

        {/* ✅ Download PDF Report */}
        {reportUrl && (
          <a href={reportUrl} className="btn btn-info mt-3" download="report.pdf">
            <FaFileDownload /> Download Report (PDF)
          </a>
        )}

        {/* ✅ Metadata Toggle */}
        {metadata && (
          <div className="mt-4 text-center w-75">
            <button className={`btn ${darkMode ? "btn-outline-light" : "btn-outline-info"}`} onClick={() => setShowMetadata(!showMetadata)}>
              {showMetadata ? <FaEyeSlash /> : <FaEye />} {showMetadata ? "Hide Metadata" : "Show Metadata"}
            </button>
            {showMetadata && (
              <pre className={`p-3 border rounded mt-3 text-start ${darkMode ? "bg-secondary text-light" : "bg-light text-dark"}`} style={{ whiteSpace: "pre-wrap" }}>
                {JSON.stringify(metadata, null, 2)}
              </pre>
            )}
          </div>
        )}
      </div>

      {/* ✅ Sticky Footer */}
      <footer className={`text-center p-3 shadow ${darkMode ? "bg-secondary text-light" : "bg-primary text-light"}`} style={{ position: "relative", bottom: "0", width: "100%" }}>
        <p className="mb-0">© 2025 Fake Payment Detector. All rights reserved.</p>
      </footer>

    </div>
  );
}

export default App;









