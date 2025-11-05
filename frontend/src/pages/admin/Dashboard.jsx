import React, { useEffect, useState } from "react";

import { fetchStatsAPI } from "../api/dashboard";
import Layout from "../../components/Layout";
import "./dashboard.css"



const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await fetchStatsAPI();
        setStats(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) return <p>Loading stats...</p>;
  if (error) return <p>Error loading stats: {error.toString()}</p>;

  if (!stats || Object.keys(stats).length === 0)
    return <p>No statistics available.</p>;

  return (
    <div className="stats">
      <div className="stats-item">
        <h1>{stats.User}</h1>
        <p>Registered Users</p>
      </div>

      <div className="stats-item">
        <h1>{stats.Admin}</h1>
        <p>Admins</p>
      </div>

      <div className="stats-item">
        <h1>{stats.Department}</h1>
        <p>Departments</p>
      </div>

      <div className="stats-item">
        <h1>{stats.Level}</h1>
        <p>Levels</p>
      </div>

      <div className="stats-item">
        <h1>{stats.Course}</h1>
        <p>Registered Courses</p>
      </div>

      <div className="stats-item">
        <h1>{stats.File}</h1>
        <p>Uploaded Files</p>
      </div>

    </div>
  );

};


function DashboardPage () {
  return <Layout main={<Dashboard />} />;
}

export default DashboardPage;
