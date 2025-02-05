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
import SearchFreelancer from "./SearchFreelancerPage";
import RecommendFreelancer from "./RecommendFreelancerPage";
import SearchProjectPage from "./SearchProjectPage";
import RegisteredProjects from "./RegisteredProjectsPage";
import Chat from "./ChatPage";
import FreelancerDetailPage from "./FreelancerDetailPage";
import AppliedProjectPage from "./AppliedProjectPage";
import FinishedProjectPage from "./FinishedProjectPage";
import FreelancerSuggestPage from "./FreelancerSuggestPage";

const AppRouter = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem("rememberMe") === "true";
  });

  useEffect(() => {
    const savedLogin = localStorage.getItem("rememberMe") === "true";
    setIsLoggedIn(savedLogin);
  }, []);

  // const handleLogout = () => {
  //   localStorage.removeItem("rememberMe"); // 로그인 유지 해제
  //   setIsLoggedIn(false); // 상태 변경
  // };

  return (
    <Router>
      <Routes>
        {/* 로그인 페이지 */}
        <Route
          path="/login"
          element={<LoginPage setIsLoggedIn={setIsLoggedIn} />}
        />

        <Route
          path="/"
          element={
            <Layout isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
          }
        >
          {/* 메인 페이지를 기본으로 설정 */}
          <Route index element={<MainPage />} />

          <Route path="/search-freelancer" element={<SearchFreelancer />} />
          <Route path="/search-project" element={<SearchProjectPage />} />

          {/* 추가 경로 */}
          {isLoggedIn ? (
            <>
              <Route
                path="/recommend-freelancer"
                element={<RecommendFreelancer />}
              />
              <Route
                path="/registered-projects"
                element={<RegisteredProjects />}
              />
              <Route path="/chat" element={<Chat />} />
              <Route
                path="/freelancer-detail"
                element={<FreelancerDetailPage />}
              />
              <Route path="/applied" element={<AppliedProjectPage />} />
              <Route path="/finished" element={<FinishedProjectPage />} />
              <Route path="/suggest" element={<FreelancerSuggestPage />} />
            </>
          ) : (
            <Route path="*" element={<Navigate to="/" replace />} />
          )}
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRouter;
