import React from "react";
import "../style/Images.css";

const ProfileIcon = ({ profileImage, style = {} }) => {
  return (
    <a href="#">
      <img
        src={profileImage}
        className="profile-image rounded-circle border"
        alt="profile-icon"
        style={style} // 외부에서 스타일 지정 시 적용
      ></img>
    </a>
  );
};

export default ProfileIcon;
