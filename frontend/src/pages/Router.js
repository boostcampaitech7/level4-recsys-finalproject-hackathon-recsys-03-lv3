import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "../components/Layout";
//import Dashboard from "./Dashboard";
import LoginPage from "./LoginPage";
import Chat from "./Chat";

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
          <Route path="/chat" element={<Chat />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRouter;
