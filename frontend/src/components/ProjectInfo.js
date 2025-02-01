import React from "react";
import InfoCard from "./InfoCard";
import ProjectKeywordIcon from "./ProjectKeywordIcon";
import ProjectSkillTag from "./ProjectSkillTag";
import "../style/ProjectInfo.css";
import "../style/colors.css";

const ProjectInfo = ({ projectinfo1 }) => {
  const { title, skills, where, start_day, day, pay, job, category, state } =
    projectinfo1;
  return (
    <InfoCard>
      <div className="status">
        {state === 0 ? (
          <ProjectKeywordIcon color="var(--color-primary)" text="모집 중" />
        ) : (
          <ProjectKeywordIcon color="var(--color-secondary)" text="모집 완료" />
        )}
      </div>
      <div class="title">
        <a href="#" style={{ color: "black", textDecoration: "none" }}>
          <strong>{title}</strong>
        </a>
      </div>
      <div class="details-row">
        <span class="label">예상 금액</span>
        <span class="value">{pay}</span>
        <span class="category">{job}</span>
      </div>
      <div class="details-row">
        <span class="label">예상 기간</span>
        <span class="value">{day}일</span>
        <span class="category2">{category}</span>
      </div>
      <div class="details-row2">
        <span class="labe-date1">근무 시작일</span>
        <span class="value2">
          {start_day
            .replace(/(\d{4})(\d{2})(\d{2})/, "$1년 $2월 $3일")
            .replace(/\b0(\d)/g, "$1")}
        </span>
        <span class="skills d-flex flex-wrap mt-3">
          {skills.map((skill, index) => (
            <ProjectSkillTag key={index} text={skill} />
          ))}
        </span>
      </div>
      <div class="location">
        <i class="fas fa-map-marker-alt"></i>
        <span class="location2">{where}</span>
      </div>
    </InfoCard>
  );
};
export default ProjectInfo;
