import React from "react";

interface StatProps {
  label: string;
  value: number;
  unit: string;
  threshold: number;
  threshold_text: string;
  showThresholdUnit: boolean;
}

const StatCard = ({
  label,
  value,
  unit,
  threshold,
  threshold_text,
  showThresholdUnit,
}: StatProps) => {
  const color =
    value < 60
      ? "text-ok-status"
      : value > threshold
        ? "text-error-status"
        : "text-warning-status";
  const showUnit = showThresholdUnit ? unit : "";

  return (
    <div className="bg-card-background rounded-xl p-5 border-border-color">
      <p className="text-main-text">{label}</p>
      <p className={`${color} text-4xl`}>
        {value}
        {unit}
      </p>

      <p className="text-muted-text">
        {threshold_text}
        {threshold}
        {showUnit}
      </p>
    </div>
  );
};

export default StatCard;
