import React from "react";
import "../style/sidebar.css"

const Sidebar = ({ isOpen }) => {
  return (
        <ul 
            className={`navbar-nav bg-gradient-primary sidebar sidebar-dark accordion ${ 
                isOpen ? "toggled" : "collapsed"
            }`} 
            id="accordionSidebar"
        >
        <a className="sidebar-brand d-flex align-items-center justify-content-center" href="/">
          <div className="sidebar-brand-icon rotate-n-15">
            <i className="fas fa-laugh-wink"></i>
          </div>
          <div className="sidebar-brand-text mx-3">Hrmony</div>
        </a>
        <hr className="sidebar-divider my-0" />
        <li className="nav-item active">
          <a className="nav-link" href="/">
            <i className="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span>
          </a>
        </li>
        <li className="nav-item active">
          <a 
            className="nav-link collapsed" 
            href="#" 
            data-toggle="collapse" 
            data-target="#collapseTwo" 
            aria-expanded="false" 
            aria-controls="collapseTwo"
        >
            <i className="fas fa-fw fa-cog"></i>
            <span>프로젝트</span>
          </a>
          <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
            <div className="bg-white py-2 collapse-inner rounded">
              <h6 className="collapse-header">프로젝트</h6>
              <a className="collapse-item active" href="BeforeStartingProjects.js">시작 전 프로젝트</a>
              <a className="collapse-item" href="ProgressingPro">진행 중 프로젝트</a>
              <a className="collapse-item" href="cards.html">완료된 프로젝트</a>
            </div>
          </div>
        </li>
      </ul>
  );
};

export default Sidebar;