import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import Footer from "./Footer";

const Layout = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div id="wrapper" className="d-flex">
      <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
      <div id="content-wrapper" className="d-flex flex-column">
        <div id="content">
          <Topbar toggleSidebar={toggleSidebar} />
          <div className="container-fluid">{children}</div>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;
