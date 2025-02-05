import React, { useEffect, useState } from "react";
import AppRouter from "./pages/Router";

const checkTokenExpiration = () => {
  const expiresAt = localStorage.getItem("expiresAt");

  if (expiresAt && new Date().getTime() > expiresAt) {
    alert("세션이 만료되었습니다. 다시 로그인하세요.");
    handleLogout();
  }
};

const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("expiresAt");
  window.location.href = "/login"; // 로그인 페이지로 이동
};

const App = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    checkTokenExpiration();
  }, []);

  useEffect(() => {
    fetch("/")
      .then((response) => response.json())
      .then((data) => setMessage(data.message));
    //.catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
      {/* 라우터 컴포넌트*/}
      <AppRouter />
      <p>{message}</p>
    </div>
  );
};

export default App;
