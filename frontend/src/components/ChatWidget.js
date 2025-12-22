import React, { useState } from 'react';
import styles from './ChatWidget.module.css';

export default function ChatWidget({ apiEndpoint }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const sendMessage = async () => {
    if (!input) return;

    const userMsg = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // UI-first: API can be plugged in later
    if (!apiEndpoint || apiEndpoint === '#') {
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: 'bot', text: '🤖 I’m still learning! Backend coming soon.' },
        ]);
      }, 600);
      return;
    }

    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });
      const data = await response.json();
      const botMsg = { sender: 'bot', text: data.answer };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '⚠️ Error: could not get response' },
      ]);
    }
  };

  return (
    <div className={styles.chatWidget}>
      {/* Toggle Button */}
      <button
        className={styles.toggleBtn}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat widget"
      >
        🤖 {isOpen ? 'Close' : 'Ask AI'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatBox}>
          <div className={styles.messages}>
            {messages.length === 0 && (
              <div className={styles.botMsg}>
                👋 Hi! I’m your Physical AI assistant.  
                Ask me anything about this book.
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={
                  msg.sender === 'user'
                    ? styles.userMsg
                    : styles.botMsg
                }
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className={styles.inputBox}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question…"
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
