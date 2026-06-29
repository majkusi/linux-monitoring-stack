import React from "react";
import StatCard from "./components/StatCard";
const App = () => {
  return (
    <div className="bg-gray-600">
      <h1 className="text-green-500">dashboard</h1>
      <StatCard label="test" value={20} unit="%" threshold={90}></StatCard>
    </div>
  );
};

export default App;
