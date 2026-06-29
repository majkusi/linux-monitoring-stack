import React from "react";

interface StatProps {
  label: string;
  value: number;
  unit: string;
  threshold: number;
}

const StatCard = ({ label, value, unit, threshold }: StatProps) => {
  return (
    <div className="bg-background min-h-screen">
      <h1>{label}</h1>
      <h1 className="color">
        {value}
        {unit}
      </h1>
      <h2>
        {threshold}
        {unit}
      </h2>
    </div>
  );
};

export default StatCard;
