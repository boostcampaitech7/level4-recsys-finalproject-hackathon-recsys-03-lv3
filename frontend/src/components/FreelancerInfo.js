import React from "react";
import InfoCard from "./InfoCard";
import ProfileIcon from "./ProfileIcon";
import FreelancerSkillTag from "./FreelancerSkillTag";
import RadarChart from "./RadarChart";
import "../style/FreelancerInfo.css";

const FreelancerInfo = ({ profile }) => {
  const {
    photo,
    name,
    feedbackscore,
    feedbackcount,
    role,
    workexp,
    worktype,
    location,
    content,
    skills,
    radarData,
  } = profile;

  return (
    <InfoCard>
      <div className="d-flex align-items-center">
        {/* 프로필 사진 */}
        <div className="profile-photo p-3 me-5">
          <ProfileIcon profileImage={photo} />
        </div>

        {/* 프로필 정보 */}
        <div className="profile-info me-4" style={{ flex: 2 }}>
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="fw-bold mb-1">{name}</h5>
            <div className="feedback-score d-flex align-items-center">
              <span className="text-warning me-">★</span>
              <span className="fw-bold">{feedbackscore.toFixed(1)}</span>
              <span className="text-muted ms-1">({feedbackcount})</span>
            </div>
          </div>
          <div className="field mb-2">
            {role} | {workexp} | {worktype} | {location}
          </div>
          <div className="intro">{content}</div>

          <div className="skills d-flex flex-wrap mt-3">
            {skills.map(({ skill, score }, index) => (
              <FreelancerSkillTag key={index} text={skill} score={score} />
            ))}
          </div>
        </div>

        {/* 방사형 차트 */}
        <div className="radar-chart" style={{ flex: 1 }}>
          <RadarChart data={radarData} />
        </div>
      </div>
    </InfoCard>
  );
};

export default FreelancerInfo;
