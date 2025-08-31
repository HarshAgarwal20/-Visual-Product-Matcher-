import { useState } from "react";
import axios from "axios";
import { API_URL } from "../api";
import "./PagesStyle.css";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploaded, setUploaded] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await axios.post(`${API_URL}/upload`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("✅ File uploaded successfully");
      setUploaded(res.data);
    } catch (err) {
      console.error(err);
      setMessage("❌ Upload failed");
    }
  };

  return (
    <div className="page-container">
      {/* Existing navigation links 
      <div className="top-nav">
        <a href="/upload">Upload</a>
        <a href="/search">Search</a>
      </div>
*/}
      <h2>Upload Image</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!file}>
        Upload
      </button>

      {message && <div className="message">{message}</div>}

      {uploaded && (
        <div className="results-grid">
          <div className="image-card">
            <img src={`${API_URL}${uploaded.url}`} alt={uploaded.filename} />
            <div className="card-text">{uploaded.filename}</div>
          </div>
        </div>
      )}
    </div>
  );
}
