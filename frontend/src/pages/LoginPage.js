import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo_primary.png";
import "../style/LoginPage.css";

const LoginPage = ({ setIsLoggedIn }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(
    localStorage.getItem("rememberMe") === "true"
  );
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (email === "test@example.com" && password === "1") {
      setIsLoggedIn(true); // 로그인 상태 업데이트

      // 로그인 유지 설정
      if (rememberMe) {
        localStorage.setItem("rememberMe", "true");
      } else {
        localStorage.removeItem("rememberMe");
      }

      navigate("/");
    } else {
      alert("잘못된 이메일 또는 비밀번호입니다.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* 로고 */}
        <div className="login-logo">
          <img src={logo} alt="Harmony Logo" />
        </div>

        {/* 캐치프레이즈 */}
        <p className="login-caption">HRmony</p>

        {/* 로그인 폼 */}
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="email"
            placeholder="이메일"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="비밀번호"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <div className="login-options">
            <label className="remember-me">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={() => setRememberMe((prev) => !prev)}
              />
              로그인 상태 유지
            </label>
            <a href="/forgot-password" className="forgot-password">
              비밀번호 찾기
            </a>
          </div>

          <button type="submit" className="login-button">
            로그인
          </button>
        </form>

        {/* 회원가입 링크 */}
        <p className="register-text">
          아직 회원이 아니신가요? <a href="/register">회원가입</a>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
