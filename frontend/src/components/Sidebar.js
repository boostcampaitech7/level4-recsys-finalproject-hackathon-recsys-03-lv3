import React from "react";

const Sidebar = ({ isOpen, toggleSidebar }) => {
  return (
    <ul
      className={`navbar-nav bg-gradient-primary sidebar sidebar-dark accordion ${isOpen ? "toggled" : ""}`}
      id="accordionSidebar"
    >
      {/* Sidebar - Brand */}
      <a className="sidebar-brand d-flex align-items-center justify-content-center" href="/">
        <div className="sidebar-brand-icon rotate-n-15">
          <i className="fas fa-laugh-wink"></i>
        </div>
        <div className="sidebar-brand-text mx-3">
          HRmony
        </div>
      </a>

      {/* Divider */}
      <hr className="sidebar-divider my-0" />

      {/* Nav Item - Dashboard */}
      <li className="nav-item active">
        <a className="nav-link" href="/">
        <i class="fa-solid fa-house"></i>
          <span>홈</span>
        </a>
      </li>

      {/* Divider */}
      <hr className="sidebar-divider" />

      {/* Heading */}
      <div className="sidebar-heading">REQUEST</div>

      {/* Nav Item - Utilities Collapse Menu */}
      <li className="nav-item">
        <a
          className="nav-link collapsed"
          href="#"
          data-toggle="collapse"
          data-target="#collapseUtilities"
          aria-expanded="false"
          aria-controls="collapseUtilities"
        >
          <i class="fa-solid fa-bullhorn"></i>
          <span>요청</span>
        </a>
        <div
          id="collapseUtilities"
          className="collapse"
          aria-labelledby="headingUtilities"
          data-parent="#accordionSidebar"
        >
          <div className="bg-white py-2 collapse-inner rounded">
            <h6 className="collapse-header">프로젝트 요청</h6>
            <a className="collapse-item" href="utilities-color.html">
              프로젝트 요청
            </a>
            <a className="collapse-item" href="utilities-border.html">
              보낸 요청
            </a>
            <a className="collapse-item" href="utilities-animation.html">
              받은 요청
            </a>
          </div>
        </div>
      </li>

      {/* Divider */}
      <hr className="sidebar-divider" />

      {/* Heading */}
      <div className="sidebar-heading">Project</div>

      {/* Nav Item - Pages Collapse Menu */}
      <li className="nav-item">
        <a
          className="nav-link collapsed"
          href="#"
          data-toggle="collapse"
          data-target="#collapsePages"
          aria-expanded="false"
          aria-controls="collapsePages"
        >
          <i className="fas fa-fw fa-folder"></i>
          <span>프로젝트</span>
        </a>
        <div
          id="collapsePages"
          className="collapse"
          aria-labelledby="headingPages"
          data-parent="#accordionSidebar"
        >
          <div className="bg-white py-2 collapse-inner rounded">
            <h6 className="collapse-header">프로젝트 확인</h6>
            <a className="collapse-item" href="login.html">
              시작 전 프로젝트
            </a>
            <a className="collapse-item" href="register.html">
              진행 중인 프로젝트
            </a>
            <a className="collapse-item" href="forgot-password.html">
              완료 프로젝트
            </a>
          </div>
        </div>
      </li>

      {/* Divider */}
      <hr className="sidebar-divider d-none d-md-block" />

      {/* Heading */}
      <div className="sidebar-heading">mypage</div>

      {/* Nav Item - Tables */}
      <li className="nav-item">
        <a className="nav-link" href="tables.html">
          <i class="fa-solid fa-person"></i>
          <span>마이페이지</span>
        </a>
      </li>

      {/* Divider */}
      <hr className="sidebar-divider d-none d-md-block" />

      {/* Nav Item - Chart */}
      <li className="nav-item">
        <a className="nav-link" href="tables.html">
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
          <span>로그아웃</span>
        </a>
      </li>

      {/* Divider */}
      <hr className="sidebar-divider d-none d-md-block" />

      {/* Sidebar Toggler (Sidebar) */}
      <div className="text-center d-none d-md-inline">
        <button
          className="rounded-circle border-0"
          id="sidebarToggle"
          onClick={toggleSidebar}
        ></button>
      </div>
    </ul>
  );
};

export default Sidebar;
