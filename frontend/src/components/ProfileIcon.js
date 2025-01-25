import React from "react";
import "../style/Images.css";

const ProfileIcon = ({ profileImage }) => {
  return (
    <a href="#">
      <img
        src={profileImage}
        className="profile-image rounded-circle border"
        alt="profile-icon"
      ></img>
    </a>
  );
};

export default ProfileIcon;
