import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Settings, FileText, CheckCircle2, AlertCircle, 
  ChevronRight, History, Save, X, Plus, Clock, 
  Database, Layout, Zap, Layers, Box, Cloud
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000/api';

const App = () => {
  const [activeStep, setActiveStep] = useState(1);
  const [showJiraForm, setShowJiraForm] = useState(false);
  const [jiraConfig, setJiraConfig] = useState({
    url: '',
    email: '',
    token: '',
    name: 'VWO Production'
  });
  
  const [genConfig, setGenConfig] = useState({
    productName: '',
    projectKey: '',
    sprint: '',
    context: ''
  });

  const [status, setStatus] = useState({ loading: false, message: '', type: '' });
  const [connectedUser, setConnectedUser] = useState(null);

  // Load from local storage
  useEffect(() => {
    const saved = localStorage.getItem('jira_config');
    if (saved) {
      const parsed = JSON.parse(saved);
      setJiraConfig(parsed);
      // Auto-test connection if we have data
      if (parsed.url && parsed.email && parsed.token) {
        testJira(parsed);
      }
    }
  }, []);

  const testJira = async (config = jiraConfig) => {
    setStatus({ loading: true, message: 'Verifying Jira Connection...', type: 'info' });
    try {
      const resp = await axios.post(`${API_BASE}/test-jira`, {
        url: config.url,
        auth: { email: config.email, token: config.token }
      });
      if (resp.data.status === 'success') {
        setStatus({ loading: false, message: `Connected to Jira! User: ${resp.data.user}`, type: 'success' });
        setConnectedUser(resp.data.user);
        localStorage.setItem('jira_config', JSON.stringify(config));
        return true;
      } else {
        setStatus({ loading: false, message: resp.data.message, type: 'error' });
        setConnectedUser(null);
        return false;
      }
    } catch (err) {
      setStatus({ loading: false, message: err.message, type: 'error' });
      setConnectedUser(null);
      return false;
    }
  };

  const handleFetchRequirements = async () => {
    if (!genConfig.projectKey) {
      setStatus({ loading: false, message: 'Project Key is required', type: 'error' });
      return;
    }
    setActiveStep(3); // Move to Review
    generatePlan();
  };

  const generatePlan = async () => {
    setStatus({ loading: true, message: 'Generating Intelligent Test Plan...', type: 'info' });
    try {
      // Use the projectKey as the jira_id for fetching (assuming it refers to the latest issues or a specific epic)
      // Or we can modify the backend to handle "Product Name" and "Project Key" specifically.
      // For now, let's treat projectKey as the ID or fetch based on project key.
      const resp = await axios.post(`${API_BASE}/generate-plan`, {
        jira_id: genConfig.projectKey, // Using project key as ID for now
        context: `${genConfig.productName} | ${genConfig.sprint} | ${genConfig.context}`,
        jira_config: {
          url: jiraConfig.url,
          auth: { email: jiraConfig.email, token: jiraConfig.token }
        },
        llm_config: {
          provider: 'Ollama (Local)',
          model: 'llama3:latest'
        }
      });
      if (resp.data.status === 'success') {
        setStatus({ loading: false, message: `Success! Plan saved to: ${resp.data.file_path}`, type: 'success' });
        setActiveStep(4);
      } else {
        setStatus({ loading: false, message: resp.data.message || 'Generation failed', type: 'error' });
      }
    } catch (err) {
      setStatus({ loading: false, message: err.response?.data?.detail || err.message, type: 'error' });
    }
  };

  const renderSetup = () => (
    <div className="setup-view">
      <div className="section-header">
        <h2 className="section-title">Jira Connection</h2>
        <p className="section-desc">Connect to your Jira instance to fetch requirements</p>
      </div>

      {showJiraForm ? (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="card">
          <div className="card-header">
            <button className="btn btn-outline" onClick={() => setShowJiraForm(false)}>
              <Settings size={16} /> Cancel
            </button>
          </div>
          <div className="form-grid">
            <div className="form-group">
              <label>Connection Name</label>
              <input 
                type="text" className="form-control" placeholder="e.g., VWO Production"
                value={jiraConfig.name} onChange={e => setJiraConfig({...jiraConfig, name: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Jira URL</label>
              <input 
                type="text" className="form-control" placeholder="https://yourcompany.atlassian.net"
                value={jiraConfig.url} onChange={e => setJiraConfig({...jiraConfig, url: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Jira Email</label>
              <input 
                type="text" className="form-control" placeholder="your-email@company.com"
                value={jiraConfig.email} onChange={e => setJiraConfig({...jiraConfig, email: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>API Token</label>
              <input 
                type="password" className="form-control" placeholder="Your Jira API token"
                value={jiraConfig.token} onChange={e => setJiraConfig({...jiraConfig, token: e.target.value})}
              />
              <p style={{fontSize: '0.75rem', color: '#64748B', marginTop: '0.5rem'}}>
                Generate at: <a href="https://id.atlassian.com/manage-profile/security/api-tokens" target="_blank" rel="noreferrer">Atlassian API Tokens</a>
              </p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button className="btn btn-primary" onClick={() => testJira()}>Save Connection</button>
          </div>
        </motion.div>
      ) : (
        <div className="card">
          <div className="form-group">
            <label>Select Jira Connection</label>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <select className="form-control" style={{ flex: 1 }}>
                <option>{jiraConfig.name} ({jiraConfig.url || 'Not configured'})</option>
              </select>
            </div>
          </div>
          <button className="btn btn-outline" onClick={() => setShowJiraForm(true)} style={{ marginTop: '1rem' }}>
            <Plus size={16} /> Add New Connection
          </button>
          <button className="btn btn-primary btn-large" style={{ marginTop: '2rem' }} onClick={() => setActiveStep(2)}>
            Continue to Fetch Issues
          </button>
        </div>
      )}

      <div style={{ marginTop: '3rem' }}>
        <h2 className="section-title">Import from Test Management Tools</h2>
        <p className="section-desc">Connect to your existing test case repositories and management platforms</p>
        
        <div className="tools-grid">
          <div className={`tool-card ${connectedUser ? 'connected' : ''}`}>
            {connectedUser && <span className="tool-badge badge-connected"><CheckCircle2 size={12} /> Connected</span>}
            <div className="tool-icon" style={{ background: '#EFF6FF', color: '#2563EB' }}><Database size={24} /></div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.5rem' }}>Jira</h3>
            <p style={{ fontSize: '0.875rem', color: '#64748B', marginBottom: '1rem' }}>Import requirements and user stories from Atlassian Jira</p>
            <ul style={{ fontSize: '0.75rem', color: '#64748B', listStyle: 'none', padding: 0 }}>
              <li>• Requirements import</li>
              <li>• User stories</li>
              <li>• Acceptance criteria</li>
            </ul>
            <button className="btn btn-outline" style={{ width: '100%', marginTop: '1.5rem', justifyContent: 'center' }} onClick={() => setShowJiraForm(true)}>
              Manage Connection
            </button>
          </div>

          {[
            { name: 'TestRail', icon: <Layers />, desc: 'Import existing test cases from TestRail' },
            { name: 'Zephyr', icon: <Zap />, desc: 'Sync test cases from Zephyr Scale or Squad' },
            { name: 'Xray', icon: <Box />, desc: 'Import test cases and plans from Xray' },
            { name: 'Qase', icon: <Box />, desc: 'Import test cases and plans from Qase' },
            { name: 'Azure DevOps', icon: <Cloud />, desc: 'Import test plans and cases from Azure' }
          ].map(tool => (
            <div className="tool-card" key={tool.name}>
              <span className="tool-badge badge-soon">Coming Soon</span>
              <div className="tool-icon" style={{ background: '#F8FAFC', color: '#94A3B8' }}>{tool.icon}</div>
              <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.5rem' }}>{tool.name}</h3>
              <p style={{ fontSize: '0.875rem', color: '#64748B' }}>{tool.desc}</p>
              <button className="btn btn-ghost" style={{ width: '100%', marginTop: '1.5rem', justifyContent: 'center' }}>
                <Clock size={16} /> Notify Me
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderFetch = () => (
    <div className="fetch-view">
      <div className="section-header">
        <h2 className="section-title">Fetch Jira Requirements</h2>
        <p className="section-desc">Enter project details to fetch user stories and requirements</p>
      </div>

      <div className="card">
        <div style={{ background: '#F8FAFC', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <p style={{ fontSize: '0.75rem', color: '#64748B' }}>Connected to:</p>
            <p style={{ fontSize: '0.875rem', fontWeight: 600 }}>{jiraConfig.name} ({jiraConfig.url})</p>
          </div>
          <button className="btn btn-outline" onClick={() => setActiveStep(1)}>Change</button>
        </div>

        <div className="form-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div className="form-group">
            <label>Product Name</label>
            <input 
              type="text" className="form-control" placeholder="e.g., App.vwo.com"
              value={genConfig.productName} onChange={e => setGenConfig({...genConfig, productName: e.target.value})}
            />
          </div>
          <div className="form-group">
            <label>Project Key *</label>
            <input 
              type="text" className="form-control" placeholder="e.g., VWOAPP"
              value={genConfig.projectKey} onChange={e => setGenConfig({...genConfig, projectKey: e.target.value})}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Sprint/Fix Version (Optional)</label>
          <input 
            type="text" className="form-control" placeholder="e.g., Sprint 15 or leave empty for all open issues"
            value={genConfig.sprint} onChange={e => setGenConfig({...genConfig, sprint: e.target.value})}
          />
        </div>

        <div className="form-group">
          <label>Additional Context (Optional)</label>
          <textarea 
            className="form-control" rows="4" placeholder="Any additional information about the product, testing goals, or constraints..."
            value={genConfig.context} onChange={e => setGenConfig({...genConfig, context: e.target.value})}
          ></textarea>
        </div>

        <button className="btn btn-primary btn-large" style={{ marginTop: '1rem' }} onClick={handleFetchRequirements} disabled={status.loading}>
          {status.loading ? 'Fetching...' : <span><Zap size={18} /> Fetch Jira Issues</span>}
        </button>
      </div>
    </div>
  );

  const renderReview = () => (
    <div className="review-view">
      <div className="section-header">
        <h2 className="section-title">Review Generated Requirements</h2>
        <p className="section-desc">AI is analyzing the fetched issues and generating test scenarios...</p>
      </div>

      <div className="card">
        {status.loading ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <div className="loading-spinner" style={{ marginBottom: '1rem' }}></div>
            <p>{status.message}</p>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <CheckCircle2 color="var(--success)" size={48} style={{ marginBottom: '1rem' }} />
            <h3>Analysis Complete</h3>
            <p className="section-desc">Ready to finalize the test plan document.</p>
            <button className="btn btn-primary btn-large" onClick={() => setActiveStep(4)}>
              Preview Test Plan
            </button>
          </div>
        )}
      </div>
    </div>
  );

  const renderTestPlan = () => (
    <div className="final-view">
      <div className="section-header">
        <h2 className="section-title">Final Test Plan</h2>
        <p className="section-desc">Your comprehensive test plan has been generated.</p>
      </div>

      <div className="card">
        <div className="status-banner status-success">
          <CheckCircle2 size={18} /> {status.message}
        </div>
        <div style={{ padding: '2rem', border: '2px dashed var(--border)', borderRadius: '12px', textAlign: 'center', marginBottom: '2rem' }}>
          <FileText size={64} color="var(--primary)" style={{ opacity: 0.5, marginBottom: '1rem' }} />
          <h3>TestPlan_{genConfig.projectKey}.docx</h3>
          <p className="section-desc">Final document with all requirements, edge cases, and test steps.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-outline" style={{ flex: 1, justifyContent: 'center' }} onClick={() => setActiveStep(1)}>Create New Plan</button>
          <button className="btn btn-primary" style={{ flex: 1, justifyContent: 'center' }}>
            Download Document
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-left">
          <div className="logo-box">
            <Zap size={28} />
          </div>
          <div className="header-title">
            <h1>Intelligent Test Planning Agent</h1>
            <p>Generate comprehensive test plans from Jira requirements using AI</p>
          </div>
        </div>
        <button className="btn btn-outline">
          <History size={16} /> View History
        </button>
      </header>

      <div className="stepper-container">
        <div className="stepper">
          {[
            { id: 1, label: '1. Setup' },
            { id: 2, label: '2. Fetch Issues' },
            { id: 3, label: '3. Review' },
            { id: 4, label: '4. Test Plan' }
          ].map(step => (
            <div 
              key={step.id} 
              className={`step ${activeStep === step.id ? 'active' : ''}`}
              onClick={() => step.id < activeStep && setActiveStep(step.id)}
            >
              {step.label}
            </div>
          ))}
        </div>
      </div>

      <main className="main-content">
        <AnimatePresence mode="wait">
          {status.message && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }} 
              animate={{ opacity: 1, y: 0 }} 
              className={`status-banner status-${status.type}`}
            >
              {status.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
              {status.message}
            </motion.div>
          )}

          <motion.div
            key={activeStep}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            transition={{ duration: 0.2 }}
          >
            {activeStep === 1 && renderSetup()}
            {activeStep === 2 && renderFetch()}
            {activeStep === 3 && renderReview()}
            {activeStep === 4 && renderTestPlan()}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
};

export default App;
