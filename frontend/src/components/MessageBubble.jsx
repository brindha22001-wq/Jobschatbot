export default function MessageBubble({ role, text }) {
  return (
    <div className={`message message-${role}`}>
      <p>{text}</p>
    </div>
  );
}
