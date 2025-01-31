import React from "react";
import "../style/SimilarProject.css";
import ProjectSkillTag from "./ProjectSkillTag";

const SimilarProject = () => {
  const projects = [
    {
      projectId: 101,
      projectName: "Python 개발 프로젝트",
      duration: 30,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250125",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Django", "API"],
      locationName: "서울특별시 강남구",
      similarityScore: 15,
    },
    {
      projectId: 102,
      projectName: "Java 백엔드 개발",
      duration: 60,
      budget: 10000000,
      workType: 0,
      contractType: 1,
      status: 0,
      registerDate: "20250120",
      categoryName: "IT•정보통신업",
      skillIdList: [4, 5, 6],
      skillNameList: ["Java", "Spring", "REST"],
      locationName: "서울특별시 서초구",
      similarityScore: 12,
    },
    {
      projectId: 101,
      projectName: "Python 개발 프로젝트",
      duration: 30,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250125",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Django", "API"],
      locationName: "서울특별시 강남구",
      similarityScore: 15,
    },
  ];

  return (
    <div
      id="carouselExample"
      className="carousel slide"
      data-bs-ride="carousel"
    >
      <div className="carousel-inner">
        {/* 프로젝트 데이터를 두 개씩 묶어서 렌더링 */}
        {projects.reduce((acc, project, index) => {
          if (index % 2 === 0) {
            const slide = (
              <div
                className={`carousel-item ${index === 0 ? "active" : ""}`}
                key={index}
              >
                <div className="row">
                  {/* 첫 번째 카드 */}
                  <div className="col-md-12">
                    <div className="card p-3">
                      <a href="#">
                        <h5>{projects[index].projectName}</h5>
                      </a>
                      <p>{projects[index].categoryName}</p>
                      <p className="f-12">
                        금액: {projects[index].budget}원{" "}
                        <i class="bi bi-geo-alt"></i>
                        {projects[index].locationName}
                      </p>
                      <p className="f-12">
                        등록일:{" "}
                        {projects[index].registerDate
                          .replace(/(\d{4})(\d{2})(\d{2})/, "$1년 $2월 $3일")
                          .replace(/\b0(\d)/g, "$1")}
                      </p>
                      <div>
                        {projects[index].skillNameList.map((skill, i) => (
                          <span key={i} className="badge">
                            <ProjectSkillTag text={skill} />
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                  {/* 두 번째 카드 (데이터가 존재하는 경우) */}
                  {projects[index + 1] && (
                    <div className="col-md-12">
                      <div className="card p-3">
                        <a href="#">
                          <h5>{projects[index + 1].projectName}</h5>
                        </a>
                        <p>{projects[index + 1].categoryName}</p>
                        <p className="f-12">
                          금액: {projects[index + 1].budget}원{" "}
                          <i class="bi bi-geo-alt"></i>
                          {projects[index + 1].locationName}
                        </p>
                        <p className="f-12">
                          등록일:{" "}
                          {projects[index + 1].registerDate
                            .replace(/(\d{4})(\d{2})(\d{2})/, "$1년 $2월 $3일")
                            .replace(/\b0(\d)/g, "$1")}
                        </p>
                        <div>
                          {projects[index + 1].skillNameList.map((skill, i) => (
                            <span key={i} className="badge">
                              <ProjectSkillTag text={skill} />
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
            acc.push(slide);
          }
          return acc;
        }, [])}
      </div>
      <button
        className="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExample"
        data-bs-slide="prev"
      >
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Previous</span>
      </button>
      <button
        className="carousel-control-next"
        type="button"
        data-bs-target="#carouselExample"
        data-bs-slide="next"
      >
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Next</span>
      </button>
    </div>
  );
};

export default SimilarProject;
