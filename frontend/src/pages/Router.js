import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import Layout from "../components/Layout";
import LoginPage from "./LoginPage";
import MainPage from "./MainPage";
import SearchProjectPage from "./SearchProjectPage";
import Chat from "./ChatPage";
import SearchFreelancer from "./SearchFreelancerPage";
import RecommendFreelancer from "./RecommendFreelancerPage";
import RegisteredProjects from "./RegisteredProjectsPage";
import FreelancerDetailPage from "./FreelancerDetailPage";
import FreelancerSuggestPage from "./FreelancerSuggestPage";

const AppRouter = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem("rememberMe") === "true";
  });

  useEffect(() => {
    // 로그인 상태 유지 확인
    if (localStorage.getItem("rememberMe") === "true") {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("rememberMe"); // 로그인 유지 해제
    setIsLoggedIn(false); // 상태 변경
  };

  return (
    <Router>
      <Routes>
        {/* 로그인 페이지 */}
        <Route
          path="/login"
          element={<LoginPage setIsLoggedIn={setIsLoggedIn} />}
        />

        {/* 로그인 안 한 경우에만 로그인 페이지로 이동 */}
        <Route
          path="/"
          element={
            isLoggedIn ? (
              <Layout isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        >
          {/* 메인 페이지를 기본으로 설정 */}
          <Route index element={<MainPage />} />

          {/* 추가 경로 */}
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
        </Route>

        {/* 존재하지 않는 경로는 메인 페이지로 리디렉트 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
