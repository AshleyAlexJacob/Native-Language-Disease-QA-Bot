import React, { useState } from 'react';

const ChatView = ({ selectedLanguage }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello, I am your HealthQA Assistant. I can help you analyze medical data or answer questions based on official WHO clinical guidelines. How can I assist you today?',
      type: 'initial'
    },
    {
      role: 'user',
      content: 'What are the recommended treatments for adult bacterial meningitis according to the latest WHO global guidelines?'
    },
    {
      role: 'assistant',
      type: 'insight',
      content: 'Based on the World Health Organization technical guidelines, the empirical antibiotic therapy for adult bacterial meningitis should be initiated immediately. The primary recommendations include the use of **Third-generation cephalosporins** (e.g., ceftriaxone or cefotaxime) [WHO-M-2023-A1].\n\nIn regions with high prevalence of penicillin-resistant pneumococci, the addition of Vancomycin is advised until sensitivities are confirmed. Dexamethasone is also recommended to be administered shortly before or with the first dose of antibiotics to reduce neurological complications [WHO-M-2023-B4].',
      sources: [
        { id: 'A1', title: 'WHO Guidelines for the Prevention and Control of Meningitis Outbreaks', subtitle: 'Section 4.2: Empirical antimicrobial therapy (2023 Revision)' }
      ]
    }
  ]);

  const [input, setInput] = useState('');

  // Mock translation effect
  const getRenderedContent = (content) => {
    if (selectedLanguage !== 'en') {
      return `[Mock Translated to ${selectedLanguage}] ${content}`;
    }
    return content;
  };

  return (
    <div className="chat-view">
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-row ${msg.role}`}>
            <div className="avatar">
              {msg.role === 'assistant' ? (
                <div className="ai-avatar">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
              ) : (
                <div className="user-avatar">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
              )}
            </div>

            <div className="message-content-wrapper">
              {msg.type === 'insight' ? (
                <div className="insight-card">
                  <div className="insight-header">AI CLINICAL INSIGHT</div>
                  <div className="insight-body">
                    {getRenderedContent(msg.content)}
                  </div>
                  <div className="divider"></div>
                  <div className="sources-section">
                    <div className="sources-header">VERIFIED SOURCES</div>
                    {msg.sources.map((source, sIdx) => (
                      <div key={sIdx} className="source-item">
                        <div className="source-label">{source.id}</div>
                        <div className="source-info">
                          <div className="source-title">{source.title}</div>
                          <div className="source-subtitle">{source.subtitle}</div>
                        </div>
                        <div className="source-external">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                            <polyline points="15 3 21 3 21 9"></polyline>
                            <line x1="10" y1="14" x2="21" y2="3"></line>
                          </svg>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className={`message-bubble ${msg.type === 'initial' ? 'initial' : ''}`}>
                  {getRenderedContent(msg.content)}
                  {msg.type === 'initial' && (
                    <div className="suggestion-chips">
                      <button className="chip">Compare WHO guidelines for Hypertension</button>
                      <button className="chip">Analyze pediatric vaccination schedule</button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="chat-input-area">
        <div className="input-container">
          <div className="input-action">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
            </svg>
          </div>
          <input
            type="text"
            placeholder="Type your medical query or ask for document summaries..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <div className="input-right-actions">
            <div className="input-action">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
              </svg>
            </div>
            <button className="send-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
        <div className="input-footer">
          <div className="footer-links">
            <span>EXPORT CHAT</span>
            <span>CLEAR HISTORY</span>
          </div>
        </div>
      </div>

    </div>
  );
};

export default ChatView;
