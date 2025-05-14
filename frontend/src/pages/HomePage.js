import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state?.username;
  const [summary, setSummary] = useState("");
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]); // Store the file object in state
  };

  const handleUploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user", username);

    try {
      const response = await fetch("http://localhost:8000/playground/read-pdf/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setSummary(data.summary);
      } else {
        alert("Failed to upload PDF");
      }
    } catch (error) {
      console.error("Error uploading PDF:", error);
      alert("Error uploading PDF");
    }
  };

  const handleSeeMyHistory = () => {
    navigate('/history', { state: { username } });
  };

  return (
    <div>
      <h2>Welcome {username}</h2>
        <h3>Upload a PDF file:</h3>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <br />
      <button onClick={handleUploadPDF}>Upload PDF</button>
      <p>{summary}</p>
      <br />
      <button onClick={handleSeeMyHistory}>See My History</button>
    </div>
  );
}

export default HomePage;
