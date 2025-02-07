import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../style/ProjectRegisterPage.css";
import botphoto from "../assets/chat_logo.png";
import ProfileIcon from "../components/ProfileIcon";
import SimilarProject from "../components/SimilarProject";
import ProjectSkillTag from "../components/ProjectSkillTag";

function convertToJSX(text) {
  const sections = text
    .slice(1, -1)
    .split(/<([^<>]+)>/)
    .filter(Boolean); // 꺽쇠 괄호를 기준으로 텍스트 분리
  let jsxElements = [];

  for (let i = 0; i < sections.length; i++) {
    const content = sections[i].trim();

    if (i % 2 === 1) {
      // 짝수 인덱스 -> 제목 (꺽쇠 안의 내용)
      jsxElements.push(<h5 key={i}>{content}</h5>);
    } else {
      // 홀수 인덱스 -> 본문 (꺽쇠 괄호 밖의 내용)
      const paragraphs = content.split(/\n+/).filter(Boolean); // 개행 문자 기준으로 나누고 빈 문자열 제거
      paragraphs.forEach((para, index) => {
        jsxElements.push(<p key={`${i}-${index}`}>{para.trim()}</p>);
      });
    }
  }

  return <div>{jsxElements}</div>;
}

const ProjectRegisterPage = () => {
  const location = useLocation();
  const { projectSummary } = location.state || {};
  const navigate = useNavigate();

  if (!projectSummary) {
    return <div>프로젝트 데이터가 없습니다. 다시 시도해주세요.</div>;
  }

  return (
    <div className="chat-page result">
      {/* Header */}
      <div className="chat-header">
        <span>새 프로젝트 등록</span>
      </div>

      {/* Chat Body */}
      <div className="chat-body">
        <div className="chat-bubble bot">
          <div className="chat-icon m-2">
            <ProfileIcon
              profileImage={botphoto}
              style={{
                width: "45px",
                height: "47px",
                margin: "0",
              }}
            />
          </div>
          <div className="chat-content bot">
            <div className="content-box">
              <p className="label">요청하신 프로젝트의 내용을 확인해주세요.</p>
              <table className="custom-table rounded-table">
                <tbody>
                  <tr>
                    <td className="table-label">프로젝트 명</td>
                    <td className="table-value">
                      {projectSummary.projectName || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">필요 스킬</td>
                    <td className="table-value">
                      {projectSummary.skillNameList.map((skill, index) => (
                        <span>
                          {skill}
                          {index === projectSummary.skillNameList.length - 1
                            ? ""
                            : ", "}
                        </span>
                      )) || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">프로젝트 기간</td>
                    <td className="table-value">
                      {projectSummary.duration.toLocaleString() || "미정"}일
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">근무 형태</td>
                    <td className="table-value">
                      {projectSummary.workType === 0
                        ? "대면"
                        : "원격" || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">계약 유형</td>
                    <td className="table-value">
                      {projectSummary.contractType === 0
                        ? "월 단위"
                        : "프로젝트 단위" || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">계약 시 우선순위</td>
                    <td className="table-value">
                      {projectSummary.priority === 0
                        ? "스킬"
                        : projectSummary.priority === 1
                          ? "금액"
                          : "상관없음" || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">금액</td>
                    <td className="table-value">
                      {projectSummary.expectedBudget.toLocaleString() || "미정"}
                      원 /
                      {projectSummary.contractType === 0
                        ? " 월"
                        : " 프로젝트" || "월"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">프로젝트 세부 내용</td>
                  </tr>
                  {/* Solar 결과 넣기 */}
                  <tr className="table-full-row">
                    <td colSpan="2" className="table-extra">
                      {convertToJSX(projectSummary.projectContent)}
                    </td>
                  </tr>
                </tbody>
              </table>
              <div className="register-btn-container">
                {/* 수정 필요 */}
                <button
                  className="register-btn btn-edit"
                  type="button"
                  id="sendRequest"
                  onClick={() => {
                    alert("요청이 완료되었습니다.");
                    window.location.reload(); //window.location.href = "https://example.com";
                  }}
                >
                  수정
                </button>
                <button
                  className="register-btn btn-confirm"
                  type="button"
                  id="sendRequest"
                  onClick={() => {
                    alert("요청이 완료되었습니다.");
                    navigate("/registered-projects");
                  }}
                >
                  등록
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="predict-things">
          <div className="predict-left">
            <SimilarProject projects={projectSummary.similarProjects} />
          </div>
          <div className="predict-right">
            <div className="predict-top">
              <h3 className="section-title">
                예상 견적{" "}
                <span className="unit">
                  ({projectSummary.contractType === 0 ? "월" : "프로젝트"} 단위)
                </span>
              </h3>
              <p className="description">
                유사 프로젝트 데이터를 바탕으로 AI가 분석한 예상 견적입니다.
              </p>
              <div className="estimate-values">
                <div className="estimate-row">
                  <p className="estimate-label">기업의 예상 금액</p>
                  <p className="company-estimate">
                    {projectSummary.budget.toLocaleString()}원
                  </p>
                </div>
                <div className="estimate-row">
                  <p className="estimate-label">AI의 예상 금액</p>
                  <p className="ai-estimate">
                    {projectSummary.expectedBudget.toLocaleString()}원
                  </p>
                </div>
              </div>
              <div className="slider-container">
                <span className="min-value">
                  최저 {projectSummary.minBudget.toLocaleString()}원
                </span>
                <input
                  type="range"
                  min={projectSummary.minBudget}
                  max={projectSummary.maxBudget}
                  value={projectSummary.expectedBudget}
                  readOnly
                />
                <span className="max-value">
                  최고 {projectSummary.maxBudget.toLocaleString()}원
                </span>
              </div>
            </div>
            <div className="predict-bottom">
              <h3 className="section-title">예상 기술 요구사항</h3>
              <p className="description">
                유사 프로젝트에 사용된 스킬을 바탕으로 AI가 분석한 예상 기술
                요구사항입니다.
              </p>
              <div className="skill-container">
                {projectSummary.simSkillNameList.map((skill, i) => (
                  <span key={i} className="badge">
                    <ProjectSkillTag text={skill} />
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectRegisterPage;
