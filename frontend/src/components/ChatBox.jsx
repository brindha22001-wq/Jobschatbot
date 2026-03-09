import { useState } from "react";
import MessageBubble from "./MessageBubble";
import InputBox from "./InputBox";
import { sendChatMessage } from "../services/api";

export default function ChatBox() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hello! Ask me anything about jobs and careers." },
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (query) => {
    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setLoading(true);

    try {
      const response = await sendChatMessage(query);
      const answer = response.answer || "No response available.";
      setMessages((prev) => [...prev, { role: "bot", text: answer }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Backend is not reachable. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="chatbox">
      <div className="messages">
        {messages.map((msg, idx) => (
          <MessageBubble key={`${msg.role}-${idx}`} role={msg.role} text={msg.text} />
        ))}
      </div>
      <InputBox onSend={handleSend} loading={loading} />
    </section>
  );
}
