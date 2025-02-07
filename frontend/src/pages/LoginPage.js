import React, { useState } from "react";
import logo from "../assets/logo_primary.png";
import "../style/LoginPage.css";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null); // 기존 에러 초기화

    try {
      const response = await fetch(
        `${process.env.REACT_APP_BASE_URL}/api/auth/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ email, password }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Login failed");
      }

      // 토큰 저장
      sessionStorage.setItem("token", data.token);

      const expiresAt = new Date().getTime() + 60 * 60 * 1000; // 1시간 후 (밀리초 단위)

      sessionStorage.setItem("userId", data.userId);
      sessionStorage.setItem("userName", data.userName);
      sessionStorage.setItem("userType", data.userType);
      sessionStorage.setItem("expiresAt", expiresAt); // 만료 시간 저장

      console.log("Login Success:", data);

      // 로그인 성공 후 메인 페이지 이동
      window.location.href = "/";
    } catch (err) {
      console.error("Login Error:", err.message);
      setError(err.message);
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
          아직 회원이 아니신가요? <a href="/signup">회원가입</a>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
