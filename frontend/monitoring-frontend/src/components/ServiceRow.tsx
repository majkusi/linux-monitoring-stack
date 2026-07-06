interface ServiceRowProps {
  title: string;
  status_code: string;
  status_message: string;
  status: string;
}

const ServiceRow = ({
  title,
  status_code,
  status_message,
  status,
}: ServiceRowProps) => {
  const color =
    status_code != "000" ? "border-ok-status" : "border-error-status";
  return (
    <div className="flex justify-between items-center text-main-text bg-card-background rounded-xl p-3 m-2 border-border-color border">
      <div>
        <p>{title}</p>
      </div>
      <div className="flex gap-5 items-center">
        <p className="text-muted-text">{status_message}</p>
        <p className={`border ${color} rounded-xl p-2 text-xs`}>{status}</p>
      </div>
    </div>
  );
};

export default ServiceRow;
