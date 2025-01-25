import React, { useState } from "react";
import Topbar from "./Topbar";
import Footer from "./Footer";
import FreelancerInfo from "./FreelancerInfo";
import { Outlet } from "react-router-dom";
import photo from "../assets/profile_example1.jpg";

const Layout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const freelancerProfile = {
    photo: photo, // 프로필 사진 URL
    name: "희수희수야",
    field: "백엔드 개발자",
    experience: "7년 | 비대면 | 양산",
    introduction:
      "27년 차 Java 개발자로, 백엔드와 프론트엔드 개발에 모두 능숙합니다. 데이터베이스 설계 및 관리 경험이 풍부하며, 앱 개발과 배포까지 전 과정을 주도한 경험이 있습니다.",
    skills: ["Java 9", "Spring Boot 7", "jQuery 6", "SQL 6", "AJAX 4", "JSP 3"],
    radarData: [5, 4, 3, 4, 3], // 점수 ["전문성", "적극성", "일정준수", "유지보수", "의사소통"] 순순
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div id="wrapper" className="d-flex">
      <div id="content-wrapper" className="d-flex flex-column">
        <div id="content">
          <Topbar toggleSidebar={toggleSidebar} />
          <div className="container-fluid">
            <div>
              <FreelancerInfo profile={freelancerProfile} />
            </div>
            <Outlet />
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;
