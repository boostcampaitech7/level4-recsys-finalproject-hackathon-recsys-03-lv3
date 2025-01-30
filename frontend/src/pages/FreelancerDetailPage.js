import React from "react";
import ProfileIcon from "../components/ProfileIcon";
import profileExample from "../assets/profile_example5.jpg";
import "../style/FreelancerDetailPage.css";
import RadarChart from "../components/RadarChart";
import SkillIcon from "../components/UserSkillTag";
import DoughnutChart from "../components/DoughnutChart";
import StaticStarRating from "../components/StaticStarRating";

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
              {freelancerInfo.skillList.map((skill) => (
                <SkillIcon text={skill.skillName} score={skill.skillScore} />
              ))}
              {/* 더 많은 스킬 배지 추가 가능 */}
            </div>
          </div>
        </div>
        <div
          className="d-flex align-items-center mx-5"
          style={{ marginTop: "20px" }}
        >
          <div className="row">
            <h4>소개</h4>
            <h6>{freelancerInfo.freelancerContent}</h6>
          </div>
        </div>
      </div>
      <div className="button-right align-items-center">
        <button type="button" className="btn-suggest" href="#">
          제안하기
        </button>
      </div>
    </div>
  );
};

const ProjectRates = ({ freelancerInfo, prograss }) => {
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
          numRates={prograss.projectCount}
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

const ProjectStatus = ({ prograss }) => {
  return (
    <div className="project-status container-fluid detail-card">
      <div className="row">
        <div>
          <h4>프로젝트 진행 상황</h4>
          {prograss.projectCount}건
        </div>
        <DoughnutChart
          data={[prograss.completedCount, prograss.ongoingCount]}
        />
      </div>
    </div>
  );
};

const ProjectHistory = ({ history }) => {
  return (
    <div
      className="project-history container-fluid detail-card mt-4"
      //   style={{ height: "300px", overflow: "hidden" }}
    >
      <div className="history-list">
        <div className="row">
          {history.map((project) => (
            <div className="card mb-3 d-flex">
              <div className="card-body">
                <div className="row">
                  <div className="col-md-9">
                    <h5 className="card-title">{project.projectName}</h5>
                    <p className="card-text">금액: {project.budget}원</p>
                    <p className="card-text">기간: {project.duration}일</p>
                  </div>
                  <div className="col-md-3">
                    평가{" "}
                    <StaticStarRating
                      rating={
                        (project.expertise +
                          project.proactiveness +
                          project.punctuality +
                          project.communication +
                          project.maintainability) /
                        5
                      }
                    />
                    <br />
                    <div className="row">
                      <div className="col-md-6">전문성</div>
                      <div className="col-md-6">{project.expertise}</div>
                      <div className="col-md-6">적극성</div>
                      <div className="col-md-6">{project.proactiveness}</div>
                      <div className="col-md-6">일정 준수</div>
                      <div className="col-md-6">{project.punctuality}</div>
                      <div className="col-md-6">의사소통</div>
                      <div className="col-md-6">{project.communication}</div>
                      <div className="col-md-6">유지보수</div>
                      <div className="col-md-6">{project.maintainability}</div>
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

const ProfilePage = () => {
  const freelancerInfo = {
    freelancerId: 123,
    freelancerName: "박왕균이",
    workExp: 5,
    price: 100000000,
    workType: 1,
    role: "백엔드 개발자",
    freelancerContent: "안녕하세요! 저 잘합니다.",
    locationName: "서울특별시 강남구",
    categoryList: ["IT•정보통신업", "건설업"],
    skillList: [
      { skillName: "Python", skillScore: 4.5 },
      { skillName: "Django", skillScore: 4.0 },
    ],
    reviewCount: 3,
    expertise: 4.2,
    proactiveness: 4.3,
    punctuality: 4.1,
    communication: 4.4,
    maintainability: 4.0,
  };

  const prograss = {
    projectCount: 20,
    ongoingCount: 5,
    completedCount: 10,
  };

  const history = [
    {
      projectId: 101,
      projectName: "AI Chatbot Development",
      duration: 6,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 1,
      registerDate: "20250125",
      companyName: "TechCorp",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      feedbackScore: 4.2,
      expertise: 4.5,
      proactiveness: 4.0,
      punctuality: 4.2,
      communication: 4.3,
      maintainability: 4.0,
      feedbackContent: "Great performance and timely delivery.",
    },
    {
      projectId: 102,
      projectName: "E-commerce Website",
      duration: 3,
      budget: 2000000,
      workType: 0,
      contractType: 1,
      status: 2,
      registerDate: "20250110",
      companyName: "ShopEase",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      feedbackScore: null,
      expertise: 4,
      proactiveness: 5,
      punctuality: 3,
      communication: 2,
      maintainability: 4,
      feedbackContent: null,
    },
  ];

  return (
    <div className="profile-page container-fluid">
      <ProfileHeader freelancerInfo={freelancerInfo} />
      <div className="container-fluid detail-card scrollable bg-light mt-4">
        <div className="row">
          <h3>프로젝트 히스토리</h3>
          <div className="col-md-6 d-flex">
            <ProjectRates freelancerInfo={freelancerInfo} prograss={prograss} />
          </div>
          <div className="col-md-6 d-flex">
            <ProjectStatus prograss={prograss} />
          </div>
          <ProjectHistory history={history} />
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
