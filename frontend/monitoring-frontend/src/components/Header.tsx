const Header = ({ isConnected }: { isConnected: boolean }) => {
  const connection = isConnected ? (
    <div className="flex items-center gap-2">
      <div className="w-2 h-2 rounded-full bg-ok-status"></div>
      <p className="text-muted-text">live, updates every 60s</p>
    </div>
  ) : (
    <div className="flex items-center gap-2">
      <div className="w-2 h-2 rounded-full bg-error-status"></div>
      <p className="text-muted-text">not live, server is unreachable</p>
    </div>
  );
  return (
    <div className="p-5 flex justify-between">
      <div>
        <h1 className="text-main-text ">Monitoring</h1>
      </div>
      {connection}
    </div>
  );
};

export default Header;
