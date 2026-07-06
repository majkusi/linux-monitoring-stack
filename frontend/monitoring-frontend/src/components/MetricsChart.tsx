import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";

interface LineChartData {
  time_stamp: string;
  ram_pct: number;
  disk_pct: number;
  cpu_pct: number;
}

const MetricsChart = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [chartData, setChartData] = useState<LineChartData[]>([]);
  const chartRef = useRef<Chart | null>(null);

  const url = "http://localhost:8000/";

  useEffect(() => {
    const fetchData = () => {
      fetch(url + "metrics").then((res) =>
        res.json().then((json) => {
          setChartData(json);
        }),
      );
    };
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const timestamp = chartData.map((d) => d.time_stamp.split("T")[1]);
    const cpu = chartData.map((d) => d.cpu_pct);
    const ram = chartData.map((d) => d.ram_pct);
    const disk = chartData.map((d) => d.disk_pct);
    if (chartRef.current) chartRef.current.destroy();
    if (canvasRef.current != null)
      chartRef.current = new Chart(canvasRef.current, {
        type: "line",
        data: {
          labels: timestamp,
          datasets: [
            { label: "CPU", data: cpu, borderColor: "#d85a30", pointRadius: 0 },
            { label: "RAM", data: ram, borderColor: "#378add", pointRadius: 0 },
            {
              label: "DISK",
              data: disk,
              borderColor: "#bc37dd",
              pointRadius: 0,
            },
          ],
        },
        options: {
          plugins: {
            legend: {
              labels: { color: "#f9fafb" },
            },
          },
          scales: {
            x: {
              ticks: { color: "#f9fafb" },
              grid: { color: "#2d2f3d" },
            },
            y: {
              ticks: { color: "#f9fafb" },
              grid: { color: "#2d2f3d" },
            },
          },
        },
      });
  }, [chartData]);

  return (
    <div className="bg-card-background p-3 rounded-xl">
      <h1 className="text-main-text"> CPU & RAM - LAST 24H</h1>
      <canvas ref={canvasRef}></canvas>
    </div>
  );
};

export default MetricsChart;
