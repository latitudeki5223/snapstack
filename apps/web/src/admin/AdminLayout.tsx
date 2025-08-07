import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';

const AdminLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const navigation = [
    {
      name: 'Dashboard',
      href: '/admin',
      icon: '📊',
      current: location.pathname === '/admin'
    },
    {
      name: 'Parser Studio',
      href: '/admin/parser',
      icon: '🔬',
      current: location.pathname === '/admin/parser'
    },
    {
      name: 'API Monitor',
      href: '/admin/api-monitor',
      icon: '🔌',
      current: location.pathname === '/admin/api-monitor'
    },
    {
      name: 'Users',
      href: '/admin/users',
      icon: '👥',
      current: location.pathname === '/admin/users'
    },
    {
      name: 'Finance',
      href: '/admin/finance',
      icon: '💰',
      current: location.pathname === '/admin/finance'
    },
    {
      name: 'Settings',
      href: '/admin/settings',
      icon: '⚙️',
      current: location.pathname === '/admin/settings'
    }
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-gray-900 transition-all duration-300`}>
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center justify-between px-4 bg-gray-800">
            <div className="flex items-center">
              <span className="text-2xl">🐊</span>
              {sidebarOpen && (
                <span className="ml-2 text-xl font-bold text-white">SnapStack</span>
              )}
            </div>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-400 hover:text-white"
            >
              {sidebarOpen ? '◀' : '▶'}
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`
                  group flex items-center px-2 py-2 text-sm font-medium rounded-md
                  ${item.current
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }
                `}
              >
                <span className="text-xl">{item.icon}</span>
                {sidebarOpen && (
                  <span className="ml-3">{item.name}</span>
                )}
              </Link>
            ))}
          </nav>

          {/* User info */}
          <div className="flex flex-shrink-0 bg-gray-800 p-4">
            <div className="flex items-center">
              <div className="text-2xl">👤</div>
              {sidebarOpen && (
                <div className="ml-3">
                  <p className="text-sm font-medium text-white">Admin User</p>
                  <p className="text-xs text-gray-400">admin@snapstack.com</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Top header */}
        <header className="bg-white shadow-sm">
          <div className="flex items-center justify-between h-16 px-6">
            <h1 className="text-2xl font-semibold text-gray-900">
              Admin Dashboard
            </h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {new Date().toLocaleDateString('en-US', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </span>
              <button className="text-gray-500 hover:text-gray-700">
                🔔
              </button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;