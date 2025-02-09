import React from "react";
import InfoCard from "./InfoCard";
import ProjectKeywordIcon from "./ProjectKeywordIcon";
import ProjectSkillTag from "./ProjectSkillTag";
import "../style/ProjectInfo.css";
import "../style/colors.css";

const ProjectInfo = ({ content, className = "", onClick = null }) => {
  const formatDateUsingMath = (dateNumber) => {
    let year = Math.floor(dateNumber / 10000); // 2025
    let month = Math.floor((dateNumber % 10000) / 100); // 2
    let day = dateNumber % 100; // 12

    return `${year}년 ${month}월 ${day}일`;
  };

  const {
    projectId, // 프로젝트 ID
    projectName, // 프로젝트 이름
    duration, // 기간(단위: 일)
    budget, // 예상 금액
    workType, // 근무 형태 (대면: 0, 원격: 1)
    contractType, // 계약 형태(월 단위: 0, 프로젝트 단위: 1)
    status, // 진행상태 (시작 전: 0, 진행 중: 1, 완료: 2)
    registerDate, // 작업 시작일 (YYYYMMDD 형식)
    categoryName, // 도메인
    categoryRole = "개발", // 직군
    skillIdList, // 스킬 ID 리스트
    skillNameList, // 스킬 이름 리스트
    locationName, // 지역명
    isReviewed, // 평가 여부
  } = content || {};

  return (
    <InfoCard className={className}>
      <div className="project-container">
        <div className="status">
          {status === 0 ? (
            <ProjectKeywordIcon color="var(--color-secondary)" text="모집 중" />
          ) : (
            <ProjectKeywordIcon color="var(--color-star)" text="모집 완료" />
          )}
          {workType === 0 ? (
            <ProjectKeywordIcon color="var(--color-secondary)" text="대면" />
          ) : (
            <ProjectKeywordIcon color="var(--color-secondary)" text="원격" />
          )}
          <ProjectKeywordIcon color="var(--color-primary)" text="NEW" />
        </div>

        <h3 className="project-title">
          <a className="project-link pointer" onClick={onClick}>
            {projectName}
          </a>
        </h3>
        <div className="project-info-grid">
          <div className="project-info-left">
            <p>
              <strong>예상 금액:</strong> {budget.toLocaleString()}원
            </p>
            <p>
              <strong>예상 기간:</strong> {duration}일
            </p>
            <p>
              <strong>근무 시작일:</strong> {formatDateUsingMath(registerDate)}
            </p>
          </div>
          <div className="project-info-right">
            <p>
              <strong>직군:</strong> {categoryRole}
            </p>
            <p>
              <strong>분야:</strong> {categoryName}
            </p>
            <div className="project-location">
              <i className="fas fa-map-marker-alt"></i>
              <p>{locationName}</p>
            </div>
          </div>
        </div>
        <div className="skills">
          {skillNameList && skillNameList.length > 0 ? (
            skillNameList.map((skill, index) => (
              // 각 스킬 태그 출력
              <ProjectSkillTag key={index} text={skill} />
            ))
          ) : (
            <span>스킬 정보 없음</span>
          )}
        </div>
      </div>
    </InfoCard>
  );
};

export default ProjectInfo;
