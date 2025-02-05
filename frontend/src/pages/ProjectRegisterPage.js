import React from "react";
import "../style/ProjectRegisterPage.css";
import botphoto from "../assets/chat_logo.png";
import { useLocation } from "react-router-dom";
import ProfileIcon from "../components/ProfileIcon";
import SimilarProject from "../components/SimilarProject";
import ProjectSkillTag from "../components/ProjectSkillTag";

const ProjectRegisterPage = () => {
  const location = useLocation();
  const { projectData } = location.state || {};
  const skillNameList = ["Java", "Spring", "REST"];

  if (!projectData) {
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
                      {projectData.projectContent || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">프로젝트 기간</td>
                    <td className="table-value">
                      {projectData.duration || "미정"}일
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">근무 형태</td>
                    <td className="table-value">
                      {projectData.workMode || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">계약 유형</td>
                    <td className="table-value">
                      {projectData.projectType || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">계약 시 우선순위</td>
                    <td className="table-value">
                      {projectData.priority || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">예상 금액</td>
                    <td className="table-value">
                      {projectData.budget || "미정"}원 (
                      {projectData.contrastType || "월"} 단위)
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">프로젝트 세부내용</td>
                  </tr>
                  <tr className="table-full-row">
                    <td colSpan="2" className="table-extra">
                      <span className="fw-bold">프로젝트 진행 상황:</span>
                      <p>
                        기획/디자인/개발환경 세팅이 완료된 상태입니다. 플랫폼의
                        ERD 및 개발 소스는 보유 중입니다.
                      </p>
                      <span className="fw-bold">주요 담당 업무:</span>
                      <p>
                        Java로 변환/구축하는 작업 수행, 초기에 개발 환경 조성 및
                        세팅 작업.
                      </p>
                      <span className="fw-bold">상세 업무 범위:</span>
                      <p>
                        기존 플랫폼의 언어 변환 작업, 유지보수 작업과 함께 MSSQL
                        서버 사용 예정.
                      </p>
                      <span className="fw-bold">기타 전달 사항:</span>
                      <p>
                        작업 최대한 빠르게 투입 가능한 분을 선정하고자 합니다.
                      </p>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div className="register-btn-container">
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
                    window.location.reload(); //window.location.href = "https://example.com";
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
            <SimilarProject />
          </div>
          <div className="predict-right">
            <div className="predict-top">
              <h3 className="section-title">
                예상 견적 <span className="unit">(월 단위)</span>
              </h3>
              <p className="description">
                왼쪽 유사한 프로젝트 데이터를 바탕으로 AI가 분석한 예상
                견적입니다.
              </p>
              <div className="estimate-values">
                <div className="estimate-row">
                  <p className="estimate-label">기업의 예상 금액</p>
                  <p className="company-estimate">3,000,000원</p>
                </div>
                <div className="estimate-row">
                  <p className="estimate-label">AI의 예상 금액</p>
                  <p className="ai-estimate">3,000,000원</p>
                </div>
              </div>
              <div className="slider-container">
                <span className="min-value">최저 100만</span>
                <input
                  type="range"
                  min="1000000"
                  max="4000000"
                  value="3000000"
                  readOnly
                />
                <span className="max-value">최고 400만</span>
              </div>
            </div>
            <div className="predict-bottom">
              <h3 className="section-title">예상 기술 요구사항</h3>
              <p className="description">
                왼쪽 유사한 프로젝트의 스킬을 바탕으로 AI가 분석한 예상 기술
                요구사항입니다.
              </p>
              <div className="skill-container">
                {skillNameList.map((skill, i) => (
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
