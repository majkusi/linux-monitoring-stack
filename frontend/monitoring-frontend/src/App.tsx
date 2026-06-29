import React, { useEffect, useState } from "react";
import StatCard from "./components/StatCard";
import Header from "./components/Header";
const App = () => {
  const [dataIsLoaded, setDataIsLoaded] = useState(false);
  const url = "";

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then(() => {
        setDataIsLoaded(true);
      });
  }, []);

  return (
    <div className="bg-background min-h-screen">
      <Header isConnected={dataIsLoaded}></Header>
      <div className="grid grid-cols-4 p-5 gap-4">
        <StatCard
          label="CPU"
          value={92}
          unit="%"
          threshold={90}
          threshold_text="threshold "
        ></StatCard>

        <StatCard
          label="RAM"
          value={12.54}
          unit="%"
          threshold={90}
          threshold_text="threshold "
        ></StatCard>

        <StatCard
          label="Disk"
          value={92}
          unit="%"
          threshold={90}
          threshold_text="threshold "
        ></StatCard>

        <StatCard
          label="Uptime"
          value={92}
          unit="%"
          threshold={200}
          threshold_text="HTTP: "
        ></StatCard>
      </div>
    </div>
  );
};

export default App;
