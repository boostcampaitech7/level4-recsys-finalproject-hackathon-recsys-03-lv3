import React from "react";
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

const AppRouter = () => {
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
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRouter;
