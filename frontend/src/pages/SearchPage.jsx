import { useState } from "react";
import axios from "axios";
import { API_URL } from "../api";
import "./SearchPage.css";

export default function SearchPage() {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [results, setResults] = useState([]);
  const [busy, setBusy] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const searchByFile = async () => {
    if (!file) {
      alert("Please select a file to search");
      return;
    }
    setBusy(true);
    setErrorMsg("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await axios.post(`${API_URL}/similar-file`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (res.data.error) {
        setErrorMsg(res.data.error);
        setResults([]);
      } else {
        setResults(res.data.similar_images || []);
      }
    } catch (err) {
      console.error(err);
      setErrorMsg("Search failed — check backend logs");
      setResults([]);
    } finally {
      setBusy(false);
    }
  };

  const searchByUrl = async () => {
    if (!url) {
      alert("Please enter an image URL");
      return;
    }
    setBusy(true);
    setErrorMsg("");
    try {
      const res = await axios.post(`${API_URL}/similar-url`, { url });
      if (res.data.error) {
        setErrorMsg(res.data.error);
        setResults([]);
      } else {
        setResults(res.data.similar_images || []);
      }
    } catch (err) {
      console.error(err);
      setErrorMsg("Search failed — check backend logs");
      setResults([]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="search-page">
      <h2>🔍 Find Similar Images</h2>

      <div className="search-inputs">
        {/* File Upload */}
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={searchByFile} disabled={busy || !file}>
            {busy ? "Searching..." : "Search File"}
          </button>
        </div>

        {/* URL Search */}
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <input
            type="text"
            placeholder="Enter image URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button onClick={searchByUrl} disabled={busy || !url}>
            {busy ? "Searching..." : "Search URL"}
          </button>
        </div>
      </div>

      {errorMsg && <div className="error-msg">{errorMsg}</div>}

      <div className="results-grid">
        {results.length === 0 && !errorMsg ? (
          <div className="no-results">No results yet.</div>
        ) : (
          results.map((r, i) => (
            <div key={i} className="image-card">
             <img 
      src={r.url.startsWith("http") ? r.url : `${API_URL}${r.url}`} 
      alt={r.filename} 
    />
              <div className="card-text">
                <div className="filename">{r.filename}</div>
                <div className="score">Score: {r.score.toFixed(3)}</div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
