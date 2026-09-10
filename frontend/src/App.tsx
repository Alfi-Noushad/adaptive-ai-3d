import { useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';

const Home = () => (
  <div className="min-h-screen bg-slate-900 text-slate-50 flex flex-col">
    <nav className="border-b border-slate-800 px-6 py-4 flex justify-between items-center max-w-7xl mx-auto w-full">
      <div className="text-xl font-bold tracking-tight text-white">NEXUS<span className="text-indigo-500">ENGINE</span></div>
      <Link to="/login" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">Sign In</Link>
    </nav>
    <main className="flex-grow flex flex-col items-center justify-center px-6 text-center max-w-4xl mx-auto">
      <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6 text-slate-50">
        Professional Pipeline Management
      </h1>
      <p className="text-lg text-slate-400 mb-10 max-w-2xl">
        Streamline your technical art workflow. Manage assets, shaders, and render queues in a clean, centralized, and responsive workspace.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link to="/login" className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-8 rounded-lg shadow-sm transition-colors w-full sm:w-auto text-center">
          Launch Workspace
        </Link>
      </div>
    </main>
  </div>
);

const Login = () => {
  const navigate = useNavigate();
  const [developerId, setDeveloperId] = useState('Mav_Art01');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (developerId && password) {
      localStorage.setItem('nexus_auth', 'true');
      localStorage.setItem('nexus_user', developerId);
      navigate('/dashboard');
    } else {
      setError('Please enter both Developer ID and Password.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 p-6">
      <div className="w-full max-w-md bg-slate-800 border border-slate-700 rounded-2xl shadow-2xl p-8 sm:p-10">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-white">Welcome back</h2>
          <p className="text-sm text-slate-400 mt-2">Sign in to your account to continue</p>
        </div>
        <form onSubmit={handleLogin} className="space-y-5">
          {error && <div className="p-3 bg-red-500/10 border border-red-500/50 text-red-400 text-sm rounded-lg">{error}</div>}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1.5">Developer ID</label>
            <input 
              type="text" 
              value={developerId}
              onChange={(e) => setDeveloperId(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors" 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1.5">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••" 
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors" 
            />
          </div>
          <button type="submit" className="block w-full text-center bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg shadow-sm transition-colors mt-4">
            Authenticate
          </button>
        </form>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const navigate = useNavigate();
  const activeUser = localStorage.getItem('nexus_user') || 'Developer';
  
  const [assets, setAssets] = useState([
    { id: 1, name: 'Hero_BaseMesh_v2.fbx', size: '24.5 MB', time: '10 mins ago', status: 'Processed' },
    { id: 2, name: 'Environment_Albedo.png', size: '8.2 MB', time: '1 hour ago', status: 'Processed' },
  ]);

  const handleLogout = () => {
    localStorage.removeItem('nexus_auth');
    localStorage.removeItem('nexus_user');
    navigate('/login');
  };

  const simulateUpload = () => {
    const newAsset = {
      id: Date.now(),
      name: `New_Rig_Test_${assets.length + 1}.blend`,
      size: `${(Math.random() * 50 + 5).toFixed(1)} MB`,
      time: 'Just now',
      status: 'Reviewing'
    };
    setAssets([newAsset, ...assets]);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col md:flex-row text-slate-300">
      <aside className="w-full md:w-64 bg-slate-950 border-r border-slate-800 flex flex-col">
        <div className="p-6 border-b border-slate-800">
          <span className="text-xl font-bold text-white tracking-tight">NEXUS</span>
        </div>
        <nav className="flex-1 p-4 space-y-1 hidden md:block">
          <Link to="/dashboard" className="block px-3 py-2 bg-indigo-500/10 text-indigo-400 rounded-md font-medium">Overview</Link>
          <Link to="/upload" className="block px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-md transition-colors">Asset Manager</Link>
        </nav>
        <div className="p-4 border-t border-slate-800 hidden md:block">
          <button onClick={handleLogout} className="block w-full text-center py-2 px-4 text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800 rounded-md transition-colors">
            Sign Out
          </button>
        </div>
      </aside>

      <main className="flex-1 p-6 md:p-10 overflow-y-auto bg-slate-900">
        <header className="flex flex-col md:flex-row md:justify-between md:items-end mb-8 gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-white mb-1">{activeUser}'s Workspace</h1>
            <p className="text-sm text-slate-400">Manage your technical art pipeline and assets.</p>
          </div>
          <button onClick={simulateUpload} className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            + Quick Upload
          </button>
        </header>
        
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden shadow-sm">
          <div className="px-6 py-4 border-b border-slate-700 bg-slate-800/50">
            <h3 className="text-base font-semibold text-white">Recent Uploads</h3>
          </div>
          <div className="divide-y divide-slate-700">
            {assets.map((file) => (
              <div key={file.id} className="flex flex-col sm:flex-row sm:items-center justify-between px-6 py-4 hover:bg-slate-700/30 transition-colors cursor-pointer">
                <div className="flex flex-col mb-2 sm:mb-0">
                  <span className="text-sm font-medium text-slate-200">{file.name}</span>
                  <span className="text-xs text-slate-500 mt-0.5">{file.size} • Uploaded {file.time}</span>
                </div>
                <span className={`text-xs px-2.5 py-1 rounded-md font-medium w-fit ${file.status === 'Processed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}`}>
                  {file.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

const Upload = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('nexus_auth');
    localStorage.removeItem('nexus_user');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col md:flex-row text-slate-300">
      <aside className="w-full md:w-64 bg-slate-950 border-r border-slate-800 flex flex-col">
        <div className="p-6 border-b border-slate-800">
          <span className="text-xl font-bold text-white tracking-tight">NEXUS</span>
        </div>
        <nav className="flex-1 p-4 space-y-1 hidden md:block">
          <Link to="/dashboard" className="block px-3 py-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-md transition-colors">Overview</Link>
          <Link to="/upload" className="block px-3 py-2 bg-indigo-500/10 text-indigo-400 rounded-md font-medium">Asset Manager</Link>
        </nav>
        <div className="p-4 border-t border-slate-800 hidden md:block">
          <button onClick={handleLogout} className="block w-full text-center py-2 px-4 text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800 rounded-md transition-colors">
            Sign Out
          </button>
        </div>
      </aside>

      <main className="flex-1 p-6 md:p-10 overflow-y-auto bg-slate-900">
        <header className="mb-8">
          <h1 className="text-2xl md:text-3xl font-bold text-white mb-1">Asset Manager</h1>
          <p className="text-sm text-slate-400">Upload and organize your 3D models and textures.</p>
        </header>

        <div className="border-2 border-dashed border-slate-700 hover:border-indigo-500 bg-slate-800/30 rounded-xl p-10 text-center transition-colors mb-8 cursor-pointer group">
          <div className="w-16 h-16 bg-slate-800 group-hover:bg-indigo-500/20 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-400 group-hover:text-indigo-400 transition-colors">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
          </div>
          <h3 className="text-lg font-medium text-white mb-1">Click or drag files to upload</h3>
          <p className="text-sm text-slate-500">Supports FBX, OBJ, BLEND, and PNG (Max 500MB)</p>
        </div>

        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden shadow-sm">
          <div className="px-6 py-4 border-b border-slate-700 bg-slate-800/50">
            <h3 className="text-base font-semibold text-white">Repository</h3>
          </div>
          <div className="p-8 text-center text-slate-500 text-sm">
            Ready for incoming assets. Drag files above to begin.
          </div>
        </div>
      </main>
    </div>
  );
};

const Register = () => <div className="p-8 text-white">Register Skeleton</div>;
const NotFound = () => <div className="p-8 text-white">404 Not Found</div>;

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}