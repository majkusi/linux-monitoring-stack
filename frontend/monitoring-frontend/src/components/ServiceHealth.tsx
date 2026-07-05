import ServiceRow from "./ServiceRow";

const ServiceHealth = () => {
  return (
    <div className="bg-section-background p-3 mt-5 rounded-xl border border-border-color text-s">
      <h1 className="text-main-text pb-5 pl-3"> SERVICE HEALTH</h1>
      <div className="m-1">
        <ServiceRow
          title={"HTTP:200/404"}
          status_code={"200/404"}
          status={"ok"}
        />
        <ServiceRow
          title={"mTLS no cert"}
          status_code={"000"}
          status={"rejected"}
        />
        <ServiceRow
          title={"mTLS with cert"}
          status_code={"404"}
          status={"reachable"}
        />
      </div>
    </div>
  );
};

export default ServiceHealth;
