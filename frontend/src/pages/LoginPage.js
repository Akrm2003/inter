import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/home", { state: { username } });
  };

  return (
    <div>
      <h2>Welcome to my pdf reader</h2>
      <h3>Please login:</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
            type="password"
            placeholder="Enter password"
            required
        >
        </input>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
