import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "../components/Layout";
//import Dashboard from "./Dashboard";
import LoginPage from "./LoginPage";
import SearchProjectPage from "./SearchProjectPage";
import Chat from "./ChatPage";
import SearchFreelancer from "./SearchFreelancerPage";
import RecommendFreelancer from "./RecommendFreelancerPage";
import RegisteredProjects from "./RegisteredProjectsPage";
import FreelancerDetailPage from "./FreelancerDetailPage";
import FreelancerSuggestPage from "./FreelancerSuggestPage";
import MainPage from "./MainPage";
import CompanyMyPage from "./CompanyMyPage";

const AppRouter = () => {
  // 로그인 정보 상태(state) 저장
  const [token, setToken] = useState(
    sessionStorage.getItem("token") || localStorage.getItem("token")
  );
  const [userId, setUserId] = useState(
    sessionStorage.getItem("userId") || localStorage.getItem("userId")
  );
  const [userName, setUserName] = useState(
    sessionStorage.getItem("userName") || localStorage.getItem("userName")
  );
  const [userType, setUserType] = useState(
    sessionStorage.getItem("userType") || localStorage.getItem("userType")
  );

  // sessionStorage 값 변경 감지
  useEffect(() => {
    const handleStorageChange = () => {
      setToken(
        sessionStorage.getItem("token") || localStorage.getItem("token")
      );
      setUserId(
        sessionStorage.getItem("userId") || localStorage.getItem("userId")
      );
      setUserName(
        sessionStorage.getItem("userName") || localStorage.getItem("userName")
      );
      setUserType(
        sessionStorage.getItem("userType") || localStorage.getItem("userType")
      );
    };

    // window 이벤트 리스너 추가 (로그인 후 변경 감지)
    window.addEventListener("storage", handleStorageChange);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  return (
    <Router>
      <Routes>
        {/* 로그인 페이지 */}
        <Route path="/login" element={<LoginPage />} />

        {/* Layout 적용된 경로 */}
        <Route path="/" element={<Layout />}>
          {/* Layout 내부의 하위 경로 */}
          {/* <Route index element={<Dashboard />} /> */}
          {/* 추가 경로 */}
          <Route path="/main-page" element={<MainPage />} />
          <Route path="/search-project" element={<SearchProjectPage />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/search-freelancer" element={<SearchFreelancer />} />
          <Route
            path="/recommend-freelancer"
            element={<RecommendFreelancer />}
          />
          <Route path="/freelancer-detail" element={<FreelancerDetailPage />} />
          <Route path="/registered-projects" element={<RegisteredProjects />} />
          <Route path="/suggest" element={<FreelancerSuggestPage />} />
          <Route
            path="/mypage"
            element={
              userType === "0" ? <FreelancerDetailPage /> : <CompanyMyPage />
            }
          />
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRouter;
