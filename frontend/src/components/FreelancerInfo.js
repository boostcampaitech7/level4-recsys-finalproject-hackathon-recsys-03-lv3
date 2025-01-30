import React from "react";
import InfoCard from "./InfoCard";
import ProfileIcon from "./ProfileIcon";
import FreelancerSkillTag from "./FreelancerSkillTag";
import RadarChart from "./RadarChart";
import "../style/FreelancerInfo.css";

const FreelancerInfo = ({ profile }) => {
  const { photo, name, field, experience, introduction, skills, radarData } =
    profile;

  const parsedSkills = skills.map((skillString) => {
    // 정규식을 사용해 기술 이름과 점수를 분리
    const match = skillString.match(/^(.*)\s(\d+)$/);
    if (match) {
      const skill = match[1]; // 점수 앞의 모든 부분을 기술 이름으로
      const score = parseInt(match[2], 10); // 숫자를 점수로 변환
      return { skill, score };
    }
    // 예외 처리: 유효하지 않은 형식의 데이터는 기본값 반환
    return { skill: skillString, score: 0 };
  });

  return (
    <InfoCard>
      <div className="d-flex align-items-center">
        {/* 프로필 사진 */}
        <div className="profile-photo p-3 me-5">
          <ProfileIcon profileImage={photo} />
        </div>

        {/* 프로필 정보 */}
        <div className="profile-info me-4" style={{ flex: 2 }}>
          <h5 className="fw-bold mb-1">{name}</h5>
          <div className="field mb-2">
            {field} | {experience}
          </div>
          <div className="intro">{introduction}</div>

          <div className="skills d-flex flex-wrap mt-3">
            {parsedSkills.map(({ skill, score }, index) => (
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
