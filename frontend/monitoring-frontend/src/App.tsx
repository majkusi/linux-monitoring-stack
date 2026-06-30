import React, { useEffect, useState } from "react";
import StatCard from "./components/StatCard";
import Header from "./components/Header";
import MetricsChart from "./components/MetricsChart";

interface StatResponse {
  time_stamp: string;
  ram_pct: number;
  ram_used: number;
  ram_total: number;
  disk_pct: number;
  cpu_pct: number;
}

interface StatusResponse {
  time_stamp: string;
  uptime_pct: number;
  successes: number;
  total: number;
}

const App = () => {
  const [resources, setResources] = useState<StatResponse[]>([]);
  const [status, setStatus] = useState<StatusResponse>();
  const [dataIsLoaded, setDataIsLoaded] = useState(false);
  const url = "http://localhost:8000/";

  useEffect(() => {
    fetch(url + "metrics/average/uptime")
      .then((res) => res.json())
      .then((json) => {
        setStatus(json);
      });
  }, []);

  useEffect(() => {
    fetch(url + "metrics")
      .then((res) => res.json())
      .then((json) => {
        setResources(json);
        setDataIsLoaded(true);
      });
  }, []);

  return (
    <>
      <div className="bg-background min-h-screen">
        <Header isConnected={dataIsLoaded}></Header>
        <div className="grid grid-cols-4 p-5 gap-4">
          <StatCard
            label="CPU"
            value={resources[0]?.cpu_pct ?? 0}
            unit="%"
            threshold={90}
            threshold_text="threshold "
            showThresholdUnit={true}
          ></StatCard>

          <StatCard
            label="RAM"
            value={resources[0]?.ram_pct ?? 0}
            unit="%"
            threshold={90}
            threshold_text="threshold "
            showThresholdUnit={true}
          ></StatCard>

          <StatCard
            label="Disk"
            value={resources[0]?.disk_pct ?? 0}
            unit="%"
            threshold={90}
            threshold_text="threshold "
            showThresholdUnit={true}
          ></StatCard>

          <StatCard
            label="Uptime"
            value={status?.uptime_pct ?? 0}
            unit="%"
            threshold={8080}
            threshold_text="HTTP: "
            showThresholdUnit={false}
          ></StatCard>
        </div>
      </div>
      <MetricsChart />
    </>
  );
};

export default App;
