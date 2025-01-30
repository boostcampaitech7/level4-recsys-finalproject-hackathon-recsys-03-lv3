import React, { useState } from "react";
import InfoCard from "./InfoCard";
import FreelancerSkillTag from "./FreelancerSkillTag";
import StarRating from "./StarRating";
import RadarChart from "./RadarChart";
import "../style/FinishedProjectContent.css";

const FinishedProjectContent = ({ content }) => {
  const {
    title,
    duration,
    startDate,
    endDate,
    category = "개발",
    role,
    skills = [],
    price,
    radarData,
    comment,
  } = content;

  // 평가 여부 상태 관리
  const [isReviewed, setIsReviewed] = useState(false);

  return (
    <InfoCard>
      <div
        className={`finished-project-container ${isReviewed ? "review-mode" : ""}`}
      >
        {/* 왼쪽: 프로젝트 정보 */}
        <div className="left-section">
          <h3 className="project-title">{title}</h3>

          {/* 금액 표시 (평가 후에만 보이도록) */}
          <p className={`project-price ${isReviewed ? "visible" : ""}`}>
            <strong>금액:</strong> {price.toLocaleString()}원
          </p>

          <div className="project-info-grid">
            <div className="project-info-left">
              <p>
                <strong>기간:</strong> {duration}일
              </p>
              <p>
                <strong>작업 시작일:</strong> {startDate}
              </p>
              <p>
                <strong>작업 종료일:</strong> {endDate}
              </p>
            </div>
            <div className="project-info-right">
              <p>
                <strong>{category}</strong>
              </p>
              <p>{role}</p>
              <div className="skills">
                {skills.length > 0 ? (
                  skills.map((skill, index) => (
                    <FreelancerSkillTag key={index} text={skill} score={10} />
                  ))
                ) : (
                  <span>스킬 정보 없음</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* 오른쪽: 평가 정보 */}
        <div className="right-section">
          {!isReviewed ? (
            <div className="before-review-container">
              <button
                className="review-button"
                onClick={() => setIsReviewed(true)}
              >
                평가하기
              </button>
              <p className="review-placeholder-text">
                평가를 완료하면 점수가 표시됩니다.
              </p>
            </div>
          ) : (
            <>
              <div className="rating">
                <StarRating />
              </div>
              <div className="radar-chart">
                <RadarChart data={radarData ?? [0, 0, 0, 0, 0]} />
              </div>
              {comment && <p className="review-comment">"{comment}"</p>}
            </>
          )}
        </div>
      </div>
    </InfoCard>
  );
};

export default FinishedProjectContent;
