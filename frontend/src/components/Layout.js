import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import Footer from './Footer';

const Layout = ({ children }) => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false); //Sidebar 상태 관리

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen); //Sidebar 토글
        console.log("Sidebar State:", !isSidebarOpen)
    };

    return (
        <div id="wrapper">
            <Sidebar isOpen={isSidebarOpen} />
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