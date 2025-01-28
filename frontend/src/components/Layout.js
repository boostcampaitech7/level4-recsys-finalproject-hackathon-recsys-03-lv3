import React, { useState } from "react";
import Topbar from "./Topbar";
import Footer from "./Footer";
import { Outlet } from "react-router-dom";

const Layout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div
      id="wrapper"
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh", // 화면 전체 높이를 보장
      }}
    >
      <div
        id="content-wrapper"
        style={{
          flex: 1, // 콘텐츠 영역이 남은 공간을 차지
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          id="content"
          style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "95vh",
          }}
        >
          <Topbar toggleSidebar={toggleSidebar} />
          <div className="container-fluid">
            <Outlet />
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;
