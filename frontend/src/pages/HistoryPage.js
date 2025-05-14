import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

function HistoryPage() {
  const location = useLocation();
  const username = location.state?.username;

  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    if (!username)
        {
      alert("No username provided");
      return;
    }

    const fetchUserSummaries = async () =>{
      try
      {
        const response = await fetch(`http://localhost:8000/playground/user-history/?user=${username}`);
        if (!response.ok) {
          alert("Failed to fetch user history");
          return;
        }

        const data = await response.json();
        if (data.summaries)
            setSummaries(data.summaries || []);
        else
            setSummaries([]);
      }
      catch (error)
      {
        console.error("Error fetching summaries:", error);
      }
    };

    fetchUserSummaries();
  }, [username]);

  return (
    <div>
      <h2>History for {username}</h2>
      {summaries.length > 0 ? (
        <ul>
          {summaries.map((summary, index) => (
            <li key={index}>{summary}</li>
          ))}
        </ul>
      ) : (
        <p>No history found.</p>
      )}
    </div>
  );
}

export default HistoryPage;
