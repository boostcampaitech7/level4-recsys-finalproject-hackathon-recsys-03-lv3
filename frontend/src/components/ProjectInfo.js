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
        {["모집 중", "상주", "NEW"].map((badgeText) => {
          if (state === badgeText) {
            return (
              <ProjectKeywordIcon
                color="var(--color-primary)"
                text={badgeText}
              />
            );
          }
          return (
            <ProjectKeywordIcon
              color="var(--color-secondary)"
              text={badgeText}
            />
          );
        })}
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
        <span class="value">{day}</span>
        <span class="category2">{category}</span>
      </div>
      <div class="details-row2">
        <span class="labe-date1">근무 시작일</span>
        <span class="value2">{start_day}</span>
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
