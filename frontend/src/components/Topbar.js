import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/main_logo.png";
import photo from "../assets/profile_example1.jpg";
import ProfileIcon from "./ProfileIcon";
import "../style/Topbar.css";

const Topbar = () => {
  const token =
    sessionStorage.getItem("token") || localStorage.getItem("token");
  const userId =
    sessionStorage.getItem("userId") || localStorage.getItem("userId");
  const userName =
    sessionStorage.getItem("userName") || localStorage.getItem("userName");
  const userType =
    sessionStorage.getItem("userType") || localStorage.getItem("userType");
  const navigate = useNavigate();
  const [dropdownState, setDropdownState] = useState({
    projectDropdownOpen: false,
    freelancerDropdownOpen: false,
  });

  const handleLogout = () => {
    sessionStorage.removeItem("token");
    localStorage.removeItem("token");
    window.location.href = "/login"; // 로그인 페이지로 이동
  };

  const toggleDropdown = (dropdownName) => {
    setDropdownState((prev) => ({
      projectDropdownOpen:
        dropdownName === "project" ? !prev.projectDropdownOpen : false,
      freelancerDropdownOpen:
        dropdownName === "freelancer" ? !prev.freelancerDropdownOpen : false,
    }));
  };

  // useEffect로 외부 클릭 감지
  useEffect(() => {
    const handleClickOutside = (event) => {
      // 드롭다운 내부를 클릭한 경우 닫지 않음
      if (
        !event.target.closest(".dropdown-menu") &&
        !event.target.closest(".dropdown-toggle")
      ) {
        setDropdownState({
          projectDropdownOpen: false,
          freelancerDropdownOpen: false,
        });
      }
    };

    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <nav className="navbar">
      {/* 로고 영역 */}
      <img src={logo} alt="Main Logo" onClick={() => navigate("/main-page")} />

      {/* 메뉴 영역 */}
      <ul className="nav-menu">
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
        {/* userType에 따라 프로젝트 관리 버튼 */}
        {userType === 1 ? (
          <li className="nav-item dropdown">
            <button
              className="nav-link-btn dropdown-toggle"
              id="projectDropdown"
              onClick={() => toggleDropdown("project")}
            >
              프로젝트 관리
            </button>
            {dropdownState.projectDropdownOpen && (
              <div
                className="custom-dropdown-menu"
                aria-labelledby="projectDropdown"
              >
                <button
                  className="dropdown-item"
                  onClick={() => navigate("/registered-projects")}
                >
                  <i class="fas fa-solid fa-file-import mr-3 text-gray-400"></i>
                  등록한 프로젝트
                </button>
                <button
                  className="dropdown-item"
                  onClick={() => navigate("/finished")}
                >
                  <i class="fas fa-solid fa-file-contract mr-3 text-gray-400"></i>
                  완료된 프로젝트
                </button>
              </div>
            )}
          </li>
        ) : (
          <li>
            <button
              className="nav-link-btn"
              onClick={() => navigate("/applied")}
            >
              프로젝트 관리
            </button>
          </li>
        )}
        {token ? (
          <li className="nav-item dropdown no-arrow">
            <button
              className="nav-link-btn dropdown-toggle"
              id="freelancerDropdown"
              onClick={() => toggleDropdown("freelancer")} // 클릭 시 토글
            >
              <ProfileIcon
                profileImage={photo}
                style={{ width: "35px", height: "35px", margin: "0" }}
              />
            </button>
            {dropdownState.freelancerDropdownOpen && (
              <div
                className="custom-dropdown-menu"
                aria-labelledby="userDropdown"
              >
                <button
                  className="dropdown-item"
                  onClick={() => navigate("/mypage")}
                >
                  <i className="fas fa-user fa-sm fa-fw mr-3 text-gray-400"></i>
                  마이페이지
                </button>
                <button className="dropdown-item" onClick={handleLogout}>
                  <i className="fas fa-sign-out-alt fa-sm fa-fw mr-3 text-gray-400"></i>
                  로그아웃
                </button>
              </div>
            )}
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
