import React from 'react';

const DocumentView = () => {
  const stats = [
    { label: 'TOTAL DOCUMENTS', value: '142', sub: '12 added this month', color: 'teal' },
    { label: 'PROCESSING', value: '08', sub: 'Average time: 4m 12s', color: 'orange' },
    { label: 'SYSTEM HEALTH', value: '99.2%', sub: 'Ingestion accuracy rate', color: 'green' }
  ];

  const inventory = [
    { name: 'WHO Hypertension Guidelines 2024', filename: 'GUIDELINE_HT_V2.pdf • 4.2MB', lang: 'English (Global)', date: 'Oct 24, 2023', status: 'Ingested' },
    { name: 'Maternal Health Standards - Vol 4', filename: 'MHS_STANDARDS_FINAL.docx • 1.8 MB', lang: 'French (Europe)', date: 'Oct 28, 2023', status: 'Processing' },
    { name: 'Vector-borne Disease Control', filename: 'WHO_VBD_REVISION.pdf • 12.5 MB', lang: 'English (Global)', date: 'Oct 30, 2023', status: 'Ingested' }
  ];

  return (
    <div className="doc-view">
      <div className="doc-header">
         <div className="breadcrumb">Clinical Library &gt; WHO Guidelines</div>
         <div className="header-main">
            <h2>WHO Clinical Guidelines</h2>
            <button className="add-doc-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="12" y1="18" x2="12" y2="12"></line>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
              <span>Add Document</span>
            </button>
         </div>
         <p className="subtitle">Manage clinical documentation and automate ingestion into the AI knowledge base.</p>
      </div>

      <div className="stats-grid">
        {stats.map((stat, i) => (
          <div key={i} className="stat-card">
            <div className="stat-label">{stat.label}</div>
            <div className="stat-value-row">
              <span className="stat-value">{stat.value}</span>
              <div className={`stat-icon ${stat.color}`}>
                 {stat.color === 'teal' && '📄'}
                 {stat.color === 'orange' && '🔄'}
                 {stat.color === 'green' && '✅'}
              </div>
            </div>
            <div className="stat-sub">{stat.sub}</div>
          </div>
        ))}
      </div>

      <div className="inventory-section">
        <div className="inventory-header">
           <h3>Guidelines Inventory</h3>
           <div className="inventory-actions">
              <div className="search-box">
                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                 </svg>
                 <input type="text" placeholder="Search guidelines..." />
              </div>
              <div className="filter-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                </svg>
              </div>
           </div>
        </div>

        <table className="inventory-table">
          <thead>
            <tr>
              <th>DOCUMENT NAME</th>
              <th>LANGUAGE</th>
              <th>DATE ADDED</th>
              <th>STATUS</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map((item, i) => (
              <tr key={i}>
                <td>
                  <div className="doc-info">
                    <div className="doc-icon-small">
                       {item.filename.includes('pdf') ? '📄' : '📝'}
                    </div>
                    <div>
                      <div className="doc-name">{item.name}</div>
                      <div className="doc-filename">{item.filename}</div>
                    </div>
                  </div>
                </td>
                <td className="doc-lang">{item.lang}</td>
                <td className="doc-date">{item.date}</td>
                <td>
                  <span className={`status-chip ${item.status.toLowerCase()}`}>
                    {item.status}
                  </span>
                </td>
                <td>
                  <div className="table-actions">
                     <span>👁️</span>
                     <span>🗑️</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="table-footer">Showing 1-10 of 142 documents</div>
      </div>

      <div className="optimization-banner">
         <div className="opt-icon">✨</div>
         <div className="opt-content">
            <h4>AI Knowledge Optimization</h4>
            <p>The system has identified 12 documents that could benefit from structural re-indexing to improve query speed.</p>
         </div>
         <button className="reindex-btn">Re-index Library</button>
      </div>

      <div className="ingestion-overlay">
         <div className="ingestion-header">
            <span>Active Ingestion</span>
            <span className="close-btn">×</span>
         </div>
         <div className="ingestion-body">
            <div className="ingestion-info">
               <span className="ing-filename">Ebola_Response_Protocol.pdf</span>
               <span className="ing-pct">65%</span>
            </div>
            <div className="progress-bar">
               <div className="progress-fill" style={{width: '65%'}}></div>
            </div>
            <div className="ingestion-status">Vectorizing medical terminology...</div>
         </div>
      </div>

    </div>
  );
};

export default DocumentView;
