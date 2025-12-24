import React, { useState } from 'react';
import styles from './ChatWidget.module.css';

export default function ChatWidget({ fullBookEndpoint, selectedTextEndpoint, bookId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [queryMode, setQueryMode] = useState('full'); // 'full' or 'selected'

  const sendMessage = async () => {
    if (!input) return;

    const userMsg = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // Choose endpoint based on queryMode
    const apiEndpoint = queryMode === 'full' ? fullBookEndpoint : selectedTextEndpoint;

    if (!apiEndpoint) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: '🤖 API endpoint not configured!' },
      ]);
      return;
    }

    try {
      // Build request body depending on query type
      const body =
        queryMode === 'full'
          ? { book_id: bookId, query: input, max_results: 5, temperature: 0.7 }
          : { selected_text: input, query: input, temperature: 0.7 };

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();
      const botMsg = { sender: 'bot', text: data.response || 'No response returned.' };
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

      {isOpen && (
        <div className={styles.chatBox}>
          {/* Query Mode Selector */}
          <div className={styles.modeSelector}>
            <label>
              <input
                type="radio"
                value="full"
                checked={queryMode === 'full'}
                onChange={() => setQueryMode('full')}
              />
              Full Book
            </label>
            <label>
              <input
                type="radio"
                value="selected"
                checked={queryMode === 'selected'}
                onChange={() => setQueryMode('selected')}
              />
              Selected Text
            </label>
          </div>

          {/* Chat Messages */}
          <div className={styles.messages}>
            {messages.length === 0 && (
              <div className={styles.botMsg}>
                👋 Hi! I’m your Physical AI assistant. Ask me anything about this book.
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={msg.sender === 'user' ? styles.userMsg : styles.botMsg}>
                {msg.text}
              </div>
            ))}
          </div>

          {/* Input Box */}
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
