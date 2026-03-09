import { useState } from "react";

export default function InputBox({ onSend, loading }) {
  const [value, setValue] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || loading) return;
    onSend(trimmed);
    setValue("");
  };

  return (
    <form className="input-row" onSubmit={handleSubmit}>
      <input
        className="chat-input"
        placeholder="Type your question about jobs or careers..."
        value={value}
        onChange={(event) => setValue(event.target.value)}
      />
      <button className="send-btn" type="submit" disabled={loading}>
        {loading ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
