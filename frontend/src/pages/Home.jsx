import Navbar from "../components/Navbar";
import ChatBox from "../components/ChatBox";

export default function Home() {
  return (
    <div className="page">
      <Navbar />
      <main className="main-content">
        <section className="hero">
          <h1>Jobs and Career AI Chatbot</h1>
          <p>Ask about roles, skills, and career opportunities.</p>
        </section>
        <ChatBox />
      </main>
    </div>
  );
}
