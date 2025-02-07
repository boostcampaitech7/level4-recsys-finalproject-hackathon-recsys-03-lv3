import React from "react";
import InfoCard from "../components/InfoCard";
import ProfileIcon from "../components/ProfileIcon.js";
import photo from "../assets/profile_example1.jpg";
import "../style/CompanyMyPage.css";
import "../style/colors.css";

const CompanyMyPage = () => {
  const company = {
    companyId: 1,
    companyName: "(주) 왕균이 증권",
    companyContent:
      "최고의 단짝을 찾아주는 미팅주선 업체최고의 단짝을 찾아주는 미팅주선팅주선 업체최고의 단짝을 찾아주는 미팅주선 업체최고의 단짝을 찾아주는 미팅주선 업체",
    locationName: "서울특별시 강남구",
  };

  return (
    <>
      <div className="page-container">
        <InfoCard>
          <div className="profile-photo p-3">
            <ProfileIcon profileImage={photo} />
            <div className="company-info">
              <h2 className="company-name">{company.companyName}</h2>
              <p className="company-address">{company.locationName}</p>
            </div>
          </div>
          <div className="intro-section">
            <p className="company-introduction">기업 소개</p>
            <p className="company-content">{company.companyContent}</p>
          </div>
        </InfoCard>
        <div class="button-container">
          <button class="edit-button">정보수정</button>
        </div>
      </div>
    </>
  );
};
export default CompanyMyPage;
