import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/main_logo.png";
import photo from "../assets/profile_example1.jpg";
import ProfileIcon from "./ProfileIcon";
import "../style/Topbar.css";

const Topbar = ({ isLoggedIn, setIsLoggedIn }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    setIsLoggedIn(false); // 로그아웃 시 상태 변경
  };

  return (
    <nav className="navbar">
      {/* 로고 영역 */}
      <img src={logo} alt="Main Logo" />

      {/* 메뉴 영역 */}
      <ul>
        {/* Search Dropdown for Mobile */}
        <li>
          <button
            className="nav-link-btn"
            onClick={() => navigate("/search-freelancer")}
          >
            프리랜서 찾기
          </button>
        </li>
        <li>
          <button
            className="nav-link-btn"
            onClick={() => navigate("/search-project")}
          >
            프로젝트 찾기
          </button>
        </li>
        <li>
          <button
            className="nav-link-btn"
            onClick={() => navigate("/manage-project")}
          >
            프로젝트 관리
          </button>
        </li>
        {isLoggedIn ? (
          <li className="nav-item dropdown no-arrow">
            <a
              className="nav-link dropdown-toggle"
              href="#"
              id="userDropdown"
              role="button"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              <ProfileIcon
                profileImage={photo}
                style={{ width: "35px", height: "35px", margin: "0" }}
              />
            </a>
            <div
              className="dropdown-menu dropdown-menu-right shadow animated--grow-in"
              aria-labelledby="userDropdown"
            >
              <a className="dropdown-item" href="#">
                <i className="fas fa-user fa-sm fa-fw mr-3 text-gray-400"></i>
                마이페이지
              </a>
              <div className="dropdown-divider"></div>
              <a
                className="dropdown-item"
                href="#"
                data-toggle="modal"
                data-target="#logoutModal"
                onClick={handleLogout}
              >
                <i className="fas fa-sign-out-alt fa-sm fa-fw mr-3 text-gray-400"></i>
                로그아웃
              </a>
            </div>
          </li>
        ) : (
          <li>
            <a href="/login" className="login-btn">
              로그인
            </a>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Topbar;
