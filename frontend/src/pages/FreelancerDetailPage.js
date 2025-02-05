import React, { useEffect, useState } from "react";
import axios from "axios";
import ProfileIcon from "../components/ProfileIcon";
import profileExample from "../assets/profile_example5.jpg";
import "../style/FreelancerDetailPage.css";
import RadarChart from "../components/RadarChart";
import FreelancerSkillTag from "../components/FreelancerSkillTag";
import DoughnutChart from "../components/DoughnutChart";
import StaticStarRating from "../components/StaticStarRating";
import ScoreDisplay from "../components/ScoreDisplay";

const API_BASE_URL = `${process.env.REACT_APP_BASE_URL}/api/resource`;

const ProfilePage = () => {
  const [freelancerInfo, setFreelancerInfo] = useState(null);
  const [progress, setProgress] = useState(null);
  const [history, setHistory] = useState([]);
  const freelancerId = parseInt(sessionStorage.getItem("userId"), 10); // 실제 사용 시 동적으로 설정 필요

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    if (!token) {
      console.error("인증 토큰이 없습니다.");
      return;
    }

    const headers = {
      Accept: "application/json",
      Authorization: `Bearer ${token}`,
    };

    const fetchFreelancerData = async () => {
      try {
        const [profileRes, progressRes, historyRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/${freelancerId}/profile`, { headers }),
          axios.get(`${API_BASE_URL}/${freelancerId}/progress`, { headers }),
          axios
            .get(`${API_BASE_URL}/${freelancerId}/feedback`, { headers })
            .catch((err) => {
              if (err.response && err.response.status === 404) {
                return { data: [] }; // 404 발생 시 빈 배열 반환
              }
              throw err;
            }),
        ]);

        setFreelancerInfo(profileRes.data);
        setProgress(progressRes.data);
        setHistory(historyRes.data);
      } catch (error) {
        console.error("데이터 불러오기 실패: ", error);
      }
    };

    fetchFreelancerData();
  }, [freelancerId]);

  if (!freelancerInfo || !progress) {
    return <div>로딩 중...</div>;
  }

  return (
    <div className="profile-page container-fluid">
      <ProfileHeader freelancerInfo={freelancerInfo} />
      <div className="container-fluid detail-card bg-light mt-4">
        <div className="row">
          <h3>프로젝트 히스토리</h3>
          <div className="col-md-6 d-flex">
            <ProjectRates freelancerInfo={freelancerInfo} progress={progress} />
          </div>
          <div className="col-md-6 d-flex">
            <ProjectStatus progress={progress} />
          </div>
          <ProjectHistory history={history} />
        </div>
      </div>
    </div>
  );
};

const ProfileHeader = ({ freelancerInfo }) => {
  return (
    <div className="profile-header container-fluid detail-card scrollable">
      <div className="row">
        <div className="d-flex align-items-center">
          <div className="mx-5">
            <ProfileIcon profileImage={profileExample} />
          </div>
          <div>
            <h3>{freelancerInfo.freelancerName}</h3>
            <p>
              {freelancerInfo.role} | {freelancerInfo.workExp}년 |{" "}
              {freelancerInfo.locationName}
            </p>
            <div>
              {freelancerInfo.skillList.map((skill, index) => (
                <FreelancerSkillTag
                  key={index}
                  text={skill.skillName}
                  score={skill.skillScore}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ProjectRates = ({ freelancerInfo, progress }) => {
  return (
    <div className="profile-stats container-fluid detail-card">
      <div className="row">
        <h4>프로젝트 평점</h4>
        <StaticStarRating
          rating={
            (freelancerInfo.expertise +
              freelancerInfo.proactiveness +
              freelancerInfo.punctuality +
              freelancerInfo.communication +
              freelancerInfo.maintainability) /
            5
          }
          numRates={progress.projectCount}
        />
        <RadarChart
          data={[
            freelancerInfo.expertise,
            freelancerInfo.proactiveness,
            freelancerInfo.punctuality,
            freelancerInfo.communication,
            freelancerInfo.maintainability,
          ]}
        />
      </div>
    </div>
  );
};

const ProjectStatus = ({ progress }) => {
  return (
    <div className="project-status container-fluid detail-card">
      <div className="row">
        <div>
          <h4>프로젝트 진행 상황</h4>
          {progress.projectCount}건
        </div>
        <DoughnutChart
          data={[progress.completedCount, progress.ongoingCount]}
        />
      </div>
    </div>
  );
};

const ProjectHistory = ({ history }) => {
  return (
    <div className="project-history container-fluid detail-card mt-4">
      <div className="history-list">
        <div className="row">
          {history.map((project, index) => (
            <div key={index} className="card mb-3 d-flex">
              <div className="card-body">
                <div className="row">
                  <div className="col-md-8">
                    <h5 className="card-title">{project.projectName}</h5>
                    <p className="card-text">
                      금액: {project.budget.toLocaleString()}원
                    </p>
                    <p className="card-text">기간: {project.duration}일</p>
                  </div>
                  <div className="col-md-4">
                    <div className="rating">
                      <div>
                        <ScoreDisplay score={project.feedbackScore} />
                      </div>
                    </div>
                    <div className="radar-chart">
                      <RadarChart
                        data={[
                          project.expertise,
                          project.proactiveness,
                          project.punctuality,
                          project.communication,
                          project.maintainability,
                        ]}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
