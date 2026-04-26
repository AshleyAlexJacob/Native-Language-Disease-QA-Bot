import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import ChatView from './components/ChatView';
import DocumentView from './components/DocumentView';
import './layout.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className={`app-container ${sidebarOpen ? 'sidebar-open' : ''}`}>
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={(tab) => {
          setActiveTab(tab);
          setSidebarOpen(false); // Close sidebar on selection for mobile
        }} 
      />
      
      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)}></div>}

      <main className="main-content">
        <TopNav 
          selectedLanguage={selectedLanguage} 
          setSelectedLanguage={setSelectedLanguage} 
          showIngestButton={activeTab === 'docs'}
          toggleSidebar={toggleSidebar}
        />
        
        <div className="view-container">
          {activeTab === 'chat' ? (
            <ChatView selectedLanguage={selectedLanguage} />
          ) : (
            <DocumentView />
          )}
        </div>
      </main>
    </div>
  );
}


export default App;


