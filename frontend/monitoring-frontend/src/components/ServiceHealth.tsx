import { useEffect, useState } from "react";
import ServiceRow from "./ServiceRow";

interface HealthResponse {
  http: number;
  mtls_no_cert: number;
  mtls_cert: number;
}

const ServiceHealth = () => {
  const [health, setHealth] = useState<HealthResponse>();
  const url = "http://localhost:8000/";
  useEffect(() => {
    const fetchHealth = () => {
      fetch(url + "metrics/status/test_results")
        .then((res) => res.json())
        .then((json) => {
          setHealth(json);
        });
    };
    fetchHealth();
    const interval = setInterval(() => {
      fetchHealth();
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  const status_http =
    health?.http == 404 || health?.http == 200 ? "ok" : "fail";
  const status_mtls_no_cert =
    health?.mtls_no_cert == 404 || health?.mtls_no_cert == 200 ? "fail" : "ok";

  const status_mtls_cert =
    health?.mtls_cert == 404 || health?.mtls_cert == 200 ? "ok" : "fail";
  const mtls_zero =
    health?.mtls_no_cert == 0 ? "000" : String(health?.mtls_no_cert);
  return (
    <div className="bg-section-background p-3 mt-5 rounded-xl border border-border-color text-s">
      <h1 className="text-main-text pb-5 pl-3"> SERVICE HEALTH</h1>
      <div className="m-1">
        <ServiceRow
          title={"HTTP:200/404"}
          status_code={String(health?.http)}
          status_message={"200/404"}
          status={status_http}
        />
        <ServiceRow
          title={"mTLS no cert"}
          status_code={String(health?.mtls_no_cert)}
          status_message={mtls_zero}
          status={status_mtls_no_cert}
        />
        <ServiceRow
          title={"mTLS with cert"}
          status_code={String(health?.mtls_cert)}
          status_message={"404"}
          status={status_mtls_cert}
        />
      </div>
    </div>
  );
};

export default ServiceHealth;
